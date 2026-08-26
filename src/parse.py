"""Convert raw responses into a tidy CSV for analysis.

    python src/parse.py --raw data/raw/nbk_study1.jsonl \
        --out data/processed/nbk_study1.csv

The raw file is the evidence and is never modified. This produces a derived
table; if the extraction rules turn out to be wrong, the data is re-parsed
rather than re-collected.

Extraction is deliberately conservative. Anything that does not match a clear
pattern is left blank and given a status, rather than guessed at. The status
counts printed at the end are part of the result: a model that frequently
fails to produce a usable answer has told you something.

Patterns the smoke test showed are needed:

  markdown emphasis     **2** and **1** wrap the rating in asterisks
  leading rating        every observed response opens with the answer
  forced-choice letter  (a), a), a., or a bare a at the start
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

FIELDS = [
    "call_id",
    "timestamp",
    "model_key",
    "model_id",
    "family",
    "item_id",
    "item_class",
    "domain",
    "name",
    "version",
    "measure",
    "frame",
    "temperature",
    "sample_index",
    "thinking",
    "rating",
    "choice",
    "explanation",
    "parse_status",
    "input_tokens",
    "output_tokens",
    "stop_reason",
]

# An optional label some models put before the answer, e.g. "Rating: 7".
# Kept to a short closed list rather than anything-before-a-colon, so that a
# sentence happening to contain a number is not mistaken for an answer.
_LABEL = re.compile(
    r"^\s*(rating|answer|score|response)\s*[:\-–—]\s*", re.IGNORECASE
)

# A rating: optional markdown emphasis, one or two digits, at the start.
_RATING = re.compile(r"^\W{0,4}(\d{1,2})\b")

# A forced-choice letter: (a) / a) / a. / a: / bare a, at the start.
_CHOICE = re.compile(r"^\W{0,4}\(?([abc])\)?[\.\):\s]", re.IGNORECASE)

# Words some models use instead of a digit.
_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9,
}

_REFUSAL = re.compile(
    r"\b(i can'?t|i cannot|i'?m not able|i won'?t|as an ai|i don'?t feel comfortable)\b",
    re.IGNORECASE,
)


def strip_emphasis(text: str) -> str:
    return re.sub(r"[*_`]+", "", text).strip()


def extract_rating(text: str, scale_max: int = 9):
    """Return (rating, explanation, status)."""
    if not text or not text.strip():
        return None, "", "empty"

    clean = _LABEL.sub("", strip_emphasis(text))

    if _REFUSAL.search(clean[:200]):
        return None, clean, "refusal"

    match = _RATING.match(clean)
    if not match:
        first_word = clean.split()[0].lower().strip(".,:;") if clean.split() else ""
        if first_word in _WORDS:
            value = _WORDS[first_word]
            explanation = clean[len(first_word):].lstrip(" .,:;-–—")
            return value, explanation, "ok_word"
        return None, clean, "no_rating"

    value = int(match.group(1))
    explanation = clean[match.end():].lstrip(" .,:;-–—")
    if not 1 <= value <= scale_max:
        return None, clean, "out_of_range"
    return value, explanation, "ok"


def extract_choice(text: str):
    """Return (choice_letter, explanation, status)."""
    if not text or not text.strip():
        return None, "", "empty"

    clean = _LABEL.sub("", strip_emphasis(text))

    if _REFUSAL.search(clean[:200]):
        return None, clean, "refusal"

    match = _CHOICE.match(clean)
    if not match:
        return None, clean, "no_choice"

    letter = match.group(1).lower()
    explanation = clean[match.end():].lstrip(" .,:;-–—")
    return letter, explanation, "ok"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--raw", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--scale-max", type=int, default=9)
    args = ap.parse_args(argv)

    raw_path, out_path = Path(args.raw), Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    counts: dict[tuple[str, str], int] = {}
    rows = 0

    with raw_path.open(encoding="utf-8") as src, \
            out_path.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()

        for line in src:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            text = rec.get("response_text", "")

            if rec["measure"] == "rating":
                rating, explanation, status = extract_rating(text, args.scale_max)
                choice = ""
            else:
                choice, explanation, status = extract_choice(text)
                rating = None
                choice = choice or ""

            counts[(rec["measure"], status)] = counts.get((rec["measure"], status), 0) + 1

            row = dict(rec)
            row.update({
                "rating": rating if rating is not None else "",
                "choice": choice,
                "explanation": explanation,
                "parse_status": status,
            })
            writer.writerow(row)
            rows += 1

    print(f"{rows} rows written to {out_path}\n")
    print(f"{'measure':15}{'status':15}{'n':>6}")
    print("-" * 36)
    for (measure, status), n in sorted(counts.items()):
        print(f"{measure:15}{status:15}{n:>6}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
