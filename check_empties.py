import json, collections

rows = [json.loads(l) for l in open("data/raw/precheck.jsonl", encoding="utf-8")]
bad = [r for r in rows if not r["response_text"].strip()]

print(f"{len(bad)} empty responses of {len(rows)}\n")
for r in bad:
    print(f"  {r['model_key']:8} {r['item_id']:22} v{r['version']} "
          f"thinking={r['thinking']} out_tokens={r['output_tokens']} "
          f"stop={r['stop_reason']}")

print("\nstop_reason by model:")
c = collections.Counter((r["model_key"], r["stop_reason"]) for r in rows)
for (model, stop), n in sorted(c.items()):
    print(f"  {model:8} {str(stop):14} {n}")

print("\noutput tokens by model:")
by = collections.defaultdict(list)
for r in rows:
    by[r["model_key"]].append(r["output_tokens"])
for model, vals in sorted(by.items()):
    print(f"  {model:8} min={min(vals):4} max={max(vals):4} "
          f"mean={sum(vals)/len(vals):6.1f}")
