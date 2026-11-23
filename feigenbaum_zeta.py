"""Feigenbaum's constant inside zeta's Newton family.

For real c, the Newton map for zeta(s) - c,  N_c(x) = x - (zeta(x) - c) / zeta'(x),  sends real
numbers to real numbers, and w = -3.595771 (a real zero of zeta'') is its free critical point.
So c -> N_c on the real line is a one-parameter family like the logistic map. In the window
c in [0.0199, 0.0205] the orbit of w has period 3, then 6, 12, 24, ...: a period-doubling cascade
(the real slice of a Mandelbrot copy of period 3).

Superstable parameters c_P (w returns to itself after exactly P steps) are found by bisection.
Feigenbaum's universality theorem (Feigenbaum 1978; proved by Lanford 1982) predicts that the
gaps shrink by delta = 4.6692016... at each doubling.

Left: bifurcation diagram (where the orbit of w settles, for each c). Right: the gap ratios.

    python feigenbaum_zeta.py
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

from newton import newton_map

W = -3.59577086165086
DELTA = 4.669201609102990
BLUE, ORANGE, GRAY, INK = "#2a78d6", "#eb6834", "#888780", "#3d3d3a"


def g(c, P):
    """N_c^P(w) - w for an array of real c."""
    x = np.full(np.shape(c), W + 0j)
    cc = np.asarray(c, float) + 0j
    for _ in range(P):
        x = newton_map(x, cc)
    return x.real - W


def superstable(guess, P, width):
    cs = np.linspace(guess - width, guess + width, 4001)
    v = g(cs, P)
    ok = np.isfinite(v[:-1]) & np.isfinite(v[1:]) & (np.abs(v[:-1]) < 0.3) & (np.abs(v[1:]) < 0.3)
    s = np.nonzero(ok & (np.sign(v[:-1]) != np.sign(v[1:])))[0]
    if s.size == 0:
        return None
    i = s[np.argmin(np.abs(cs[s] - guess))]
    a, b = cs[i], cs[i + 1]
    ga = g(np.array([a]), P)[0]
    for _ in range(70):
        m = (a + b) / 2
        gm = g(np.array([m]), P)[0]
        if np.sign(gm) == np.sign(ga):
            a, ga = m, gm
        else:
            b = m
    return (a + b) / 2


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--maxP", type=int, default=384)
    ap.add_argument("--out", default="output/feigenbaum_zeta.png")
    a = ap.parse_args()

    cs = {3: superstable(0.020425947, 3, 2e-5), 6: superstable(0.020159478, 6, 2e-5), 12: superstable(0.020083369, 12, 2e-5)}
    P = 12
    while 2 * P <= a.maxP:
        gap = cs[P // 2] - cs[P]
        r = superstable(cs[P] - gap / DELTA, 2 * P, 0.3 * gap / DELTA)
        if r is None:
            break
        cs[2 * P] = r
        P *= 2
    ks = sorted(cs)
    for k in ks:
        print(f"period {k:4d}: c = {cs[k]:.15f}")
    ratios = [(cs[x] - cs[y]) / (cs[y] - cs[z]) for x, y, z in zip(ks, ks[1:], ks[2:])]
    for (x, y, z), r in zip(zip(ks, ks[1:], ks[2:]), ratios):
        print(f"   gap ratio for periods {x}, {y}, {z}: {r:.6f}")
    print(f"Feigenbaum delta = {DELTA}")

    # bifurcation diagram
    cgrid = np.linspace(0.01995, 0.02050, 2200)
    x = np.full(cgrid.shape, W + 0j)
    for _ in range(2500):
        x = newton_map(x, cgrid + 0j)
    pts = []
    for _ in range(200):
        x = newton_map(x, cgrid + 0j)
        pts.append(x.real.copy())
    pts = np.array(pts)

    fig, axs = plt.subplots(1, 2, figsize=(16, 6.2), dpi=150, gridspec_kw={"width_ratios": [1.6, 1]})
    ax = axs[0]
    for row in pts:
        m = np.abs(row - W) < 1.5
        ax.plot(cgrid[m], row[m], ",", color=INK, alpha=0.5)
    for k in ks[:5]:
        ax.axvline(cs[k], color=ORANGE, lw=0.6, ls=":")
        ax.text(cs[k], W + 1.42, f"{k}", color=ORANGE, fontsize=7, ha="center")
    ax.set_ylim(W - 1.5, W + 1.5)
    ax.set_xlabel("c (real)")
    ax.set_ylabel("where the orbit of w settles (real s)")
    ax.set_title("Bifurcation diagram of Newton's method for ζ(s) − c, seed w = −3.5958 (a zero of ζ″)\n"
                 "orange: superstable parameters of period 3, 6, 12, 24, 48", fontsize=10)
    ax.invert_xaxis()

    ax = axs[1]
    ax.plot(range(1, len(ratios) + 1), ratios, "o-", color=BLUE, ms=6)
    ax.axhline(DELTA, color=GRAY, ls="--", lw=1)
    ax.text(1, DELTA + 0.04, "Feigenbaum δ = 4.6692…", color=GRAY, fontsize=9)
    ax.set_xticks(range(1, len(ratios) + 1))
    ax.set_xticklabels([f"{x}/{y}/{z}" for x, y, z in zip(ks, ks[1:], ks[2:])], fontsize=8)
    ax.set_xlabel("periods used")
    ax.set_ylabel("gap ratio (c_P − c_2P) / (c_2P − c_4P)")
    ax.set_title("The gaps shrink by Feigenbaum's constant", fontsize=10)
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
