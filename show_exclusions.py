import json

rows = [json.loads(l) for l in open("data/raw/nbk_study1.jsonl", encoding="utf-8")]

import sys
sys.path.insert(0, "src")
from parse import extract_rating, extract_choice

for r in rows:
    if r["measure"] == "rating":
        _, _, status = extract_rating(r["response_text"])
    else:
        _, _, status = extract_choice(r["response_text"])
    if status not in ("ok", "ok_word"):
        print("=" * 70)
        print(f"{r['model_key']}  {r['item_id']}  version {r['version']}  "
              f"{r['measure']}  {r['frame']} frame  [{status}]")
        print(f"thinking={r['thinking']} out_tokens={r['output_tokens']} "
              f"stop={r['stop_reason']}")
        print("-" * 70)
        print(r["response_text"][:600] if r["response_text"].strip() else "(empty)")
        print()
