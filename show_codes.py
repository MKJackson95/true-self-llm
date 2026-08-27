import json
from collections import Counter, defaultdict

rows = [json.loads(l) for l in open("data/raw/codes_auto.jsonl", encoding="utf-8")]
print(f"{len(rows)} coded\n")

overall = Counter()
for r in rows:
    overall.update(r["codes"])

print("CODE FREQUENCY overall (proportion of responses)\n")
for code, n in overall.most_common():
    print(f"  {code:20}{n:6}{n/len(rows):8.2f}")

print(f"\nmean codes per response: {sum(len(r['codes']) for r in rows)/len(rows):.2f}")

print("\n\nBY MODEL (proportion of that model's responses)\n")
by = defaultdict(Counter)
tot = Counter()
for r in rows:
    by[r["model_key"]].update(r["codes"])
    tot[r["model_key"]] += 1

codes = [c for c, _ in overall.most_common(8)]
print(f"{'code':20}" + "".join(f"{m:>9}" for m in ["haiku","sonnet","opus","sol","grok"]))
print("-" * (20 + 9*5))
for c in codes:
    row = "".join(f"{by[m][c]/tot[m]:9.2f}" for m in ["haiku","sonnet","opus","sol","grok"])
    print(f"{c:20}{row}")

print("\n\nBY VERSION, moral items only\n")
mv = defaultdict(Counter); mt = Counter()
for r in rows:
    if r["item_class"] == "moral":
        mv[r["version"]].update(r["codes"]); mt[r["version"]] += 1
print(f"{'code':20}{'ver a':>9}{'ver b':>9}")
print("-" * 38)
for c in codes:
    print(f"{c:20}{mv['a'][c]/mt['a']:9.2f}{mv['b'][c]/mt['b']:9.2f}")
