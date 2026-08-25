"""Check that each provider responds and that the keys load."""

import os
from dotenv import load_dotenv

load_dotenv()


def check_anthropic():
    from anthropic import Anthropic

    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=50,
        messages=[{"role": "user", "content": "Reply with the single word: working"}],
    )
    return msg.content[0].text.strip()


def check_openai():
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    resp = client.chat.completions.create(
        model="gpt-5.6-luna",
        max_completion_tokens=50,
        messages=[{"role": "user", "content": "Reply with the single word: working"}],
    )
    return resp.choices[0].message.content.strip()


def check_xai():
    from openai import OpenAI

    client = OpenAI(
        api_key=os.environ["XAI_API_KEY"],
        base_url="https://api.x.ai/v1",
    )
    resp = client.chat.completions.create(
        model="grok-4",
        max_completion_tokens=50,
        messages=[{"role": "user", "content": "Reply with the single word: working"}],
    )
    return resp.choices[0].message.content.strip()


for name, fn in [
    ("anthropic", check_anthropic),
    ("openai", check_openai),
    ("xai", check_xai),
]:
    try:
        print(f"{name:12} {fn()}")
    except Exception as exc:
        print(f"{name:12} FAILED: {type(exc).__name__}: {exc}")
