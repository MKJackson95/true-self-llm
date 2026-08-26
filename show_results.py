import csv, statistics as st
from collections import defaultdict

rows = [r for r in csv.DictReader(open("data/processed/nbk_study1.csv", encoding="utf-8"))
        if r["parse_status"] in ("ok", "ok_word")]

rat = [r for r in rows if r["measure"] == "rating"]
by = defaultdict(list)
for r in rat:
    by[(r["item_class"], r["model_key"], r["version"])].append(int(r["rating"]))

print("MEAN RATING by item class, model, version\n")
print(f"{'class':12}{'model':9}{'ver a':>8}{'ver b':>8}{'diff':>8}")
print("-" * 45)
for cls in ["moral", "preference"]:
    for m in ["haiku", "sonnet", "opus", "sol", "grok"]:
        a = by.get((cls, m, "a"), [])
        b = by.get((cls, m, "b"), [])
        if a and b:
            print(f"{cls:12}{m:9}{st.mean(a):8.2f}{st.mean(b):8.2f}"
                  f"{st.mean(a)-st.mean(b):+8.2f}")
    print()

fc = [r for r in rows if r["measure"] == "forced_choice"]
ch = defaultdict(lambda: defaultdict(int))
for r in fc:
    ch[(r["item_class"], r["model_key"], r["version"])][r["choice"]] += 1

print("\nFORCED CHOICE: proportion selecting true self (a)\n")
print(f"{'class':12}{'model':9}{'ver a':>8}{'ver b':>8}{'diff':>8}")
print("-" * 45)
for cls in ["moral", "preference"]:
    for m in ["haiku", "sonnet", "opus", "sol", "grok"]:
        pa = ch.get((cls, m, "a"), {})
        pb = ch.get((cls, m, "b"), {})
        if pa and pb:
            fa = pa["a"] / sum(pa.values())
            fb = pb["a"] / sum(pb.values())
            print(f"{cls:12}{m:9}{fa:8.2f}{fb:8.2f}{fa-fb:+8.2f}")
    print()
