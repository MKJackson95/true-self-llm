"""Power simulation for the replication design.

    python src/simulate_power.py

No API calls. Simulates the design under parameters estimated from the
variance measurement (measure_variance.py) and reports power for each
comparison at a range of item counts and samples per cell.

The question this answers is not "how many samples do I need to detect the
valence effect". The variance measurement settled that: within-cell standard
deviations of 0.0 to 0.73 against a valence difference of 2.5 to 5.9 points
give effect sizes so large that three samples per cell would suffice.

The question is how many *items* are needed for the comparisons that depend on
between-item variation — model against model, moral against non-moral, one
frame against another. Those are governed by item count, not by samples per
cell, and twelve items is a small number for a model with random intercepts by
item.

Parameters below are taken from the measured data where possible and stated as
assumptions where not. Assumptions are conservative: a smaller effect and more
between-item variation than observed.
"""

from __future__ import annotations

import numpy as np
from scipy import stats

RNG = np.random.default_rng(20260826)
N_SIMS = 2000
ALPHA = 0.05

# --- Measured from measure_variance.py (item nbk_s1_minorities, 20 draws) ---
# Within-cell SD by model: haiku 0.73/0.37, sonnet 0.67/0.37, opus 0.31/0.00.
WITHIN_SD = 0.60          # upper end of the observed range

# Version a minus version b, by model: haiku 2.55, sonnet 5.30, opus 5.90.
VALENCE_EFFECT = 2.50     # the smallest observed, used as the conservative case

# Model means on version a ranged 3.70 to 7.90 on one item. Between-item
# variation was not measured (one item only) and is assumed.
BETWEEN_ITEM_SD = 1.20    # assumption

# Differences of interest for the secondary comparisons.
MODEL_DIFFERENCE = 1.00       # difference in valence effect between two models
CLASS_DIFFERENCE = 2.00       # moral items minus non-moral items
FRAME_DIFFERENCE = 0.50       # participant frame minus minimal frame


def simulate_valence(n_items: int, n_samples: int) -> bool:
    """One simulated study; returns whether the valence effect is detected.

    Items get random intercepts. Each item contributes a mean per version,
    averaged over samples. The test is on item-level differences, which is the
    correct unit: repeated samples from one model on one item are not
    independent observations.
    """
    item_intercepts = RNG.normal(0, BETWEEN_ITEM_SD, n_items)
    se = WITHIN_SD / np.sqrt(n_samples)

    a = item_intercepts + VALENCE_EFFECT / 2 + RNG.normal(0, se, n_items)
    b = item_intercepts - VALENCE_EFFECT / 2 + RNG.normal(0, se, n_items)

    _, p = stats.ttest_rel(a, b)
    return p < ALPHA


def simulate_difference(n_items: int, n_samples: int, difference: float,
                        paired: bool) -> bool:
    """Detection of a difference between two conditions or two models.

    paired=True for comparisons where both levels are measured on the same
    items (frame, model). paired=False for comparisons between different sets
    of items (moral against non-moral).
    """
    se = WITHIN_SD / np.sqrt(n_samples)

    if paired:
        item_intercepts = RNG.normal(0, BETWEEN_ITEM_SD, n_items)
        x = item_intercepts + difference + RNG.normal(0, se, n_items)
        y = item_intercepts + RNG.normal(0, se, n_items)
        _, p = stats.ttest_rel(x, y)
    else:
        n_a = n_items
        n_b = max(2, n_items // 2)   # non-moral set is smaller
        x = RNG.normal(difference, np.sqrt(BETWEEN_ITEM_SD**2 + se**2), n_a)
        y = RNG.normal(0, np.sqrt(BETWEEN_ITEM_SD**2 + se**2), n_b)
        _, p = stats.ttest_ind(x, y)

    return p < ALPHA


def power(fn, *args) -> float:
    return sum(fn(*args) for _ in range(N_SIMS)) / N_SIMS


def main() -> int:
    print(f"{N_SIMS} simulations per cell, alpha = {ALPHA}\n")
    print("Parameters")
    print(f"  within-cell SD           {WITHIN_SD:.2f}   (measured, upper end)")
    print(f"  valence effect           {VALENCE_EFFECT:.2f}   (measured, smallest)")
    print(f"  between-item SD          {BETWEEN_ITEM_SD:.2f}   (assumed)")
    print(f"  model difference         {MODEL_DIFFERENCE:.2f}   (assumed)")
    print(f"  item class difference    {CLASS_DIFFERENCE:.2f}   (assumed)")
    print(f"  frame difference         {FRAME_DIFFERENCE:.2f}   (assumed)")

    item_counts = [8, 12, 16, 24, 32, 48]
    sample_counts = [3, 5, 8]

    print("\n\nPrimary: valence effect (version a vs version b)")
    print(f"{'items':>7}" + "".join(f"{f'n={s}':>9}" for s in sample_counts))
    print("-" * (7 + 9 * len(sample_counts)))
    for n_items in item_counts:
        row = "".join(f"{power(simulate_valence, n_items, s):9.3f}"
                      for s in sample_counts)
        print(f"{n_items:>7}{row}")

    comparisons = [
        ("Model against model (paired by item)", MODEL_DIFFERENCE, True),
        ("Frame against frame (paired by item)", FRAME_DIFFERENCE, True),
        ("Moral against non-moral (unpaired)", CLASS_DIFFERENCE, False),
    ]

    for label, difference, paired in comparisons:
        print(f"\n\nSecondary: {label}, difference = {difference}")
        print(f"{'items':>7}" + "".join(f"{f'n={s}':>9}" for s in sample_counts))
        print("-" * (7 + 9 * len(sample_counts)))
        for n_items in item_counts:
            row = "".join(
                f"{power(simulate_difference, n_items, s, difference, paired):9.3f}"
                for s in sample_counts
            )
            print(f"{n_items:>7}{row}")

    print("\n\nRead the rows, not the columns: power is driven by item count.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
