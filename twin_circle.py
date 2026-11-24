"""Is there a circle that traps all twin primes?

In the prime-spiral layout (radius = angle = p), the twin prime conjecture is false exactly when
some circle of radius K contains every twin prime. That is a restatement (finite = bounded).

The arms can decide this for some patterns, never for twin primes:
    (p, p + 2, p + 4): one of the three is divisible by 3, so the only such triple is 3, 5, 7.
        A circle of radius 7 traps them all, provably.
    (p, p + 2): never forced to hit a multiple of any prime q (it uses 2 of q's residues,
        leaving others free), so the arms always leave room; the residues cannot trap twin primes.
        Whether a circle traps them is the twin prime conjecture itself.
Proven: pairs of primes at most 246 apart cannot be trapped by any circle (Zhang 2013,
Maynard-Tao, Polymath). Brun (1919): the twin primes are sparse enough that sum 1/p converges.

Left: twin primes up to --R in the spiral layout; the 3-5-7 triple inside its circle of radius 7.
Right: number of twin pairs up to x against the Hardy-Littlewood prediction
2 C2 * integral_2^x dt / log^2 t, up to --X.

    python twin_circle.py
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

BLUE, ORANGE, GRAY, INK = "#2a78d6", "#eb6834", "#888780", "#3d3d3a"
C2 = 0.6601618158468696


def sieve(n):
    s = np.ones(n + 1, bool)
    s[:2] = False
    for p in range(2, int(n**0.5) + 1):
        if s[p]:
            s[p * p::p] = False
    return s


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=3000)
    ap.add_argument("--X", type=int, default=10**8)
    ap.add_argument("--out", default="output/twin_circle.png")
    a = ap.parse_args()

    s = sieve(a.X + 2)
    tw = np.nonzero(s[:-2] & s[2:])[0]          # smaller members p with p + 2 prime
    tw = tw[tw + 2 <= a.X]
    trip = [p for p in range(2, 10**6) if s[p] and s[p + 2] and s[p + 4]]
    print(f"prime triples (p, p + 2, p + 4) below 10^6: {trip}")
    xs = np.unique(np.round(np.logspace(2, np.log10(a.X), 60)).astype(int))
    counts = np.searchsorted(tw, xs, side="right")
    # integral_2^x dt / log^2 t, computed in u = log t (dt = e^u du) so the grid is fine near t = 2
    u = np.linspace(np.log(2), np.log(a.X), 400001)
    f = np.exp(u) / u**2
    cum = np.concatenate([[0], np.cumsum((f[1:] + f[:-1]) / 2 * np.diff(u))])
    pred = 2 * C2 * np.interp(np.log(xs), u, cum)
    for x, c, p in zip(xs[::10], counts[::10], pred[::10]):
        print(f"x = {x:>11,}: twin pairs {c:>9,}   Hardy-Littlewood {p:>11,.0f}   ratio {c / p:.4f}")
    print(f"x = {xs[-1]:>11,}: twin pairs {counts[-1]:>9,}   Hardy-Littlewood {pred[-1]:>11,.0f}   ratio {counts[-1] / pred[-1]:.4f}")
    brun = np.sum(1 / tw + 1 / (tw + 2))
    print(f"partial Brun sum (1/p + 1/(p+2)) over twin pairs up to {a.X:,}: {brun:.6f} (Brun's constant is about 1.902)")

    fig, axs = plt.subplots(1, 2, figsize=(16, 7.4), dpi=150, gridspec_kw={"width_ratios": [1, 1.15]})
    ax = axs[0]
    P = np.nonzero(s[: a.R + 1])[0].astype(float)
    T = tw[tw + 2 <= a.R].astype(float)
    ax.scatter(P * np.cos(P), P * np.sin(P), s=2, color="#d3d1c7", linewidths=0, label="primes")
    for v, col, lab in [(T, BLUE, "smaller twin p"), (T + 2, ORANGE, "larger twin p + 2")]:
        ax.scatter(v * np.cos(v), v * np.sin(v), s=7, color=col, linewidths=0, label=lab)
    th = np.linspace(0, 2 * np.pi, 400)
    K = T[-1] + 2
    ax.plot(K * np.cos(th), K * np.sin(th), color=INK, lw=0.8, ls="--")
    ax.text(0, -K * 1.06, f"circle through the last twin pair drawn ({int(T[-1])}, {int(T[-1]) + 2}):\nthe next pair always lies outside, as far as anyone has looked",
            ha="center", fontsize=8, color=INK)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.legend(frameon=False, fontsize=8, loc="upper left", markerscale=2.5)
    ax.set_title(f"Twin primes up to {a.R} in the spiral layout (radius = p)", fontsize=10)
    ins = ax.inset_axes([0.76, 0.06, 0.24, 0.24])
    v = np.array([3.0, 5.0, 7.0])
    ins.plot(7 * np.cos(th), 7 * np.sin(th), color=ORANGE, lw=1)
    ins.scatter(v * np.cos(v), v * np.sin(v), color=ORANGE, s=18)
    for x in v:
        ins.annotate(str(int(x)), (x * np.cos(x), x * np.sin(x)), xytext=(3, 3), textcoords="offset points", fontsize=7)
    ins.set_aspect("equal")
    ins.set_xticks([])
    ins.set_yticks([])
    ins.set_title("triples p, p+2, p+4: only 3, 5, 7\n(radius 7 traps them, provably)", fontsize=7)

    ax = axs[1]
    ax.loglog(xs, counts, "o", color=BLUE, ms=4, label="twin pairs up to x (counted)")
    ax.loglog(xs, pred, color=ORANGE, lw=1.4, label="Hardy–Littlewood: 2C₂ ∫ dt / log²t")
    ax.set_xlabel("x (the radius of the circle)")
    ax.set_ylabel("twin prime pairs inside the circle")
    ax.set_title(f"No circle has trapped them yet: {counts[-1]:,} pairs below {a.X:,},\n"
                 f"ratio to the Hardy–Littlewood prediction {counts[-1] / pred[-1]:.4f}", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
