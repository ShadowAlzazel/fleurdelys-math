"""Other flowers: the image of the critical line t -> F(1/2 + it) for other functions.

The zeta flower is an "hourglass": petals above and below the real axis, all meeting at 0.
Two things make that shape:
    mirror symmetry: real coefficients give F(conj s) = conj F(s), so t and -t are mirror images;
    petals through 0: each zero on the line is a petal through the origin.
Panels:
    zeta(1/2 + it)                       real coefficients, Euler product
    L(1/2 + it, chi_4)                   real character mod 4, Euler product
    zeta(s) L(s, chi_4) at s = 1/2 + it  the zeta function of the Gaussian integers (Dedekind zeta of Q(i))
    Davenport-Heilbronn f(1/2 + it)      real coefficients but no Euler product; misses petals
    L(1/2 + it, chi) with chi(2) = i     complex character mod 5: no mirror symmetry
    zeta(0.6 + it)                       off the line: an hourglass whose petals never reach 0

    python other_flowers.py
    python other_flowers.py --T 100
"""
import argparse

import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np

from lookalikes import DH

mp.mp.dps = 12
PURPLE, ORANGE, GREEN = "#534AB7", "#D85A30", "#1D9E75"

CHI4 = [0, 1, 0, -1]
CHI5 = [0, 1, 1j, -1j, -1]

FLOWERS = [
    ("ζ(½ + it)", lambda t: mp.zeta(mp.mpc(0.5, t))),
    ("L(½ + it, χ₄), real character mod 4", lambda t: mp.dirichlet(mp.mpc(0.5, t), CHI4)),
    ("ζ·L(χ₄): the Gaussian-integer zeta", lambda t: mp.zeta(mp.mpc(0.5, t)) * mp.dirichlet(mp.mpc(0.5, t), CHI4)),
    ("Davenport–Heilbronn f(½ + it)", lambda t: DH.value(mp.mpc(0.5, t))),
    ("L(½ + it, χ), complex character mod 5", lambda t: mp.dirichlet(mp.mpc(0.5, t), CHI5)),
    ("ζ(0.6 + it), off the line", lambda t: mp.zeta(mp.mpc(0.6, t))),
]


def through_zero(v, tol=0.03):
    a = np.abs(v)
    return int(((a[1:-1] < a[:-2]) & (a[1:-1] < a[2:]) & (a[1:-1] < tol)).sum()), float(a.min())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=float, default=60)
    ap.add_argument("--dt", type=float, default=0.01)
    ap.add_argument("--out", default="output/other_flowers.png")
    a = ap.parse_args()

    ts = np.arange(-a.T, a.T + a.dt / 2, a.dt)
    fig, axs = plt.subplots(2, 3, figsize=(16, 10.6), dpi=150)
    for ax, (name, F) in zip(axs.ravel(), FLOWERS):
        v = np.array([complex(F(t)) for t in ts])
        k, mn = through_zero(v)
        mirror = float(np.max(np.abs(v[::-1] - np.conj(v))))
        ax.plot(v.real, v.imag, color=PURPLE, lw=0.6)
        ax.plot([0], [0], "o", color=ORANGE, ms=5)
        ax.plot([1], [0], "o", color=GREEN, ms=4)
        ax.axhline(0, color="gray", lw=0.4)
        ax.axvline(0, color="gray", lw=0.4)
        ax.set_aspect("equal")
        sym = "mirror-symmetric" if mirror < 1e-6 else "not mirror-symmetric"
        ax.set_title(f"{name}\n{k} passes through 0 for t in ±{a.T:g}; {sym}", fontsize=9.5)
        print(f"{name:42s} passes through 0: {k:3d}   closest approach {mn:.1e}   mirror mismatch {mirror:.1e}")
    fig.suptitle("Other flowers: t ↦ F(σ + it). Orange dot: 0. Green dot: 1", fontsize=12)
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
