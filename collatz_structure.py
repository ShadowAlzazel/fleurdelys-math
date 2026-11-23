"""Where the curves and dashes in the Collatz steps plot come from.

Curves: steps(2n) = steps(n) + 1 (n is even, so its first move halves it). So the
chain n, 2n, 4n, ... climbs one step per doubling: on a linear n-axis that is the
curve y = log2|n| + const. Many such chains side by side make the fans near 0.

Dashes: runs of consecutive numbers with the same step count. Example that always
works, for every integer k (positive or negative):
    8k + 4 -> 4k + 2 -> 2k + 1 -> 6k + 4
    8k + 5 -> 24k + 16 -> 12k + 8 -> 6k + 4
The two orbits merge after 3 steps, so steps(8k + 4) = steps(8k + 5).
In general the first m moves depend only on n mod 2^m (Terras 1976), so the
pattern is the same for negative and positive numbers.

    python collatz_structure.py
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

from collatz_negative import CYCLES, settle

BLUE, ORANGE = "#2a78d6", "#eb6834"

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--N", type=int, default=3000, help="range of the left panel")
    p.add_argument("--stats", type=int, default=200000, help="range for the mod-8 statistics")
    p.add_argument("--out", default="output/collatz_structure.png")
    a = p.parse_args()

    on = {m: i for i, c in enumerate(CYCLES.values()) for m in c}
    M = max(a.N, a.stats) + 2
    st = {n: settle(n, on)[0] for n in range(-M, M + 1)}

    fig, axs = plt.subplots(1, 2, figsize=(14, 5.6), dpi=150, gridspec_kw={"width_ratios": [1.7, 1]})

    ax = axs[0]
    ns = np.arange(-a.N, a.N + 1)
    ys = np.array([st[n] for n in ns])
    ax.scatter(ns, ys, s=2, color="#b4b2a9", linewidths=0, zorder=1)
    for c in [27, 31, 41, 47, 55, -51, -25, -37, -59, -61]:
        chain = [c * 2**j for j in range(20) if abs(c * 2**j) <= a.N]
        ax.plot(chain, [st[n] for n in chain], "-o", ms=2.5, lw=1, color=BLUE if c > 0 else ORANGE, zorder=2)
    ax.axvline(0, color="gray", lw=0.5)
    ax.set_xlabel("starting number n")
    ax.set_ylabel("steps until it lands on a cycle")
    ax.set_title("Doubling chains n, 2n, 4n, …: one more step per doubling → log₂ curves", fontsize=10)

    ax = axs[1]
    rows = []
    for rng in [range(1, a.stats), range(-a.stats, -1)]:
        tot, eq = np.zeros(8), np.zeros(8)
        for n in rng:
            tot[n % 8] += 1
            eq[n % 8] += st[n] == st[n + 1]
        rows.append(100 * eq / tot)
    x = np.arange(8)
    ax.bar(x - 0.2, rows[0], 0.38, color=BLUE, label="positive n")
    ax.bar(x + 0.2, rows[1], 0.38, color=ORANGE, label="negative n")
    ax.set_xticks(x)
    ax.set_xlabel("n mod 8")
    ax.set_ylabel("% of n with steps(n) = steps(n + 1)")
    ax.set_ylim(0, 108)
    ax.text(4, 102, "always", ha="center", fontsize=9)
    ax.set_title("Dashes: 8k + 4 and 8k + 5 always merge after 3 steps", fontsize=10)
    ax.legend(frameon=False, loc="upper left")
    for r, (pos, neg) in enumerate(zip(*rows)):
        print(f"n mod 8 = {r}: positive {pos:5.1f}%  negative {neg:5.1f}%")

    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
