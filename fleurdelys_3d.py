"""The 3D shape of the flower (Re F, Im F, height t), and the 4D view with sigma.

Top two rows: the curve t -> (Re F(1/2 + it), Im F(1/2 + it), t) for t in [-T, T], seen from the
side, for six functions (as in other_flowers.py). Black dots: where the curve hits the vertical
axis F = 0 (the zeros on the line). Real coefficients make the shape mirror-symmetric top to bottom.
Bottom: the 4D picture for zeta. The fourth coordinate sigma = Re(s) is shown by drawing several
slices sigma = 0.3, 0.5, 0.7 in one 3D view; only sigma = 1/2 touches the axis.

    python fleurdelys_3d.py
    python fleurdelys_3d.py --T 30 --elev 15
"""
import argparse

import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np

from other_flowers import FLOWERS

mp.mp.dps = 12
PURPLE, ORANGE, BLUE, AQUA = "#534AB7", "#eb6834", "#2a78d6", "#1baf7a"


def curve(F, ts):
    return np.array([complex(F(t)) for t in ts])


def axis_hits(ts, v):
    """Passes through 0: a local minimum of |F| where the direction of F flips by about half a turn
    (a near miss at distance d turns much less). Robust to the step size in t."""
    a = np.abs(v)
    flip = np.abs(np.angle(v[2:] / v[:-2]))
    m = (a[1:-1] <= a[:-2]) & (a[1:-1] <= a[2:]) & (flip > 2.5)
    return ts[1:-1][m]


def style(ax, elev, azim, lim):
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlim(-lim, lim + 2)
    ax.set_ylim(-lim - 1, lim + 1)
    ax.set_xlabel("Re F", fontsize=8)
    ax.set_ylabel("Im F", fontsize=8)
    ax.set_zlabel("t", fontsize=8)
    ax.tick_params(labelsize=7)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=float, default=50)
    ap.add_argument("--dt", type=float, default=0.02)
    ap.add_argument("--elev", type=float, default=8)
    ap.add_argument("--azim", type=float, default=-60)
    ap.add_argument("--out", default="output/fleurdelys_3d.png")
    a = ap.parse_args()

    ts = np.arange(-a.T, a.T + a.dt / 2, a.dt)
    fig = plt.figure(figsize=(18, 17), dpi=140)
    for i, (name, F) in enumerate(FLOWERS):
        v = curve(F, ts)
        hits = axis_hits(ts, v)
        ax = fig.add_subplot(3, 3, i + 1, projection="3d")
        ax.plot(v.real, v.imag, ts, color=PURPLE, lw=0.5)
        ax.plot([0, 0], [0, 0], [-a.T, a.T], color="gray", lw=0.8)
        ax.scatter(np.zeros_like(hits), np.zeros_like(hits), hits, color="black", s=8, depthshade=False)
        style(ax, a.elev, a.azim, 3)
        ax.set_title(f"{name}\n{len(hits)} hits of the axis for t in ±{a.T:g}", fontsize=9.5)
        print(f"{name:42s} axis hits: {len(hits)}")

    ax = fig.add_subplot(3, 3, (7, 9), projection="3d")
    for sig, col in [(0.3, AQUA), (0.5, PURPLE), (0.7, ORANGE)]:
        v = curve(lambda t: mp.zeta(mp.mpc(sig, t)), ts)
        hits = axis_hits(ts, v)
        ax.plot(v.real, v.imag, ts, color=col, lw=0.6, label=f"σ = {sig}: {len(hits)} axis hits, closest {np.abs(v).min():.3f}")
        print(f"zeta sigma = {sig}: axis hits {len(hits)}, closest approach {np.abs(v).min():.4f}")
    ax.plot([0, 0], [0, 0], [-a.T, a.T], color="gray", lw=0.8)
    style(ax, a.elev, a.azim, 4)
    ax.set_title("4D: ζ(σ + it) for three values of σ (the fourth coordinate). Only σ = ½ touches the axis", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.suptitle("Fleurdelys in 3D: (Re F, Im F, t) seen from the side", fontsize=13)
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
