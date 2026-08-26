"""Run the study and write one JSON line per model response.

    python src/runner.py --stimuli stimuli/nbk_study1.json \
        --out data/raw/nbk_study1.jsonl --models haiku,sol --samples 4

Add --dry-run to see the call count and one example prompt without spending
anything.

Three properties matter more than speed.

**Raw text is preserved.** Each line records the response exactly as returned,
before any parsing. The parsed rating is a convenience derived later; if the
parser turns out to be wrong, the data is re-parsed rather than re-collected.

**Writes are immediate.** Each response is written and flushed as it arrives,
so an interrupted run keeps everything collected up to that point.

**Runs resume.** Every call has a deterministic identifier built from the
model, the presentation and the sample index. On restart the runner reads the
identifiers already in the output file and skips them, so an interrupted run
continues without duplicate calls or wasted spend.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from models import MODELS, ModelError, call_model, get_model
from prompts import build_presentations, load_stimuli, presentation_dict

_write_lock = threading.Lock()


def call_id(model_key: str, p, sample_index: int, temperature: float) -> str:
    """Deterministic identifier for one call, used to skip completed work."""
    payload = "|".join([
        model_key,
        p.item_id,
        p.version,
        p.measure,
        p.frame,
        str(sample_index),
        f"{temperature:.2f}",
    ])
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def completed_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    done = set()
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                done.add(json.loads(line)["call_id"])
            except (json.JSONDecodeError, KeyError):
                continue
    return done


def build_jobs(presentations, model_keys, samples, temperature, done):
    jobs = []
    for p in presentations:
        for key in model_keys:
            for i in range(samples):
                cid = call_id(key, p, i, temperature)
                if cid not in done:
                    jobs.append((cid, key, p, i))
    return jobs


def run_one(cid, model_key, presentation, sample_index, temperature, max_tokens):
    spec = get_model(model_key)
    result = call_model(
        spec,
        prompt=presentation.prompt,
        system=presentation.system,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    record = {
        "call_id": cid,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model_key": spec.key,
        "model_id": spec.model_id,
        "family": spec.family,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "sample_index": sample_index,
        "response_text": result["text"],
        "thinking": result["thinking"],
        "input_tokens": result["input_tokens"],
        "output_tokens": result["output_tokens"],
        "stop_reason": result["stop_reason"],
        "response_id": result["response_id"],
    }
    record.update(presentation_dict(presentation))
    return record


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stimuli", default="stimuli/nbk_study1.json")
    ap.add_argument("--out", default="data/raw/nbk_study1.jsonl")
    ap.add_argument("--models", default=",".join(m.key for m in MODELS))
    ap.add_argument("--samples", type=int, default=8)
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--max-tokens", type=int, default=600)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--measures", default="forced_choice,rating")
    ap.add_argument("--frames", default="minimal,participant")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    stimuli = load_stimuli(args.stimuli)
    measures = tuple(m.strip() for m in args.measures.split(",") if m.strip())
    frames = tuple(f.strip() for f in args.frames.split(",") if f.strip())
    presentations = build_presentations(stimuli, measures=measures, frames=frames)

    model_keys = [k.strip() for k in args.models.split(",") if k.strip()]
    for key in model_keys:
        get_model(key)  # fail early on a bad model key

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    done = completed_ids(out_path)
    jobs = build_jobs(presentations, model_keys, args.samples,
                      args.temperature, done)

    print(f"{len(presentations)} presentations x {len(model_keys)} models "
          f"x {args.samples} samples = {len(presentations) * len(model_keys) * args.samples} calls")
    print(f"{len(done)} already recorded, {len(jobs)} to run")

    if args.dry_run:
        if jobs:
            _, key, p, _ = jobs[0]
            print(f"\n--- example: {key}, {p.item_id}, version {p.version}, "
                  f"{p.measure}, {p.frame} frame ---")
            if p.system:
                print(f"[system] {p.system}\n")
            print(p.prompt)
        return 0

    if not jobs:
        print("nothing to do")
        return 0

    failures = 0
    with out_path.open("a", encoding="utf-8") as fh:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {
                pool.submit(run_one, cid, key, p, i,
                            args.temperature, args.max_tokens): cid
                for cid, key, p, i in jobs
            }
            for n, fut in enumerate(as_completed(futures), start=1):
                try:
                    record = fut.result()
                except ModelError as exc:
                    failures += 1
                    print(f"  failed: {exc}", file=sys.stderr)
                    continue
                with _write_lock:
                    fh.write(json.dumps(record, ensure_ascii=False) + "\n")
                    fh.flush()
                if n % 25 == 0 or n == len(jobs):
                    print(f"  {n}/{len(jobs)}")

    written = len(jobs) - failures
    print(f"\ndone. {written} written, {failures} failed")
    if failures:
        print("Re-run the same command to retry the failures; "
              "completed calls will be skipped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
