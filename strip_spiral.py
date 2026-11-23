"""The critical strip in the prime-spiral layout: top view and side view.

Top view: the strip 0 <= sigma <= 1 wrapped onto the spiral. The point sigma + it is
drawn at angle t and radius t + K (sigma - 1/2), so the critical line is the spiral
r = theta itself, the same curve the prime spiral samples at the integers. Colors
show zeta(sigma + it): hue = its direction (arg), dark = small |zeta|. Zeros are the
dark points where all colors meet; every one sits on the middle of the band.
White dots: zeros. Blue ticks: primes at radius p. Orange: twin primes.

Side view: the same strip unrolled (t to the right, sigma up), with Z(t) below it,
the signed petal length, whose sign changes are the petals through the origin.

Putting integers and zero heights on one axis is a choice of layout, not a link:
the real link between them is the spectrum (gamma pairs with log p), see petal_spectrum.py.

    python strip_spiral.py
    python strip_spiral.py --T 60 --K 3
"""
import argparse

import matplotlib.colors as mc
import matplotlib.pyplot as plt
import numpy as np

from collatz_polar import primes_upto
from zeros import load, theta
from zeta_fast import zeta

BLUE, ORANGE = "#3987e5", "#eb6834"


def domain_color(z):
    hue = np.mod(np.angle(z) / (2 * np.pi), 1.0)
    a = np.abs(z)
    val = 0.12 + 0.88 * (1 - np.exp(-1.4 * a))          # dark where zeta is small: zeros are black points
    val *= 0.9 + 0.1 * np.mod(np.log2(a + 1e-300), 1.0)  # faint rings of constant |zeta|
    return mc.hsv_to_rgb(np.stack([hue, np.full(hue.shape, 0.55), val], -1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=float, default=120)
    ap.add_argument("--K", type=float, default=4.0, help="radial width of the strip in the top view (keep below 2 pi)")
    ap.add_argument("--px", type=int, default=1500)
    ap.add_argument("--out", default="output/strip_spiral.png")
    a = ap.parse_args()

    g = load(10000)
    g = g[g <= a.T]
    P = primes_upto(int(a.T) + 2)
    S = set(P.tolist())
    twin = np.array([p for p in P if p + 2 in S or p - 2 in S])
    P = P[P <= a.T]
    twin = twin[twin <= a.T]

    # ---- top view: pixel -> (t, sigma) on the wrapped strip
    R = a.T + a.K
    x = np.linspace(-R, R, a.px)
    X, Y = np.meshgrid(x, x)
    r, th = np.hypot(X, Y), np.arctan2(Y, X)
    k = np.round((r - th) / (2 * np.pi))
    t = th + 2 * np.pi * k
    sig = 0.5 + (r - t) / a.K
    ok = (sig >= 0) & (sig <= 1) & (t > 0.5) & (t <= a.T)
    img = np.full(X.shape + (3,), 0.06)
    s = sig[ok] + 1j * t[ok]
    img[ok] = domain_color(np.concatenate([zeta(s[i:i + 200000]) for i in range(0, s.size, 200000)]))

    fig = plt.figure(figsize=(21, 10.5), dpi=150, facecolor="#0f0f0e")
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 1.25], height_ratios=[1, 1])
    ax = fig.add_subplot(gs[:, 0])
    ax.imshow(img, origin="lower", extent=[-R, R, -R, R], interpolation="nearest")
    ax.scatter(g * np.cos(g), g * np.sin(g), s=14, color="white", edgecolors="black", linewidths=0.4, zorder=3)
    ax.scatter(P * np.cos(P), P * np.sin(P), s=22, marker="o", color=BLUE, edgecolors="black", linewidths=0.5, zorder=3)
    ax.scatter(twin * np.cos(twin), twin * np.sin(twin), s=22, marker="o", color=ORANGE, edgecolors="black", linewidths=0.5, zorder=4)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"Top view: the critical strip wrapped onto the spiral r = θ, t up to {a.T:g}\n"
                 "white dots: zeros (dark points, all on the middle line)   blue dots: primes at radius p   orange: twin primes",
                 color="#c3c2b7", fontsize=10)

    # ---- side view: the strip unrolled
    ax = fig.add_subplot(gs[0, 1])
    tt = np.linspace(0.5, a.T, 3000)
    ss = np.linspace(0, 1, 160)
    TT, SS = np.meshgrid(tt, ss)
    Zs = zeta((SS + 1j * TT).ravel()).reshape(TT.shape)
    ax.imshow(domain_color(Zs), origin="lower", extent=[tt[0], tt[-1], 0, 1], aspect="auto", interpolation="nearest")
    ax.scatter(g, np.full_like(g, 0.5), s=14, color="white", edgecolors="black", linewidths=0.4, zorder=3)
    ax.scatter(P, np.full_like(P, 1.035, dtype=float), s=40, marker="|", color=BLUE, clip_on=False, linewidths=1.4)
    ax.scatter(twin, np.full_like(twin, 1.035, dtype=float), s=40, marker="|", color=ORANGE, clip_on=False, linewidths=1.6)
    ax.axhline(0.5, color="white", lw=0.4, ls=":")
    ax.set_ylim(0, 1)
    ax.set_ylabel("σ", color="#c3c2b7")
    ax.set_title("Side view: the strip unrolled (t to the right). White dots: zeros on σ = ½. "
                 "Ticks above: primes, twin primes orange", color="#c3c2b7", fontsize=10, pad=26)

    ax2 = fig.add_subplot(gs[1, 1], sharex=ax)
    Zt = np.real(zeta(0.5 + 1j * tt) * np.exp(1j * theta(np.maximum(tt, 1.0))))
    ax2.plot(tt, Zt, color="#bfe3ff", lw=0.8)
    ax2.axhline(0, color="#5f5e5a", lw=0.6)
    ax2.scatter(g, np.zeros_like(g), s=14, color="white", edgecolors="black", linewidths=0.4, zorder=3)
    ax2.set_xlabel("t", color="#c3c2b7")
    ax2.set_ylabel("Z(t)", color="#c3c2b7")
    ax2.set_title("Side view of the flower: Z(t), the signed petal length. Each sign change is a petal through the origin",
                  color="#c3c2b7", fontsize=10)
    for axx in (ax, ax2):
        axx.set_facecolor("#0f0f0e")
        axx.tick_params(colors="#c3c2b7")
        for sp in axx.spines.values():
            sp.set_color("#383835")
    ax.set_xlim(0, a.T)
    print(f"t up to {a.T:g}: {len(g)} zeros, {len(P)} primes, {len(twin)} twin primes")
    fig.tight_layout()
    fig.savefig(a.out, facecolor="#0f0f0e")
    print("saved", a.out)
