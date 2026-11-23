"""Collatz in polar coordinates, like the prime spiral.

Each integer n is drawn at radius |n| and angle n (radians). In this layout the
primes form spiral arms (6 at small scale, 44 at larger scale, because
2*pi is close to 44/7) and 3Blue1Brown explains why: residue classes mod 6 and
mod 44 become arms, and Dirichlet's theorem spreads the primes evenly over the
arms they are allowed on.

Columns: primes (reference) | positive n colored by steps to reach 1
         | negative n colored by the cycle they fall into.
Rows: small scale (|n| <= 1500) and large scale (|n| <= 40000).

    python collatz_polar.py
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

from collatz_negative import CYCLES, settle

BG = "#0f0f0e"
CYCLE_COLORS = {"−1 → −2": "#3987e5", "−5 → … (length 5)": "#199e70", "−17 → … (length 18)": "#c98500"}
STEPS_CMAP = LinearSegmentedColormap.from_list("steps", ["#1c3d5e", "#3987e5", "#bfe3ff"])


def primes_upto(n):
    s = np.ones(n + 1, bool)
    s[:2] = False
    for p in range(2, int(n**0.5) + 1):
        if s[p]:
            s[p * p::p] = False
    return np.nonzero(s)[0]


def polar(ax, n, **kw):
    ax.scatter(np.abs(n) * np.cos(n), np.abs(n) * np.sin(n), linewidths=0, **kw)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--small", type=int, default=1500)
    p.add_argument("--large", type=int, default=40000)
    p.add_argument("--out", default="output/collatz_polar.png")
    a = p.parse_args()

    on = {m: i for i, c in enumerate(CYCLES.values()) for m in c}
    N = a.large
    pos = np.arange(1, N + 1)
    neg = -np.arange(1, N + 1)
    steps = np.array([settle(int(n), on)[0] for n in pos])
    which = np.array([settle(int(n), on)[1] for n in neg])
    names = list(CYCLES)

    # Is "which cycle" tied to residues the way primes are? Spread of the cycle shares across n mod 6 and mod 44.
    for m in [6, 44]:
        shares = []
        for r in range(m):
            sel = (-neg) % m == r
            shares.append([np.mean(which[sel] == i) for i in (2, 3, 4)])
        shares = 100 * np.array(shares)
        print(f"negatives, cycle share by |n| mod {m}: min/max over classes  "
              + "  ".join(f"{names[i]} {shares[:, j].min():.1f}–{shares[:, j].max():.1f}%" for j, i in enumerate((2, 3, 4))))

    fig, axs = plt.subplots(2, 3, figsize=(16, 11), dpi=150, facecolor=BG)
    pr = primes_upto(N)
    for row, R in enumerate([a.small, a.large]):
        s = 4 if row == 0 else 0.35
        ax = axs[row, 0]
        polar(ax, pr[pr <= R], s=s, color="#bfe3ff")
        ax.set_title(f"primes ≤ {R}", color="#c3c2b7", fontsize=10)
        ax = axs[row, 1]
        m = pos <= R
        polar(ax, pos[m], s=s, c=steps[m], cmap=STEPS_CMAP, vmin=0, vmax=np.percentile(steps[m], 98))
        ax.set_title(f"positive n ≤ {R}, colored by steps to 1 (brighter = more)", color="#c3c2b7", fontsize=10)
        ax = axs[row, 2]
        m = -neg <= R
        for i, name in enumerate(names):
            k = m & (which == i)
            if k.any():
                polar(ax, neg[k], s=s, color=CYCLE_COLORS[name], label=name)
        ax.set_title(f"negative n ≥ −{R}, colored by cycle", color="#c3c2b7", fontsize=10)
        if row == 0:
            leg = ax.legend(markerscale=4, frameon=False, loc="lower right", fontsize=8)
            for t in leg.get_texts():
                t.set_color("#c3c2b7")
        for ax in axs[row]:
            ax.set_facecolor(BG)
            ax.set_aspect("equal")
            ax.set_xlim(-R, R)
            ax.set_ylim(-R, R)
            ax.axis("off")
    fig.suptitle("Integers at radius |n|, angle n radians (the prime-spiral layout)", color="#f0efec", fontsize=12)
    fig.tight_layout()
    fig.savefig(a.out, facecolor=BG)
    print("saved", a.out)
