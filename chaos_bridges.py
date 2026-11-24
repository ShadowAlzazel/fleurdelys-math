"""Escape regions and chaos: the Mandelbrot set, zeta, and the zeros.

1. Mandelbrot escape criterion (proven, one line): if |z_n| > 2 and |z_n| >= |c|, then
   |z_{n+1}| >= |z_n|^2 - |c| >= |z_n| (|z_n| - 1) > |z_n|, and the orbit runs to infinity.
   So the Mandelbrot set lies in |c| <= 2. Checked on random orbits: none ever comes back.
2. Zeta's escape region (proven, the Euler product): for Re s = sigma > 1,
   |zeta(s)| >= prod_p (1 + p^-sigma)^-1 = zeta(2 sigma) / zeta(sigma) > 0, so no zeros there.
   The floor is sharp (Kronecker). Inside the strip 1/2 < sigma < 1 there is no floor: the
   minimum over t goes to 0 (Bohr). The Davenport-Heilbronn function has no Euler product and
   no such floor: it has zeros even with sigma > 1 (if output/dh_right.json exists, they are drawn).
3. Chaos in zeta's own Newton family: the Lyapunov exponent lambda(c) along the real cascade
   (lambda < 0: settles on a cycle; lambda > 0: chaos).
4. Quantum chaos: the spacing between neighbouring zeros follows the random-matrix (GUE) law,
   the signature of a chaotic quantum system without time reversal (Bohigas-Giannoni-Schmit 1984;
   Berry-Keating 1999 propose such a system for zeta). Regular (integrable) systems give Poisson.

    python chaos_bridges.py
"""
import argparse
import json
import os

import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np

from newton import newton_map
from zeros import load, theta
from zeta_fast import zeta

BLUE, ORANGE, AQUA, GRAY, INK = "#2a78d6", "#eb6834", "#1baf7a", "#888780", "#3d3d3a"
W = -3.59577086165086


def mandelbrot(ext, n, iters=200):
    X, Y = np.meshgrid(np.linspace(ext[0], ext[1], n), np.linspace(ext[2], ext[3], n))
    c = X + 1j * Y
    z = np.zeros_like(c)
    alive = np.ones(c.shape, bool)
    for _ in range(iters):
        z[alive] = z[alive] ** 2 + c[alive]
        alive &= np.abs(z) < 2
    return alive


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=float, default=600, help="t range for the minimum of |zeta(sigma + it)|")
    ap.add_argument("--out", default="output/chaos_bridges.png")
    a = ap.parse_args()

    # 1. escape criterion check
    rng = np.random.default_rng(1)
    c = rng.uniform(-2.2, 2.2, 400000) + 1j * rng.uniform(-2.2, 2.2, 400000)
    z = np.zeros_like(c)
    out = np.zeros(c.shape, bool)
    back = 0
    for _ in range(60):
        z = np.where(np.abs(z) < 1e6, z * z + c, z)
        crossed = (np.abs(z) > 2) & (np.abs(z) >= np.abs(c))
        back += int(np.sum(out & ~crossed & (np.abs(z) < 1e6)))
        out |= crossed
    print(f"escape criterion: {out.sum()} of {c.size} random orbits passed radius max(2, |c|); {back} came back")

    # 2. minimum of |zeta| over t, for each sigma
    sig = np.linspace(0.5, 2.5, 41)
    ts = np.arange(1, a.T, 0.02)
    mins = []
    for s in sig:
        v = np.abs(np.concatenate([zeta(s + 1j * ts[i:i + 20000], N=max(60, int(a.T / 4))) for i in range(0, len(ts), 20000)]))
        mins.append(v.min())
    mins = np.array(mins)
    floor = np.array([float(mp.zeta(2 * s) / mp.zeta(s)) if s > 1 else np.nan for s in sig])
    for s, m, f in zip(sig[::8], mins[::8], floor[::8]):
        print(f"sigma = {s:.2f}: min |zeta| over t in [1, {a.T:g}] = {m:.4f}; proven floor {f:.4f}")
    dh = json.load(open("output/dh_right.json")) if os.path.exists("output/dh_right.json") else None

    # 3. Lyapunov exponent along the cascade
    cc = np.linspace(0.01995, 0.02050, 1500) + 0j
    x = np.full(cc.shape, W + 0j)
    for _ in range(2000):
        x = newton_map(x, cc)
    acc = np.zeros(cc.shape)
    for _ in range(3000):
        d = (newton_map(x + 1e-7, cc) - newton_map(x - 1e-7, cc)) / 2e-7
        acc += np.log(np.abs(d) + 1e-300)
        x = newton_map(x, cc)
    lam = acc / 3000
    print(f"Lyapunov exponent along the cascade: {np.mean(lam > 0):.2f} of the window is chaotic (lambda > 0)")

    # 4. nearest-neighbour spacings of the zeros
    g = load(30000)
    g = g[g > 100]
    u = theta(g) / np.pi + 1
    sp = np.diff(u)
    sp = sp / sp.mean()
    print(f"{len(sp)} spacings; share below 0.2: {np.mean(sp < 0.2):.4f} (Poisson {1 - np.exp(-0.2):.4f})")

    fig, axs = plt.subplots(2, 2, figsize=(15, 12), dpi=150)
    ax = axs[0, 0]
    ext = [-2.4, 2.4, -2.4, 2.4]
    M = mandelbrot(ext, 900)
    ax.imshow(np.where(M[..., None], 0.15, 0.96) * np.ones(3), origin="lower", extent=ext, interpolation="nearest")
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(2 * np.cos(th), 2 * np.sin(th), color=ORANGE, lw=1.2)
    for c0, col in [(-0.75 + 0.1j, BLUE), (0.5 + 0.5j, AQUA)]:
        zz, orb = 0j, [0j]
        for _ in range(12):
            zz = zz * zz + c0
            orb.append(zz)
            if abs(zz) > 4:
                break
        orb = np.array(orb)
        ax.plot(orb.real, orb.imag, "-o", color=col, ms=3, lw=0.8)
        k = np.argmax(np.abs(orb) > max(2, abs(c0))) if np.any(np.abs(orb) > 2) else None
        label = f"c = {c0.real:+.2f}{c0.imag:+.2f}i: " + ("bounded" if k is None else f"crosses radius 2 at step {k}, then escapes")
        ax.plot([], [], "-o", color=col, ms=3, label=label)
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.4, 2.4)
    ax.set_aspect("equal")
    ax.set_title(f"Escape criterion: past radius max(2, |c|) an orbit never returns\n"
                 f"({out.sum():,} random orbits crossed it, {back} came back). The set lies inside radius 2", fontsize=10)

    ax = axs[0, 1]
    ax.semilogy(sig, mins, "o-", color=BLUE, ms=4, label=f"min of |ζ(σ + it)| over t in [1, {a.T:g}]")
    ax.semilogy(sig, floor, color=ORANGE, lw=1.6, label="proven floor ζ(2σ)/ζ(σ) for σ > 1 (Euler product)")
    if dh:
        ax.semilogy([d["sigma"] for d in dh["mins"]], [max(d["min"], 1e-6) for d in dh["mins"]], "s", color=INK, ms=6,
                    label="Davenport–Heilbronn: min |f| (no Euler product, no floor)")
        for zr in dh.get("zeros", []):
            ax.axvline(zr[0], color=INK, lw=0.8, ls=":")
            ax.text(zr[0], 2e-4, f" DH zero at\n {zr[0]:.4f} + {zr[1]:.2f}i", fontsize=7, color=INK)
    ax.axvspan(0.5, 1.0, color="#f0efec")
    ax.text(0.53, 3, "critical strip:\nno floor (Bohr)", fontsize=8, color=INK)
    ax.axvline(1, color=GRAY, lw=0.6)
    ax.set_xlabel("σ = Re s")
    ax.set_ylim(1e-4, 10)
    ax.set_title("ζ's escape region: for σ > 1 the Euler product keeps |ζ| above a floor, so no zeros", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="lower right")

    ax = axs[1, 0]
    ax.plot(cc.real, lam, color=BLUE, lw=0.8)
    ax.axhline(0, color=GRAY, lw=0.8)
    ax.fill_between(cc.real, 0, lam, where=lam > 0, color=ORANGE, alpha=0.5, label="λ > 0: chaos")
    ax.invert_xaxis()
    ax.set_ylim(-2.5, 0.5)
    ax.set_xlabel("c (real)")
    ax.set_ylabel("Lyapunov exponent λ")
    ax.set_title("Chaos inside ζ's Newton family: order (λ < 0), the doubling cascade, then chaos (λ > 0)", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="lower left")

    ax = axs[1, 1]
    ax.hist(sp, bins=np.arange(0, 3.5, 0.05), density=True, color=BLUE, alpha=0.8, label=f"zeros 100–30,000 ({len(sp):,} spacings)")
    s = np.linspace(0, 3.5, 400)
    ax.plot(s, 32 / np.pi**2 * s**2 * np.exp(-4 * s**2 / np.pi), color=ORANGE, lw=1.6, label="GUE (chaotic, no time reversal)")
    ax.plot(s, np.pi / 2 * s * np.exp(-np.pi * s**2 / 4), color=AQUA, lw=1.2, ls="--", label="GOE (chaotic, time reversal)")
    ax.plot(s, np.exp(-s), color=GRAY, lw=1.2, ls=":", label="Poisson (regular, integrable)")
    ax.set_xlabel("spacing between neighbouring zeros (mean 1)")
    ax.set_title("Quantum chaos: the zeros space like the energy levels of a chaotic system", fontsize=10)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
