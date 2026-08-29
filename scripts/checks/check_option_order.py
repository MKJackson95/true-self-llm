"""Is Haiku's forced-choice response driven by option position?

In the confirmatory run the forced-choice options always appeared in the same
order: true self (a), surface self (b), none of the above (c). Haiku selected
surface self on 85% of trials regardless of item class or version, while its
ratings on the same items showed the moral asymmetry strongly. A position bias
toward the second option would produce exactly that pattern.

This script re-runs the forced-choice measure with the option order reversed,
so that surface self appears first. If Haiku's responses follow the content,
the proportion selecting surface self should stay near 0.85. If they follow
the position, it should collapse.

Run as an exploratory control. Output goes to a separate file and does not
enter the confirmatory dataset.

    python check_option_order.py
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, "src")

from models import call_model, get_model
from prompts import load_stimuli, FRAME_SYSTEM
from parse import strip_markup, _LABEL, _CHOICE

STIMULI = "stimuli/nbk_study1.json"
OUT = Path("data/raw/option_order_control.jsonl")
MODELS = ["haiku", "opus", "grok"]
SAMPLES = 3
MAX_TOKENS = 1200

# Reversed relative to the confirmatory run: surface self first.
REVERSED_OPTIONS = [
    "His \"surface self\" (the things that he learned from society or others)",
    "His \"true self\" (the deepest, most essential aspect of his being)",
    "None of the above",
]

# Which letter now corresponds to which construct.
LETTER_TO_CONSTRUCT = {"a": "surface", "b": "true_self", "c": "neither"}


def build_prompt(stimuli: dict, item: dict, version: str) -> str:
    vignette = item[f"version_{version}"]
    options = "\n".join(
        f"({chr(97 + i)}) {opt}" for i, opt in enumerate(REVERSED_OPTIONS)
    )
    question = (
        f"{stimuli['measures']['forced_choice']['stem'].format(name=item['name'])}\n\n"
        f"{options}\n\n"
        "Give the letter of your choice, then explain your answer in one or "
        "two sentences."
    )
    return "\n\n".join([
        stimuli["framing"].format(name=item["name"]),
        vignette,
        question,
    ])


def extract(text: str):
    clean = _LABEL.sub("", strip_markup(text))
    match = _CHOICE.match(clean)
    if not match:
        return None
    return match.group(1).lower()


def main() -> int:
    stimuli = load_stimuli(STIMULI)
    items = [(it, "moral") for it in stimuli["moral_items"]] + \
            [(it, "preference") for it in stimuli["preference_items"]]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    counts = defaultdict(lambda: defaultdict(int))
    total = len(items) * 2 * len(MODELS) * SAMPLES
    n = 0

    print(f"{total} calls: {len(items)} items x 2 versions x "
          f"{len(MODELS)} models x {SAMPLES} samples\n")

    with OUT.open("a", encoding="utf-8") as fh:
        for key in MODELS:
            spec = get_model(key)
            for item, item_class in items:
                for version in ["a", "b"]:
                    prompt = build_prompt(stimuli, item, version)
                    for i in range(SAMPLES):
                        r = call_model(spec, prompt=prompt,
                                       system=FRAME_SYSTEM["minimal"],
                                       temperature=1.0, max_tokens=MAX_TOKENS)
                        letter = extract(r["text"])
                        construct = LETTER_TO_CONSTRUCT.get(letter, "unparsed")
                        counts[(key, item_class, version)][construct] += 1
                        fh.write(json.dumps({
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "control": "reversed_option_order",
                            "model_key": key,
                            "item_id": item["item_id"],
                            "item_class": item_class,
                            "version": version,
                            "sample_index": i,
                            "letter": letter,
                            "construct": construct,
                            "response_text": r["text"],
                            "thinking": r["thinking"],
                            "output_tokens": r["output_tokens"],
                        }, ensure_ascii=False) + "\n")
                        fh.flush()
                        n += 1
                        if n % 25 == 0:
                            print(f"  {n}/{total}")

    print("\nPROPORTIONS WITH OPTIONS REVERSED (surface self listed first)\n")
    print(f"{'model':9}{'class':12}{'ver':5}{'true self':>11}{'surface':>10}"
          f"{'neither':>10}")
    print("-" * 57)
    for key in MODELS:
        for item_class in ["moral", "preference"]:
            for version in ["a", "b"]:
                c = counts.get((key, item_class, version))
                if not c:
                    continue
                t = sum(c.values())
                print(f"{key:9}{item_class:12}{version:5}"
                      f"{c['true_self']/t:11.2f}{c['surface']/t:10.2f}"
                      f"{c['neither']/t:10.2f}")
        print()

    print("Compare against the confirmatory run. If Haiku still answers")
    print("surface self on roughly 85% of trials, its response tracks content.")
    print("If the proportion moves with the position, it tracks order.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
