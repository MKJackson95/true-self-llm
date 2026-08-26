import csv
from collections import defaultdict

rows = [r for r in csv.DictReader(open("data/processed/nbk_study1.csv", encoding="utf-8"))
        if r["measure"] == "forced_choice" and r["parse_status"] == "ok"]

d = defaultdict(lambda: defaultdict(int))
for r in rows:
    d[(r["model_key"], r["item_class"], r["version"])][r["choice"]] += 1

print(f"{'model':9}{'class':12}{'ver':5}{'true self':>11}{'surface':>10}{'neither':>10}")
print("-" * 57)
for m in ["haiku", "sonnet", "opus", "sol", "grok"]:
    for cls in ["moral", "preference"]:
        for v in ["a", "b"]:
            c = d.get((m, cls, v))
            if not c:
                continue
            n = sum(c.values())
            print(f"{m:9}{cls:12}{v:5}{c['a']/n:11.2f}{c['b']/n:10.2f}{c['c']/n:10.2f}")
    print()
