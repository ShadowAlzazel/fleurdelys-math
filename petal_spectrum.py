"""The petals hear the primes, extended: the zero spectrum up to x = 100.

    y(x) = -2 pi sqrt(x) * sum_gamma w(gamma) cos(gamma log x) / int w,   w(gamma) = exp(-(gamma/tau)^2 / 2)

Landau's formula (1912) predicts a spike of height log p at every prime power p^k
and about 0 elsewhere. Twin primes (p and p + 2 both prime) are drawn orange,
other primes blue, higher prime powers gray.

Right panel: the measured spike height against log p for every prime power.

    python petal_spectrum.py                       # zeros up to 30000 (python zeros.py --T 30000 first)
    python petal_spectrum.py --xmax 200 --tau 8000
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

from collatz_polar import primes_upto
from zeros import load

BLUE, ORANGE, GRAY, INK = "#2a78d6", "#eb6834", "#888780", "#3d3d3a"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=float, default=30000, help="use zeros up to this height")
    ap.add_argument("--tau", type=float, default=6000, help="Gaussian taper width (larger = sharper spikes, needs more zeros)")
    ap.add_argument("--xmax", type=float, default=100)
    ap.add_argument("--step", type=float, default=6e-5, help="grid step in log x")
    ap.add_argument("--out", default="output/petal_spectrum.png")
    a = ap.parse_args()

    g = load(a.T)
    w = np.exp(-0.5 * (g / a.tau) ** 2)
    norm = a.tau * np.sqrt(np.pi / 2)
    u = np.arange(np.log(1.6), np.log(a.xmax + 0.5), a.step)
    y = np.empty_like(u)
    for i in range(0, len(u), 1500):
        y[i:i + 1500] = np.cos(np.outer(u[i:i + 1500], g)) @ w
    xs = np.exp(u)
    y = -2 * np.pi * np.sqrt(xs) * y / norm

    P = primes_upto(int(a.xmax) + 2)
    S = set(P.tolist())
    twins = {p for p in P if p + 2 in S or p - 2 in S}
    pp = {}
    for p in P:
        q = p
        while q <= a.xmax:
            pp[q] = (p, q == p)
            q *= p

    def at(x):  # spike value: max of y within half a spike width of x
        k = np.searchsorted(xs, x)
        return y[max(k - 3, 0):k + 4].max()

    rows = [(q, p, isp, at(q)) for q, (p, isp) in sorted(pp.items())]
    off = [at(n) for n in range(6, int(a.xmax) + 1) if n not in pp]
    err = np.array([v - np.log(p) for q, p, isp, v in rows])
    print(f"{len(g)} zeros up to {a.T:g}, tau = {a.tau:g}")
    print(f"prime powers up to {a.xmax:g}: {len(rows)}; spike minus log p: mean {err.mean():+.3f}, worst {np.abs(err).max():.3f}")
    print(f"integers that are not prime powers: {len(off)}; largest |y| there {np.max(np.abs(off)):.3f}")

    fig, axs = plt.subplots(1, 2, figsize=(17, 6.2), dpi=150, gridspec_kw={"width_ratios": [2.6, 1]})
    ax = axs[0]
    ax.plot(xs, y, color=INK, lw=0.5)
    for q, p, isp, v in rows:
        col = GRAY if not isp else (ORANGE if p in twins else BLUE)
        ax.plot([q], [np.log(p)], "o", mfc="none", mec=col, ms=5, mew=1.1)
        if isp and p in twins:
            ax.text(q, np.log(p) + 0.12, str(p), color=ORANGE, fontsize=6.5, ha="center")
    ax.plot([], [], "o", mfc="none", mec=ORANGE, label="twin primes (p − 2 or p + 2 also prime)")
    ax.plot([], [], "o", mfc="none", mec=BLUE, label="other primes")
    ax.plot([], [], "o", mfc="none", mec=GRAY, label="prime powers p², p³, …")
    ax.set_xlim(1.6, a.xmax + 0.5)
    ax.set_ylim(-1.2, np.log(a.xmax) + 0.6)
    ax.set_xlabel("x")
    ax.set_ylabel("−2π√x · Σ w(γ) cos(γ log x) / ∫w")
    ax.set_title(f"The petals hear the primes: {len(g)} zeros up to height {a.T:g}. Circles: log p, Landau's prediction",
                 fontsize=10)
    ax.legend(frameon=False, loc="upper left", fontsize=8)

    ax = axs[1]
    for q, p, isp, v in rows:
        col = GRAY if not isp else (ORANGE if p in twins else BLUE)
        ax.plot(np.log(p), v, "o", color=col, ms=5)
    lim = [0, np.log(a.xmax) + 0.3]
    ax.plot(lim, lim, color=GRAY, lw=0.8, ls="--")
    ax.set_xlabel("log p")
    ax.set_ylabel("measured spike height")
    ax.set_title("Every prime power: measured spike vs log p", fontsize=10)
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
