"""Apply the coding scheme to every explanation.

    python src/code_explanations.py

Reads data/processed/nbk_study1.csv, sends each explanation to a coding model
with the scheme, and writes one JSON line per response to
data/raw/codes_auto.jsonl. Resumable: completed call_ids are skipped.

**The coding model is not one of the models under study.** Using a model to
code its own output would confound the coding with the thing being measured.
claude-sonnet-4-5 is used here; it appears nowhere in the confirmatory design.

**This is assistance, not authority.** A blind human coding of a stratified
sample is compared against this output and agreement reported. Where the two
diverge, the divergence is the result, not an error to be corrected in favour
of either.

The coding prompt supplies the scheme's definitions but no anchor examples
drawn from the confirmatory data, so that the coder is not primed toward the
patterns already observed.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from models import ModelSpec, call_model

CODER = ModelSpec("coder", "anthropic", "claude-sonnet-4-5", "anthropic")

CODES = {
    "MORAL_VALENCE": "Appeals to the moral quality of the behaviour as the reason for the attribution: the change is good, therefore it reflects the true self, or bad, therefore it does not.",
    "REFLECTIVE": "Appeals to deliberation, considered judgement, moral reasoning, or the agent's endorsed beliefs as against their impulses.",
    "EMOTIONAL": "Appeals to urges, cravings, impulses or feelings as more revealing of the true self than considered belief.",
    "META_DESIRE": "Appeals to whether the agent endorses or wishes to be rid of their own motivation; what the agent wants to want.",
    "ESSENTIALISM": "Appeals to a fixed underlying nature, core or essence treated as independent of and prior to conduct, which behaviour either expresses or fails to express.",
    "PERSON_POSITIVITY": "Appeals to a general disposition to view people favourably, independent of any claim about essences.",
    "ATTITUDE_NOT_SELF": "Explicitly separates the agent's general attitudes from a deeper self, allowing that both can be attributed at once.",
    "ANTI_CONDITIONING": "Appeals to resisting social pressure, acting against one's environment, or holding a view independently of one's surroundings. The true self is what is not merely socially inherited.",
    "CONSISTENCY": "Appeals to the agent's prior pattern, track record or history as evidence about their real character. Continuity with one's own past, as distinct from independence from one's surroundings.",
    "TRIVIALITY": "Declines to attribute on the grounds that the domain is too superficial to bear on the true self at all.",
    "AUTHENTICITY_BARE": "Asserts that the behaviour is or is not genuinely the agent's own, without giving any criterion for that judgement.",
    "GROWTH": "Treats change as constitutive of the self rather than as evidence of something prior: the self is made through change, not revealed by it.",
    "UNCLEAR": "No criterion identifiable, or the response is too brief to code.",
}

SYSTEM = """You are coding explanations from a study on true-self attribution.

You will be shown one explanation. Assign every code that applies. Coding is multi-label: an explanation may invoke more than one criterion, and frequently does.

Rules.

Code what is said, not what is implied. An explanation accompanying a high rating for a morally good change is not coded MORAL_VALENCE unless the explanation itself appeals to the goodness of the behaviour.

Code the reasoning offered, not whether it is correct or consistent.

Where no criterion is identifiable, assign UNCLEAR and nothing else.

Reply with a JSON object and nothing else, of exactly this form:
{"codes": ["CODE_ONE", "CODE_TWO"]}"""


def build_prompt(explanation: str) -> str:
    definitions = "\n\n".join(f"{name}\n{desc}" for name, desc in CODES.items())
    return (
        f"Codes and their definitions:\n\n{definitions}\n\n"
        f"---\n\nExplanation to code:\n\n{explanation}"
    )


_JSON = re.compile(r"\{.*\}", re.DOTALL)
_write_lock = threading.Lock()


def parse_codes(text: str) -> tuple[list[str], str]:
    match = _JSON.search(re.sub(r"```(?:json)?", "", text))
    if not match:
        return [], "no_json"
    try:
        obj = json.loads(match.group(0))
    except json.JSONDecodeError:
        return [], "bad_json"
    codes = obj.get("codes")
    if not isinstance(codes, list):
        return [], "no_codes"
    valid = [c for c in codes if c in CODES]
    unknown = [c for c in codes if c not in CODES]
    return valid, "ok" if not unknown else f"unknown:{','.join(unknown)}"


def completed(path: Path) -> set[str]:
    if not path.exists():
        return set()
    done = set()
    for line in path.open(encoding="utf-8"):
        line = line.strip()
        if line:
            try:
                done.add(json.loads(line)["call_id"])
            except (json.JSONDecodeError, KeyError):
                pass
    return done


def code_one(row: dict) -> dict:
    r = call_model(
        CODER,
        prompt=build_prompt(row["explanation"]),
        system=SYSTEM,
        temperature=0.0,
        max_tokens=300,
    )
    codes, status = parse_codes(r["text"])
    return {
        "call_id": row["call_id"],
        "model_key": row["model_key"],
        "item_id": row["item_id"],
        "item_class": row["item_class"],
        "version": row["version"],
        "measure": row["measure"],
        "frame": row["frame"],
        "rating": row["rating"],
        "choice": row["choice"],
        "codes": codes,
        "code_status": status,
        "coder_raw": r["text"],
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--processed", default="data/processed/nbk_study1.csv")
    ap.add_argument("--out", default="data/raw/codes_auto.jsonl")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--limit", type=int, default=0,
                    help="code only the first N (for testing)")
    args = ap.parse_args(argv)

    rows = [r for r in csv.DictReader(open(args.processed, encoding="utf-8"))
            if r["parse_status"] in ("ok", "ok_word") and r["explanation"].strip()]
    if args.limit:
        rows = rows[:args.limit]

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    done = completed(out_path)
    todo = [r for r in rows if r["call_id"] not in done]

    print(f"{len(rows)} explanations, {len(done)} already coded, {len(todo)} to do")
    if not todo:
        print("nothing to do")
        return 0

    failures = 0
    with out_path.open("a", encoding="utf-8") as fh:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(code_one, r): r["call_id"] for r in todo}
            for n, fut in enumerate(as_completed(futures), start=1):
                try:
                    rec = fut.result()
                except Exception as exc:
                    failures += 1
                    print(f"  failed: {type(exc).__name__}: {exc}", file=sys.stderr)
                    continue
                with _write_lock:
                    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    fh.flush()
                if n % 100 == 0 or n == len(todo):
                    print(f"  {n}/{len(todo)}")

    print(f"\ndone. {len(todo) - failures} coded, {failures} failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
