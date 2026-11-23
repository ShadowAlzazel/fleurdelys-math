"""Draw the zeta flower: the image of the critical line Re(s) = 1/2.

    python flower.py                 # t from -50 to 50 and -1000 to 1000
    python flower.py --T 200         # a single custom range
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

from zeta_fast import zeta_em


def flower_points(T, per_unit=400):
    t = np.linspace(-T, T, int(2 * T * per_unit))
    N = max(60, int(T / 4))  # keep N comfortably above T / (2*pi)
    return zeta_em(0.5 + 1j * t, N=N)


def draw(ax, T):
    v = flower_points(T)
    thin = T > 100
    ax.plot(v.real, v.imag, lw=0.15 if thin else 0.8, alpha=0.35 if thin else 0.9, color="#534AB7")
    ax.plot([0], [0], "o", color="#D85A30", ms=5)
    ax.plot([1], [0], "o", color="#1D9E75", ms=4)
    ax.axhline(0, color="gray", lw=0.4)
    ax.axvline(0, color="gray", lw=0.4)
    ax.set_aspect("equal")
    ax.set_title(f"t from -{T} to {T}")
    if thin:
        ax.set_xlim(-4, 7)
        ax.set_ylim(-5.5, 5.5)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--T", type=float, nargs="*", default=[50, 1000])
    p.add_argument("--out", default="output/flower.png")
    a = p.parse_args()
    fig, axs = plt.subplots(len(a.T), 1, figsize=(6, 6 * len(a.T)), dpi=150, squeeze=False)
    for ax, T in zip(axs[:, 0], a.T):
        draw(ax, T)
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
