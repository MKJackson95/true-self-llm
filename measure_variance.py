"""How much does a rating actually vary across repeated calls?

Twenty draws from one cell (one item, one version, one model, one frame) at
temperature 1.0. Repeated across three models and both directions of change.

This is the quantity a power calculation needs and the smoke test could not
supply, having taken only one draw per cell.
"""

import sys
from collections import Counter
from statistics import mean, stdev

sys.path.insert(0, "src")
from models import get_model, call_model
from prompts import load_stimuli, build_presentations
from parse import extract_rating

N = 20
ITEM = "nbk_s1_minorities"

stimuli = load_stimuli("stimuli/nbk_study1.json")
presentations = [
    p for p in build_presentations(stimuli, measures=("rating",), frames=("minimal",))
    if p.item_id == ITEM
]

print(f"{N} draws per cell, item {ITEM}, temperature 1.0\n")
print(f"{'model':8}{'version':9}{'mean':>7}{'sd':>7}{'min':>5}{'max':>5}  distribution")
print("-" * 72)

for key in ["haiku", "sonnet", "opus"]:
    spec = get_model(key)
    for p in sorted(presentations, key=lambda x: x.version):
        values = []
        for _ in range(N):
            r = call_model(spec, prompt=p.prompt, system=p.system,
                           temperature=1.0, max_tokens=600)
            rating, _, status = extract_rating(r["text"])
            if status.startswith("ok"):
                values.append(rating)
        if not values:
            print(f"{key:8}{p.version:9}  no parseable responses")
            continue
        counts = Counter(values)
        dist = " ".join(f"{v}:{counts[v]}" for v in sorted(counts))
        sd = stdev(values) if len(values) > 1 else 0.0
        print(f"{key:8}{p.version:9}{mean(values):7.2f}{sd:7.2f}"
              f"{min(values):5}{max(values):5}  {dist}")
