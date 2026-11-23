"""The petals in polar coordinates, like the prime spiral.

Each zero 1/2 + i*gamma of zeta (each petal of the flower) is drawn at radius
gamma and angle gamma, the layout the prime spiral uses for integers.

Panel 1, zero spiral: angle = gamma. Hlawka (1975) proved that a*gamma is
equidistributed mod 1 for every real a != 0, so no arms are expected.

Panel 2, wind the petals by log x: angle = gamma * log x. Landau (1912) proved
    sum_{0 < gamma <= T} x^(i gamma) = -(T / 2pi) * Lambda(x) / sqrt(x) + O(log T),
where Lambda(x) = log p if x is a power of a prime p and 0 otherwise. So for
x = 2 the angles lean toward pi, and for x = 6 they do not.

Panel 3, the spectrum: y(x) = -2pi sqrt(x) * sum w(gamma) cos(gamma log x) / int w.
Landau's formula predicts a spike of height log p at every prime power p^k and
almost nothing elsewhere: the petals know the primes.

    python zero_polar.py            # needs output/zeros_10000.npy (python zeros.py)
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

from zeros import load

BG = "#0f0f0e"
INK = "#c3c2b7"


def prime_powers(xmax):
    out = {}
    for p in range(2, xmax + 1):
        if all(p % q for q in range(2, int(p**0.5) + 1)):
            q = p
            while q <= xmax:
                out[q] = np.log(p)
                q *= p
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=float, default=10000)
    ap.add_argument("--xmax", type=int, default=32)
    ap.add_argument("--out", default="output/zero_polar.png")
    a = ap.parse_args()

    g = load(a.T)
    N = len(g)
    print(f"{N} zeros up to {a.T:g}")

    for x in [2, 3, 4, 6, 10]:
        m = np.mean(np.exp(1j * g * np.log(x)))
        lam = prime_powers(x).get(x, 0.0)
        pred = -(a.T / (2 * np.pi)) * lam / np.sqrt(x) / N
        print(f"x = {x:2d}: mean of e^(i gamma log x) = {m.real:+.4f} {m.imag:+.4f}i   Landau predicts real part {pred:+.4f}")

    fig = plt.figure(figsize=(17, 6.2), dpi=150, facecolor=BG)
    gs = fig.add_gridspec(1, 4, width_ratios=[1, 0.62, 0.62, 1.5])

    ax = fig.add_subplot(gs[0])
    ax.scatter(g * np.cos(g), g * np.sin(g), s=0.6, color="#bfe3ff", linewidths=0)
    ax.set_aspect("equal")
    ax.set_title(f"petal spiral: zero γ at radius γ, angle γ\n({N} zeros up to {a.T:g})", color=INK, fontsize=10)
    ax.axis("off")

    bins = 36
    edges = np.linspace(0, 2 * np.pi, bins + 1)
    for k, (x, col) in enumerate([(2, "#3987e5"), (6, "#c98500")]):
        ax = fig.add_subplot(gs[1 + k], projection="polar")
        ang = np.mod(g * np.log(x), 2 * np.pi)
        h, _ = np.histogram(ang, edges)
        h = h / h.mean()
        ax.bar(edges[:-1], h, width=2 * np.pi / bins, align="edge", color=col, edgecolor=BG, linewidth=1)
        ax.plot(np.linspace(0, 2 * np.pi, 200), np.ones(200), color=INK, lw=0.6, ls="--")
        ax.set_ylim(0, 1.3)
        ax.set_yticks([])
        ax.set_xticks(np.arange(0, 2 * np.pi, np.pi / 2))
        ax.set_xticklabels(["0", "π/2", "π", "3π/2"], color=INK, fontsize=8)
        ax.set_facecolor(BG)
        ax.spines["polar"].set_color("#383835")
        ax.grid(color="#383835")
        tag = "a prime: leans toward π" if x == 2 else "not a prime power: flat"
        ax.set_title(f"angles γ·log {x}\n{tag}", color=INK, fontsize=10, pad=14)

    ax = fig.add_subplot(gs[3])
    tau = a.T / 3
    w = np.exp(-0.5 * (g / tau) ** 2)
    xs = np.exp(np.arange(np.log(1.6), np.log(a.xmax + 0.5), 1e-4))
    y = np.empty_like(xs)
    for i in range(0, len(xs), 2000):
        u = np.log(xs[i:i + 2000])
        y[i:i + 2000] = -2 * np.pi * np.sqrt(xs[i:i + 2000]) * (np.cos(np.outer(u, g)) @ w) / (tau * np.sqrt(np.pi / 2))
    ax.plot(xs, y, color="#bfe3ff", lw=0.6)
    pp = prime_powers(a.xmax)
    ax.scatter(list(pp), list(pp.values()), s=22, facecolors="none", edgecolors="#d95926", linewidths=1, zorder=3,
               label="log p at each prime power p^k (Landau's prediction)")
    for q in pp:
        ax.text(q, pp[q] + 0.18, str(q), color=INK, fontsize=7, ha="center")
    ax.set_facecolor(BG)
    ax.set_xlim(1.6, a.xmax + 0.5)
    ax.set_ylim(-0.8, 4.2)
    ax.set_xlabel("x", color=INK)
    ax.set_title("the petals hear the primes: −2π√x · Σ w(γ) cos(γ log x), normalized", color=INK, fontsize=10)
    ax.tick_params(colors=INK)
    for sp in ax.spines.values():
        sp.set_color("#383835")
    leg = ax.legend(frameon=False, loc="upper right", fontsize=8)
    for t in leg.get_texts():
        t.set_color(INK)
    hits = {q: float(np.interp(q, xs, y)) for q in pp}
    print("spectrum at prime powers (should be about log p):",
          " ".join(f"{q}:{hits[q]:.2f}/{pp[q]:.2f}" for q in list(pp)[:8]))
    off = [float(np.interp(q, xs, y)) for q in [6, 10, 12, 14, 15, 18, 20, 21, 22, 24]]
    print("spectrum at non-prime-powers 6,10,12,...:", " ".join(f"{v:+.2f}" for v in off))

    fig.suptitle("Fleurdelys in the prime-spiral layout: the petal heights γ", color="#f0efec", fontsize=12)
    fig.tight_layout()
    fig.savefig(a.out, facecolor=BG)
    print("saved", a.out)
