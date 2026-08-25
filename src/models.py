"""One interface to Anthropic, OpenAI and xAI.

Every adapter returns the same dict, so nothing downstream needs to know which
provider answered:

    {
        "text":          str,   # assembled response text
        "thinking":      bool,  # whether a reasoning block was returned
        "input_tokens":  int,
        "output_tokens": int,
        "stop_reason":   str | None,
        "response_id":   str | None,
    }

Two behaviours established by testing rather than assumption, both documented
in the probe scripts at the repository root.

Sampling parameters were removed from the Anthropic SDK method signatures at
version 1.0. The API still accepts them, so temperature is passed through
`extra_body`.

Claude Opus 5 returns a thinking block before its answer. On twelve trials of
a vignette it did so every time. Response text is therefore assembled by
filtering content blocks by type and joining the text blocks, never by taking
the first block. Whether thinking occurred is recorded per call rather than
suppressed, since a judgement preceded by extended reasoning may not be the
same task as an immediate one.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv

load_dotenv()


class ModelError(RuntimeError):
    """A provider call that failed after all retries."""


@dataclass(frozen=True)
class ModelSpec:
    key: str          # short label used in the data
    provider: str     # anthropic | openai | xai
    model_id: str     # exact identifier sent to the API
    family: str       # grouping variable for analysis


# The models under test. Everything downstream reads the design off this list.
MODELS: list[ModelSpec] = [
    ModelSpec("haiku", "anthropic", "claude-haiku-4-5", "anthropic"),
    ModelSpec("sonnet", "anthropic", "claude-sonnet-5", "anthropic"),
    ModelSpec("opus", "anthropic", "claude-opus-5", "anthropic"),
    ModelSpec("sol", "openai", "gpt-5.6-sol", "openai"),
    ModelSpec("grok", "xai", "grok-4", "xai"),
]

XAI_BASE_URL = "https://api.x.ai/v1"

_clients: dict[str, Any] = {}


def get_model(key: str) -> ModelSpec:
    for spec in MODELS:
        if spec.key == key:
            return spec
    raise KeyError(f"No model registered under key {key!r}. "
                   f"Known: {', '.join(m.key for m in MODELS)}")


def _require(var: str) -> str:
    value = os.environ.get(var)
    if not value:
        raise ModelError(f"{var} is not set. Check your .env file.")
    return value


def _anthropic_client():
    if "anthropic" not in _clients:
        from anthropic import Anthropic

        _clients["anthropic"] = Anthropic(api_key=_require("ANTHROPIC_API_KEY"))
    return _clients["anthropic"]


def _openai_client():
    if "openai" not in _clients:
        from openai import OpenAI

        _clients["openai"] = OpenAI(api_key=_require("OPENAI_API_KEY"))
    return _clients["openai"]


def _xai_client():
    if "xai" not in _clients:
        from openai import OpenAI

        _clients["xai"] = OpenAI(
            api_key=_require("XAI_API_KEY"), base_url=XAI_BASE_URL
        )
    return _clients["xai"]


# --------------------------------------------------------------------------
# Adapters
# --------------------------------------------------------------------------

def _call_anthropic(spec, system, prompt, temperature, max_tokens):
    client = _anthropic_client()
    kwargs = {
        "model": spec.model_id,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
        "extra_body": {"temperature": temperature},
    }
    if system is not None:
        kwargs["system"] = system

    resp = client.messages.create(**kwargs)

    block_types = [b.type for b in resp.content]
    text = "".join(b.text for b in resp.content if b.type == "text")

    return {
        "text": text,
        "thinking": "thinking" in block_types,
        "input_tokens": resp.usage.input_tokens,
        "output_tokens": resp.usage.output_tokens,
        "stop_reason": resp.stop_reason,
        "response_id": resp.id,
    }


def _call_openai_compatible(client, spec, system, prompt, temperature, max_tokens):
    """Shared by OpenAI and xAI, which use the same request format."""
    messages = []
    if system is not None:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    resp = client.chat.completions.create(
        model=spec.model_id,
        messages=messages,
        max_completion_tokens=max_tokens,
        temperature=temperature,
    )
    choice = resp.choices[0]

    # Reasoning tokens are billed as output and reported separately when the
    # provider exposes them. Their presence is the analogue of a thinking block.
    details = getattr(resp.usage, "completion_tokens_details", None)
    reasoning_tokens = getattr(details, "reasoning_tokens", 0) or 0

    return {
        "text": (choice.message.content or "").strip(),
        "thinking": reasoning_tokens > 0,
        "input_tokens": resp.usage.prompt_tokens,
        "output_tokens": resp.usage.completion_tokens,
        "stop_reason": choice.finish_reason,
        "response_id": resp.id,
    }


def _call_openai(spec, system, prompt, temperature, max_tokens):
    return _call_openai_compatible(
        _openai_client(), spec, system, prompt, temperature, max_tokens
    )


def _call_xai(spec, system, prompt, temperature, max_tokens):
    return _call_openai_compatible(
        _xai_client(), spec, system, prompt, temperature, max_tokens
    )


_ADAPTERS = {
    "anthropic": _call_anthropic,
    "openai": _call_openai,
    "xai": _call_xai,
}


def call_model(
    spec: ModelSpec,
    prompt: str,
    system: str | None = None,
    temperature: float = 1.0,
    max_tokens: int = 600,
    retries: int = 4,
) -> dict:
    """Call one model once, retrying with exponential backoff on failure."""
    adapter = _ADAPTERS[spec.provider]
    delay = 2.0
    last: Exception | None = None

    for attempt in range(retries):
        try:
            return adapter(spec, system, prompt, temperature, max_tokens)
        except Exception as exc:
            last = exc
            if attempt < retries - 1:
                time.sleep(delay)
                delay *= 2

    raise ModelError(f"{spec.key} failed after {retries} attempts: {last}")


if __name__ == "__main__":
    # Smoke test: one trivial call to each registered model.
    for spec in MODELS:
        try:
            r = call_model(spec, "Reply with one word: working", max_tokens=50)
            print(f"{spec.key:8} {spec.model_id:20} thinking={str(r['thinking']):5} "
                  f"in={r['input_tokens']:4} out={r['output_tokens']:4} "
                  f"-> {r['text']!r}")
        except Exception as exc:
            print(f"{spec.key:8} {spec.model_id:20} FAILED: "
                  f"{type(exc).__name__}: {str(exc)[:100]}")
