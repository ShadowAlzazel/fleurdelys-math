"""Hilbert-Polya: transform the flower's plane so that "on the line" becomes "on a circle".

The map w = 1 - 1/s (a Moebius map; Li 1997, Bombieri-Lagarias 1999) sends
    the critical line Re s = 1/2  ->  the unit circle |w| = 1,
    the right half (Re s > 1/2)   ->  inside,   the left half -> outside,
and the zero rho = 1/2 + i gamma lands at angle about 1/gamma, so the zeros pile up near w = 1.
RH  <=>  every zero lands ON the circle  <=>  (Li's criterion) every
    lambda_n = sum over zeros [1 - (1 - 1/rho)^n]   is >= 0.
A zero off the line sits inside the circle and its mirror 1 - conj(rho) outside; the outside one
makes (1 - 1/rho)^n grow, so lambda_n eventually turns negative.

This is the eigenvalue picture of Hilbert-Polya: eigenvalues of a unitary matrix lie on a circle.

Panels:
 (a) the w-plane: lines Re s = sigma become circles tangent at w = 1; zeta's zeros on the circle (zoom).
 (b) distance from the circle ||w| - 1| for zeta and Davenport-Heilbronn zeros up to height 200.
 (c) Li coefficients lambda_n for zeta (from 35,673 zeros plus a tail estimate) against the Keiper-Li
     asymptotic, and the growing term of each Davenport-Heilbronn off-line pair.
 (d) eigenvalues of a random unitary matrix (CUE) on a circle, next to 100 consecutive zeros wrapped
     onto a circle after unfolding, and 100 independent random points (Poisson).

    python hilbert_polya.py
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

from petal_ledger import FUNCS, petals
from zeros import load, theta

BLUE, ORANGE, AQUA, GRAY, INK, PURPLE = "#2a78d6", "#eb6834", "#1baf7a", "#888780", "#3d3d3a", "#534AB7"
EULER_GAMMA = 0.5772156649015329
# Davenport-Heilbronn zeros right of the line (mpmath.findroot, |f| < 1e-24)
DH_OFF = np.array([0.8085171825 + 85.69934849j, 0.6508300806 + 114.1633427j,
                   0.5743560505 + 166.4793059j, 0.7242576946 + 176.7024612j])


def li_coefficients(gammas, ns, T):
    """lambda_n from zeros 1/2 + i gamma (gamma <= T, both signs) plus an estimate of the tail beyond T.

    For gamma > T, 1 - w^n ~ n^2/(2 gamma^2) on average, and summing against the zero density
    (1/2pi) log(gamma/2pi) gives the tail n^2 (log(T/2pi) + 1) / (2 pi T)."""
    w = 1 - 1 / (0.5 + 1j * gammas)
    out = []
    for n in ns:
        core = np.sum(2 * np.real(1 - w**n))
        tail = n**2 * (np.log(T / (2 * np.pi)) + 1) / (2 * np.pi * T)
        out.append(core + tail)
    return np.array(out)


def keiper_li(n):
    return n / 2 * (np.log(n) - 1 + EULER_GAMMA - np.log(2 * np.pi))


def cue(N, rng):
    Z = (rng.normal(size=(N, N)) + 1j * rng.normal(size=(N, N))) / np.sqrt(2)
    Q, R = np.linalg.qr(Z)
    Q = Q * (np.diag(R) / np.abs(np.diag(R)))   # Mezzadri's fix: Haar-distributed unitary
    return np.angle(np.linalg.eigvals(Q))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=float, default=30000, help="use zeta zeros up to this height")
    ap.add_argument("--nmax", type=int, default=2000)
    ap.add_argument("--out", default="output/hilbert_polya.png")
    a = ap.parse_args()

    g = load(int(a.T))
    w = 1 - 1 / (0.5 + 1j * g)
    print(f"zeta: {len(g):,} zeros up to {a.T:g}; max ||w| - 1| = {np.abs(np.abs(w) - 1).max():.1e}")
    lam1 = li_coefficients(g, [1], a.T)[0]
    exact1 = 1 + EULER_GAMMA / 2 - 0.5 * np.log(4 * np.pi)
    print(f"lambda_1 = {lam1:.7f}, exact 1 + gamma/2 - log(4 pi)/2 = {exact1:.7f}")
    ns = np.unique(np.round(np.geomspace(1, a.nmax, 120)).astype(int))
    lam = li_coefficients(g, ns, a.T)
    for n in (2, 10, 100, 1000, a.nmax):
        k = np.searchsorted(ns, n)
        if k < len(ns) and ns[k] == n:
            print(f"lambda_{n} = {lam[k]:.4f}   Keiper-Li asymptotic {keiper_li(n):.4f}")
    print(f"all lambda_n > 0 for n in the sample (1..{a.nmax}): {bool(np.all(lam > 0))}")

    # Davenport-Heilbronn: on-line zeros up to 200 and the four off-line ones (with mirrors)
    dh_line = petals(FUNCS["Davenport–Heilbronn"], 200)
    dev_in = np.abs(1 - 1 / DH_OFF) - 1
    dev_out = np.abs(1 - 1 / (1 - np.conj(DH_OFF))) - 1
    for z, di, do in zip(DH_OFF, dev_in, dev_out):
        print(f"DH zero {z.real:.4f} + {z.imag:.4f}i: |w| - 1 = {di:+.3e}, mirror {do:+.3e}; "
              f"approx (2 sigma - 1)/(2 gamma^2) = {(2 * z.real - 1) / (2 * z.imag**2):.3e}")
    # where the outside mirror's term 2(1 + delta)^n overtakes the typical size of lambda_n
    big_n = np.geomspace(10, 1e7, 4000)
    cross = []
    for do in dev_out:
        env = 2 * np.exp(big_n * np.log1p(do))
        k = np.nonzero((env > keiper_li(big_n)) & (big_n > 100))[0]
        cross.append(big_n[k[0]] if k.size else np.nan)
    print("n where each DH pair's growing term passes the Keiper-Li size:", [f"{c:.2e}" for c in cross])

    # unfolded zeros on a circle, CUE, Poisson
    rng = np.random.default_rng(1)
    M = 100
    gg = g[20000:20000 + M + 1]
    u = theta(gg) / np.pi
    ang_zero = 2 * np.pi * (u[:-1] - u[0]) / (u[-1] - u[0])
    ang_cue = cue(M, rng)
    ang_poi = rng.uniform(-np.pi, np.pi, M)

    def min_gap(ang):
        s = np.sort(np.mod(ang, 2 * np.pi))
        d = np.diff(np.concatenate([s, [s[0] + 2 * np.pi]]))
        return d.min() / (2 * np.pi / M), np.mean(d < 0.2 * 2 * np.pi / M)
    for name, ang in [("zeros", ang_zero), ("CUE", ang_cue), ("Poisson", ang_poi)]:
        mg, fr = min_gap(ang)
        print(f"{name:8s} on the circle: smallest gap {mg:.3f} x mean, share of gaps below 0.2 x mean {fr:.0%}")

    fig = plt.figure(figsize=(16, 15), dpi=150)
    gs = fig.add_gridspec(2, 2)

    ax = fig.add_subplot(gs[0, 0])
    tt = np.concatenate([-np.geomspace(1e3, 1e-3, 2000), np.geomspace(1e-3, 1e3, 2000)])
    for sg, col, lw in [(0.0, GRAY, 0.8), (0.3, ORANGE, 1.0), (0.5, BLUE, 2.0), (0.7, AQUA, 1.0), (1.0, GRAY, 0.8)]:
        ww = 1 - 1 / (sg + 1j * tt)
        ax.plot(ww.real, ww.imag, color=col, lw=lw, label=f"Re s = {sg:g}" + ("  (the critical line)" if sg == 0.5 else ""))
    ax.plot(w.real[:200], w.imag[:200], "o", color=PURPLE, ms=3)
    ax.plot([1], [0], "+", color=INK, ms=10)
    ax.set_aspect("equal")
    ax.set_xlim(-2.6, 1.6)
    ax.set_ylim(-2.1, 2.1)
    ax.set_title("(a) The map w = 1 − 1/s. Lines Re s = σ become circles tangent at w = 1:\n"
                 "the critical line is the unit circle, right of it is inside, left of it outside", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    ins = ax.inset_axes([0.6, 0.62, 0.38, 0.36])
    phi = np.linspace(0, 0.08, 200)
    ins.plot(np.cos(phi), np.sin(phi), color=BLUE, lw=1)
    ins.plot(w.real[:12], w.imag[:12], "o", color=PURPLE, ms=4)
    for k in (0, 1, 2, 5):
        ins.annotate(f"{g[k]:.1f}", (w.real[k], w.imag[k]), xytext=(4, 0), textcoords="offset points", fontsize=6)
    ins.set_xlim(0.995, 1.001)
    ins.set_ylim(-0.002, 0.075)
    ins.set_title("zoom at w = 1: zeros at angle ≈ 1/γ", fontsize=7)
    ins.tick_params(labelsize=6)

    ax = fig.add_subplot(gs[0, 1])
    floor = 1e-9
    gz = g[g < 200]
    ax.plot(gz, np.full(gz.size, floor), "|", color=BLUE, ms=12, label=f"ζ: {gz.size} zeros, all on the circle (|w| − 1 = 0)")
    ax.plot(dh_line, np.full(dh_line.size, -floor), "|", color=ORANGE, ms=12,
            label=f"Davenport–Heilbronn: {dh_line.size} zeros on the circle")
    ax.plot(DH_OFF.imag, dev_out, "^", color=ORANGE, ms=9, label="Davenport–Heilbronn mirror zeros: outside")
    ax.plot(DH_OFF.imag, dev_in, "v", color=ORANGE, ms=9, label="Davenport–Heilbronn zeros right of the line: inside")
    for z, do in zip(DH_OFF, dev_out):
        ax.annotate(f"σ = {z.real:.3f}\n{do:.1e}", (z.imag, do), xytext=(0, 10), textcoords="offset points",
                    fontsize=7, ha="center", color=ORANGE)
    ax.axhline(0, color=INK, lw=0.8)
    ax.set_yscale("symlog", linthresh=1e-8)
    ax.set_ylim(-3e-4, 3e-4)
    ax.set_xlabel("height γ")
    ax.set_ylabel("|w| − 1   (0 = on the circle)")
    ax.set_title("(b) Distance from the circle. An off-line zero misses it by only ≈ (2σ − 1)/(2γ²):\n"
                 "the circle squeezes heights together, so the miss is tiny but it is there", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="upper left")

    ax = fig.add_subplot(gs[1, 0])
    ax.plot(ns, lam, "o", color=BLUE, ms=3, label=f"λₙ for ζ from {len(g):,} zeros (+ tail estimate)")
    ax.plot(big_n, keiper_li(big_n), color=BLUE, lw=1, alpha=0.6,
            label="Keiper–Li size (n/2)(log n − 1 + γ − log 2π), all positive under RH")
    for i, (z, do, c) in enumerate(zip(DH_OFF, dev_out, cross)):
        env = 2 * np.exp(big_n * np.log1p(do))
        ax.plot(big_n, env, color=ORANGE, lw=0.9, ls="--")
        ax.plot([c], [keiper_li(c)], "o", color=ORANGE, ms=5)
        ax.annotate(f"γ = {z.imag:.0f}: n ≈ {c:.1e}", (c, keiper_li(c)), xytext=(-8, [8, -14, 8, 10][i]), textcoords="offset points",
                    fontsize=7, ha="right", color=ORANGE)
    ax.plot([], [], color=ORANGE, ls="--", label="Davenport–Heilbronn: size 2(1 + δ)ⁿ of each off-line pair's term")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(1e-2, 1e9)
    ax.set_xlim(1, 1e7)
    ax.set_xlabel("n")
    ax.set_ylabel("λₙ")
    ax.set_title("(c) Li's criterion: RH ⇔ λₙ ≥ 0 for all n. ζ: positive and on the predicted curve.\n"
                 "An off-line zero gives a term that grows exponentially; it wins only for very large n (no slack)",
                 fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="upper left")

    ax = fig.add_subplot(gs[1, 1])
    for r, ang, col, name in [(1.0, ang_poi, GRAY, "independent random points (Poisson)"),
                              (1.35, ang_cue, AQUA, f"eigenvalues of a random {M}×{M} unitary matrix (CUE)"),
                              (1.7, ang_zero, PURPLE, f"{M} consecutive zeros of ζ after #20000, unfolded")]:
        ph = np.linspace(0, 2 * np.pi, 400)
        ax.plot(r * np.cos(ph), r * np.sin(ph), color=col, lw=0.4, alpha=0.6)
        ax.plot(r * np.cos(ang), r * np.sin(ang), "o", color=col, ms=3.5, label=name)
        for x in ang:
            ax.plot([0.93 * r * np.cos(x), r * np.cos(x)], [0.93 * r * np.sin(x), r * np.sin(x)], color=col, lw=0.6)
    ax.set_aspect("equal")
    ax.set_xlim(-2.1, 2.1)
    ax.set_ylim(-2.3, 2.1)
    ax.axis("off")
    ax.set_title("(d) The 'other flower': eigenvalues of a unitary matrix live on a circle and repel.\n"
                 "Zeros (outer) space like them (middle), not like random points (inner, with clumps and gaps)",
                 fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="lower center", ncol=1)
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
