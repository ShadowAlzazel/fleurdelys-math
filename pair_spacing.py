"""Does the spacing between pairs of zeros hear the prime pairs (twin primes and others)?

Zeros are unfolded to mean spacing 1: x = theta(gamma)/pi + 1.

Left: pair correlation R2(u), the density of pairs at distance u, against
    GUE (random-matrix) prediction 1 - (sin(pi u)/(pi u))^2  (Montgomery's conjecture)
    no correlation (Poisson): 1
Right: its Fourier transform, the form factor K(tau) = (1/N) sum_{j,k} w(x_j - x_k) e^{2 pi i tau (x_j - x_k)},
against
    GUE: min(|tau|, 1)
    the "diagonal" part alone (each prime paired with itself): |tau|
The bend at tau = 1 and the plateau after it are where, heuristically, pairs of primes
(p, p + h) with Hardy-Littlewood statistics enter: twin primes are h = 2, and every even h
contributes (Montgomery 1973, Goldston-Montgomery 1987, Bogomolny-Keating 1996).

    python pair_spacing.py                    # zeros up to 30000
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

from zeros import load, theta

BLUE, ORANGE, GRAY, INK = "#2a78d6", "#eb6834", "#888780", "#3d3d3a"

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=float, default=30000)
    ap.add_argument("--s", type=float, default=12.0, help="Gaussian taper width for the form factor (in mean spacings)")
    ap.add_argument("--out", default="output/pair_spacing.png")
    a = ap.parse_args()

    g = load(a.T)
    g = g[g > 100]  # unfolding is cleanest away from the first few zeros
    x = theta(g) / np.pi + 1
    N = len(x)
    L = 4 * a.s
    diffs = []
    for k in range(1, 400):
        d = x[k:] - x[:-k]
        d = d[d < L]
        if d.size == 0:
            break
        diffs.append(d)
    D = np.concatenate(diffs)
    print(f"{N} zeros from 100 to {a.T:g}; {D.size} pairs closer than {L:g} mean spacings")

    # pair correlation
    bw = 0.05
    edges = np.arange(0, 4 + bw, bw)
    h, _ = np.histogram(D, edges)
    R2 = h / (N * bw)
    err = np.sqrt(h) / (N * bw)
    u = (edges[:-1] + edges[1:]) / 2
    gue = 1 - (np.sinc(u)) ** 2
    chi = np.sum(((R2 - gue) / np.maximum(err, 1e-9)) ** 2) / len(u)
    print(f"pair correlation vs GUE: mean |difference| {np.mean(np.abs(R2 - gue)):.4f}, "
          f"chi^2 per bin {chi:.2f} (about 1 means agreement within counting noise)")
    small = D < 0.3
    uu3 = np.linspace(0, 0.3, 3001)
    gue_count = N * np.trapezoid(1 - np.sinc(uu3) ** 2, uu3)
    print(f"pairs closer than 0.3 spacings: {small.sum()}; no correlation would give about {int(0.3 * N)}, GUE about {gue_count:.0f}")

    # form factor via a fine histogram of differences
    fb = np.arange(0, L + 1e-3, 1e-3)
    hd, _ = np.histogram(D, fb)
    dc = (fb[:-1] + fb[1:]) / 2
    w = np.exp(-dc**2 / (2 * a.s**2)) * hd
    tau = np.linspace(0, 3, 601)
    K = 1 + 2 * (np.cos(2 * np.pi * np.outer(tau, dc)) @ w) / N   # diagonal j = k gives the 1
    # subtract the smeared delta at tau = 0 coming from the mean density
    K -= a.s * np.sqrt(2 * np.pi) * np.exp(-2 * np.pi**2 * a.s**2 * tau**2)
    kk = (tau > 0.25) & (tau < 0.85)
    slope = np.polyfit(tau[kk], K[kk], 1)
    plateau = K[(tau > 1.3) & (tau < 2.8)]
    print(f"form factor: slope on [0.25, 0.85] = {slope[0]:.3f} (GUE: 1), plateau on [1.3, 2.8] = {plateau.mean():.3f} "
          f"± {plateau.std():.3f} (GUE: 1; diagonal alone would keep rising to 2.8)")

    fig, axs = plt.subplots(1, 2, figsize=(16, 6), dpi=150)
    ax = axs[0]
    ax.errorbar(u, R2, yerr=err, fmt="o", ms=3, color=BLUE, ecolor="#9fc3ef", label=f"zeros 100–{a.T:g} ({N} zeros)")
    uu = np.linspace(1e-3, 4, 800)
    ax.plot(uu, 1 - np.sinc(uu) ** 2, color=ORANGE, lw=1.5, label="GUE: 1 − (sin πu / πu)²")
    ax.axhline(1, color=GRAY, lw=1, ls="--", label="no correlation (Poisson)")
    ax.set_xlabel("u = distance between two zeros, in mean spacings")
    ax.set_ylabel("pair correlation R₂(u)")
    ax.set_title("Pair spacing: zeros repel at short distance (twin petals are rare)", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="lower right")

    ax = axs[1]
    m = tau > 0.12
    ax.plot(tau[m], K[m], color=BLUE, lw=1.4, label="zeros (measured)")
    ax.plot(tau, np.minimum(tau, 1), color=ORANGE, lw=1.5, label="GUE: min(τ, 1)")
    ax.plot(tau, tau, color=GRAY, lw=1, ls="--", label="each prime with itself only: τ")
    ax.axvline(1, color=INK, lw=0.6, ls=":")
    ax.text(1.04, 0.3, "bend at τ = 1:\nprime pairs (p, p + h),\ntwin primes are h = 2", fontsize=8, color=INK)
    ax.annotate("spike at τ = 1.00: Gram's law\n(zeros sit midway between Gram points)", (1.0, 1.19), xytext=(1.45, 1.62),
                fontsize=8, color=INK, arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.6))
    ax.annotate("spikes at 1.09 and 1.23: real (robust to smoothing),\nnot yet explained; candidate: finite-height\nprime corrections (Bogomolny–Keating)",
                (1.09, 1.48), xytext=(1.45, 1.3), fontsize=8, color=INK, arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.6))
    ax.set_ylim(0, 2)
    ax.set_xlabel("τ (frequency, in units of the mean density)")
    ax.set_ylabel("form factor K(τ)")
    ax.set_title("Its Fourier transform: the plateau after τ = 1 is where prime pairs enter", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
