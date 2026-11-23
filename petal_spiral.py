"""Primes, twin primes, petals and twin petals in the prime-spiral layout.

Every value v (an integer n, or a petal height gamma) is drawn at radius v and
angle v radians. All of them sit on the Archimedean spiral r = theta; the arms
come from sampling it (2*pi is close to 6, 44/7, 710/113).

Columns:
    primes | twin primes (smaller member blue, larger orange)
    | petals (zeros) colored by the gap to the next one | twin petals only
Rows: small scale and large scale.

Twin petals: consecutive zeros whose gap is below --twin times the average spacing
at that height (2 pi / log(gamma / 2 pi)).

    python petal_spiral.py
    python petal_spiral.py --twin 0.4
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

from collatz_polar import primes_upto
from zeros import load

BG, INK = "#0f0f0e", "#c3c2b7"
BLUE, ORANGE, AQUA = "#3987e5", "#d95926", "#bfe3ff"
GAP_CMAP = LinearSegmentedColormap.from_list("gap", ["#1c3d5e", "#3987e5", "#bfe3ff"])


def polar(ax, v, **kw):
    ax.scatter(v * np.cos(v), v * np.sin(v), linewidths=0, **kw)


def normalized_gaps(g):
    return np.diff(g) * np.log(g[:-1] / (2 * np.pi)) / (2 * np.pi)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--small", type=float, default=1500)
    ap.add_argument("--large", type=float, default=10000)
    ap.add_argument("--twin", type=float, default=0.3, help="twin-petal threshold, as a fraction of the average spacing")
    ap.add_argument("--out", default="output/petal_spiral.png")
    a = ap.parse_args()

    P = primes_upto(int(a.large) + 2)
    S = set(P.tolist())
    lesser = np.array([p for p in P if p + 2 in S and p + 2 <= a.large])
    greater = lesser + 2
    g = load(10000)
    g = g[g <= a.large]
    d = normalized_gaps(g)
    tw = np.nonzero(d < a.twin)[0]
    twin_petals = np.unique(np.concatenate([g[tw], g[tw + 1]]))

    big = lesser[lesser > 11]
    for m in [6, 44]:
        arms_p = set((P[P > 11] % m).tolist())
        arms_l, arms_g = set((big % m).tolist()), set(((big + 2) % m).tolist())
        print(f"mod {m}: primes use {len(arms_p)} arms; smaller twins {len(arms_l)} (avoid {sorted(arms_p - arms_l)}); "
              f"larger twins {len(arms_g)} (avoid {sorted(arms_p - arms_g)})")
    print(f"{len(lesser)} twin-prime pairs up to {a.large:g}; {len(tw)} twin-petal pairs (gap < {a.twin} of average) "
          f"among {len(g)} zeros; consecutive normalized gaps correlate {np.corrcoef(d[:-1], d[1:])[0, 1]:+.3f}")

    fig, axs = plt.subplots(2, 4, figsize=(20, 10.6), dpi=150, facecolor=BG)
    for row, R in enumerate([a.small, a.large]):
        s = 4 if row == 0 else 0.6
        sparse = 4 if row == 0 else 2.2  # twin panels have few points; draw them larger
        ax = axs[row, 0]
        polar(ax, P[P <= R].astype(float), s=s, color=AQUA)
        ax.set_title(f"primes ≤ {R:g}", color=INK, fontsize=10)
        ax = axs[row, 1]
        polar(ax, lesser[lesser <= R].astype(float), s=sparse * 1.4, color=BLUE, label="smaller twin p")
        polar(ax, greater[greater <= R].astype(float), s=sparse * 1.4, color=ORANGE, label="larger twin p + 2")
        ax.set_title(f"twin primes ≤ {R:g}", color=INK, fontsize=10)
        if row == 0:
            leg = ax.legend(markerscale=3, frameon=False, loc="lower right", fontsize=8)
            for t in leg.get_texts():
                t.set_color(INK)
        ax = axs[row, 2]
        m = g[:-1] <= R
        ax.scatter(g[:-1][m] * np.cos(g[:-1][m]), g[:-1][m] * np.sin(g[:-1][m]), s=s * 1.6, c=np.clip(d[m], 0, 2),
                   cmap=GAP_CMAP, linewidths=0)
        ax.set_title(f"petals (zeros) ≤ {R:g}, colored by gap to the next\n(dark = close, bright = far)", color=INK, fontsize=10)
        ax = axs[row, 3]
        polar(ax, twin_petals[twin_petals <= R], s=sparse * 2, color=ORANGE)
        ax.set_title(f"twin petals only: gap < {a.twin:g} × average", color=INK, fontsize=10)
        for ax in axs[row]:
            ax.set_facecolor(BG)
            ax.set_aspect("equal")
            ax.set_xlim(-R, R)
            ax.set_ylim(-R, R)
            ax.axis("off")
    fig.suptitle("The prime-spiral layout (radius = angle = value) for primes, twin primes, petals and twin petals",
                 color="#f0efec", fontsize=12, y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.965])
    fig.savefig(a.out, facecolor=BG)
    print("saved", a.out)
