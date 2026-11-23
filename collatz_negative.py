"""Collatz on all integers, negative ones included.

n -> n/2 if n is even, 3n + 1 if n is odd. Every start in [-N, N] is followed until
it lands on a cycle. On the positive side that is always 1 -> 4 -> 2 (checked here;
conjectured in general). On the negative side three cycles appear.

    python collatz_negative.py
    python collatz_negative.py --N 100000
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

CYCLES = {
    "0": (0,),
    "1 → 4 → 2": (1, 4, 2),
    "−1 → −2": (-1, -2),
    "−5 → … (length 5)": (-5, -14, -7, -20, -10),
    "−17 → … (length 18)": (-17, -50, -25, -74, -37, -110, -55, -164, -82,
                            -41, -122, -61, -182, -91, -272, -136, -68, -34),
}
COLORS = ["#888780", "#2a78d6", "#eb6834", "#1baf7a", "#eda100"]


def step(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1


def settle(n, on_cycle):
    """Steps until n first lands on a known cycle, and which cycle."""
    k = 0
    while n not in on_cycle:
        n = step(n)
        k += 1
    return k, on_cycle[n]


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--N", type=int, default=20000)
    p.add_argument("--out", default="output/collatz_negative.png")
    a = p.parse_args()

    on_cycle = {m: i for i, c in enumerate(CYCLES.values()) for m in c}
    ns = np.arange(-a.N, a.N + 1)
    res = np.array([settle(int(n), on_cycle) for n in ns])
    steps, which = res[:, 0], res[:, 1]

    neg = ns < 0
    for i, name in enumerate(CYCLES):
        k = int((which[neg] == i).sum())
        if k:
            print(f"{name:22s} {k:6d} of {neg.sum()} negative starts ({100 * k / neg.sum():.1f}%)")

    fig, ax = plt.subplots(figsize=(12, 5.5), dpi=150)
    for i, name in enumerate(CYCLES):
        m = which == i
        ax.scatter(ns[m], steps[m], s=1.2, color=COLORS[i], label=name, linewidths=0)
    ax.axvline(0, color="gray", lw=0.5)
    ax.set_xlabel("starting number n")
    ax.set_ylabel("steps until it lands on a cycle")
    ax.set_title(f"Collatz 3n + 1 on −{a.N} … {a.N}: positives all reach 1 → 4 → 2, negatives split into three cycles")
    ax.legend(markerscale=8, frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
