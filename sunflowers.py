"""Sunflowers: the same rotation that draws the prime-spiral arms and the Mandelbrot stars.

Point n sits at angle n * (turn) and radius sqrt(n) (Vogel's sunflower model, 1979), so the
points spread evenly. The number of arms you see at a given scale is a denominator of a
fraction close to the turn (its continued-fraction convergents):

    golden angle, 0.381966 of a turn   -> 1/2, 1/3, 2/5, 3/8, 5/13, 8/21, 13/34, 21/55 ...  Fibonacci arms
    1 radian (the prime-spiral layout), 0.159155 of a turn -> 1/6, 7/44, 113/710          6, 44, 710 arms
    step 210 of the prime progression, 0.422535 of a turn  -> 2/5, 3/7, 5/12, 8/19        5, 7, 12, 19 arms

Top row: every point. Bottom row: only the primes, in the same layout.

    python sunflowers.py
"""
import argparse
from fractions import Fraction

import matplotlib.pyplot as plt
import numpy as np

from collatz_polar import primes_upto

BG, INK = "#0f0f0e", "#c3c2b7"
GOLD, BLUE, ORANGE = "#eda100", "#3987e5", "#eb6834"


def convergents(x, n=8):
    out, a, h0, h1, k0, k1 = [], [], 1, 0, 0, 1
    y = x
    for _ in range(n):
        ai = int(np.floor(y))
        h0, h1 = ai * h0 + h1, h0
        k0, k1 = ai * k0 + k1, k0
        out.append(Fraction(h0, k0))
        if y - ai < 1e-12:
            break
        y = 1 / (y - ai)
    return [f for f in out if f.denominator > 1]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=3000)
    ap.add_argument("--out", default="output/sunflowers.png")
    a = ap.parse_args()

    turns = [
        ("golden angle", (3 - np.sqrt(5)) / 2, GOLD),
        ("1 radian (prime-spiral layout)", 1 / (2 * np.pi), BLUE),
        ("step 210 (199 + 210j)", np.mod(210 / (2 * np.pi), 1), ORANGE),
    ]
    n = np.arange(1, a.n + 1)
    P = primes_upto(a.n)
    fig, axs = plt.subplots(2, 3, figsize=(16, 11), dpi=150, facecolor=BG)
    for j, (name, t, col) in enumerate(turns):
        conv = convergents(t, 9)
        print(f"{name}: turn {t:.6f}; convergents {', '.join(str(c) for c in conv[:7])}")
        for i, pts in enumerate([n, P]):
            ax = axs[i, j]
            ang = 2 * np.pi * t * pts
            r = np.sqrt(pts)
            ax.scatter(r * np.cos(ang), r * np.sin(ang), s=(7 if i == 0 else 9) * (1 - 0.5 * r / r.max()) + 1, color=col, linewidths=0)
            ax.set_aspect("equal")
            ax.axis("off")
            ax.set_facecolor(BG)
            what = f"all n ≤ {a.n}" if i == 0 else f"primes ≤ {a.n}"
            arms = ", ".join(str(c.denominator) for c in conv[1:6])
            ax.set_title(f"{name}: {t:.4f} turn, {what}\narm counts at growing scale: {arms}", color=INK, fontsize=10)
    fig.suptitle("Sunflowers: point n at angle n × turn and radius √n. The arms count the denominators of fractions near the turn",
                 color="#f0efec", fontsize=12)
    fig.tight_layout()
    fig.savefig(a.out, facecolor=BG)
    print("saved", a.out)
