import json, sys

path = sys.argv[1] if len(sys.argv) > 1 else "data/raw/smoke.jsonl"
rows = [json.loads(l) for l in open(path, encoding="utf-8")]
rows.sort(key=lambda r: (r["item_id"], r["version"], r["model_key"]))

print(f"{len(rows)} responses\n")
for r in rows:
    text = " ".join(r["response_text"].split())
    print(f"{r['model_key']:7} {r['item_id']:22} {r['version']}  {text[:100]}")
