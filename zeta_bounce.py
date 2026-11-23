"""The flower as a bouncing ball: elasticity, phase, and the pi of colliding blocks.

A bouncing ball has a height y(t) that hits the floor, a phase portrait (y, p), an energy that
drops by e^2 per bounce (e = elasticity). The side view of the flower has the same parts:
    |Z(t)| = |zeta(1/2 + it)| touches 0 at every zero        (the bounces)
    (Z, Z' / theta')                                      (the phase portrait; theta' ~ (1/2) log(t/2pi)
                                                           is the local frequency)
    reach_n = max |Z| between zeros n and n+1              (the bounce heights)
    elasticity e_n = reach_{n+1} / reach_n                  (not constant: it fluctuates)
    phase lag S(t) = N(t) - theta(t)/pi - 1                 (zeros counted minus the clock theta/pi)
Selberg's central limit theorem (1946, proven): log|zeta(1/2 + it)| is approximately normal with
variance (1/2) log log t. That is the law of the bounce heights. At reachable heights the next term
matters; Keating and Snaith's random-matrix model (2000) gives (1/2)(log N + gamma + 1), N = log(t/2pi).

Colliding blocks (Galperin 2003): masses 1 and 100^k, perfectly elastic. In the coordinates
(sqrt(m1) v1, sqrt(m2) v2) energy is a circle, and every collision turns the state by the same
angle 2 * arctan(sqrt(m1/m2)), so the number of collisions is the number of steps that fit in pi:
3, 31, 314, 3141, ... The flower counts the other way: N(T) is about theta(T) / pi, the number of
half-turns (each ~ pi) that fit into the total angle theta(T), off by the phase lag S(T).

    python zeta_bounce.py
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

from zeros import Z, load, theta

BLUE, ORANGE, AQUA, GRAY, INK = "#2a78d6", "#eb6834", "#1baf7a", "#888780", "#3d3d3a"


def theta_prime(t):
    return 0.5 * np.log(t / (2 * np.pi))


def block_collisions(k):
    m1, m2 = 1.0, 100.0**k
    v1, v2, n = 0.0, -1.0, 0
    states = [(np.sqrt(m1) * v1, np.sqrt(m2) * v2)]
    while True:
        if v1 > v2:                       # blocks approach: elastic collision
            u1 = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
            u2 = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
            v1, v2 = u1, u2
        elif v1 < 0:                      # small block hits the wall
            v1 = -v1
        else:
            break
        n += 1
        if k <= 1:
            states.append((np.sqrt(m1) * v1, np.sqrt(m2) * v2))
    return n, np.array(states)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="output/zeta_bounce.png")
    a = ap.parse_args()

    g = load(10000)
    # bounce heights (petal reach) between consecutive zeros
    frac = np.linspace(0.02, 0.98, 25)
    mids = g[:-1, None] + (g[1:] - g[:-1])[:, None] * frac[None, :]
    ok = mids[:, 0] > 12
    reach = np.full(len(g) - 1, np.nan)
    vals = np.abs(Z(mids[ok].ravel())).reshape(-1, len(frac))
    reach[ok] = vals.max(axis=1)
    r = reach[ok]
    e = r[1:] / r[:-1]
    print(f"{len(r)} petals between zeros 12 < t < 10000")
    print(f"elasticity e_n = reach_(n+1)/reach_n: median {np.median(e):.3f}, mean of log e {np.mean(np.log(e)):+.4f}, "
          f"sd of log e {np.std(np.log(e)):.3f}; share of bounces higher than the last: {np.mean(e > 1):.3f}")
    print(f"correlation of consecutive log e: {np.corrcoef(np.log(e[:-1]), np.log(e[1:]))[0, 1]:+.3f}")

    # phase lag S(t)
    ts = np.linspace(20, 10000, 400000)
    N = np.searchsorted(g, ts)
    S = N - theta(ts) / np.pi - 1
    print(f"phase lag S(t), 20 < t < 10000: mean {S.mean():+.4f}, sd {S.std():.3f}, max |S| {np.abs(S).max():.3f}")

    # Selberg's central limit theorem
    rng = np.random.default_rng(0)
    tr = rng.uniform(5000, 10000, 40000)
    L = np.log(np.abs(Z(tr)))
    var_pred = 0.5 * np.log(np.log(7500))
    Nm = np.log(7500 / (2 * np.pi))
    var_rmt = 0.5 * (np.log(Nm) + np.euler_gamma + 1)
    print(f"log|zeta(1/2+it)| at 40000 random t in [5000, 10000]: mean {L.mean():+.3f}, variance {L.var():.3f}; "
          f"Selberg's leading-order variance (1/2) log log t = {var_pred:.3f}; "
          f"Keating-Snaith random-matrix variance (1/2)(log N + gamma + 1), N = log(t/2pi): {var_rmt:.3f}")

    # blocks
    counts = [block_collisions(k)[0] for k in range(6)]
    print("block collisions for mass ratios 1, 100, 100^2, ...:", counts)
    n1, st1 = block_collisions(1)

    fig = plt.figure(figsize=(18, 11.5), dpi=150)
    gs = fig.add_gridspec(2, 3)

    ax = fig.add_subplot(gs[0, 0])
    tt = np.linspace(12, 70, 6000)
    ax.plot(np.abs(Z(tt)), tt, color=BLUE, lw=1)
    gg = g[(g > 12) & (g < 70)]
    ax.plot(np.zeros_like(gg), gg, "o", color=INK, ms=3)
    ax.axvline(0, color=INK, lw=1.2)
    ax.set_xlabel("|Z(t)| = |ζ(½ + it)|  (the height)")
    ax.set_ylabel("t (time runs up)")
    ax.set_title("The side view as a bouncing ball: every zero is a bounce off the floor", fontsize=10)

    ax = fig.add_subplot(gs[0, 1])
    tt = np.linspace(14, 100, 20000)
    z = Z(tt)
    zp = (Z(tt + 1e-4) - Z(tt - 1e-4)) / 2e-4 / theta_prime(tt)
    sc = ax.scatter(z, zp, c=tt, cmap="Blues", s=0.6, linewidths=0)
    ax.axvline(0, color=INK, lw=1)
    ax.axhline(0, color=GRAY, lw=0.5)
    ax.set_aspect("equal")
    ax.set_xlabel("Z(t)")
    ax.set_ylabel("Z′(t) / θ′(t)")
    ax.set_title("Phase portrait (Z, Z′/θ′), t from 14 to 100 (darker = later)\neach loop is one petal; crossing Z = 0 is a zero",
                 fontsize=10)

    ax = fig.add_subplot(gs[0, 2])
    ax.hist(np.log(e), bins=80, color=BLUE, alpha=0.85, density=True)
    ax.axvline(np.log(0.8), color=ORANGE, lw=2)
    ax.text(np.log(0.8), ax.get_ylim()[1] * 0.92, " the ball: e = 0.8\n (always loses energy)", color=ORANGE, fontsize=8)
    ax.axvline(0, color=GRAY, lw=0.8, ls="--")
    ax.set_xlabel("log of the elasticity e_n = reach_(n+1) / reach_n")
    ax.set_title(f"Elasticity of the petals ({len(e):,} bounces up to t = 10,000)\n"
                 f"half go higher, half lower; next bounce anti-correlated", fontsize=10)

    ax = fig.add_subplot(gs[1, 0])
    ax.plot(ts, S, color=BLUE, lw=0.3)
    band = np.sqrt(np.log(np.log(ts)) / (2 * np.pi**2))
    ax.plot(ts, 2 * band, color=ORANGE, lw=1, label="±2 × Selberg's standard deviation √(log log t / 2π²)")
    ax.plot(ts, -2 * band, color=ORANGE, lw=1)
    ax.axhline(0, color=GRAY, lw=0.6)
    ax.set_xlabel("t")
    ax.set_ylabel("S(t) = N(t) − θ(t)/π − 1")
    ax.set_title("Phase lag: zeros counted minus the clock θ/π. It stays near 0 (Turing's method uses this)", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="lower right")

    ax = fig.add_subplot(gs[1, 1])
    ax.hist(L, bins=120, density=True, color=BLUE, alpha=0.85, label="log|ζ(½ + it)|, t random in [5000, 10000]")
    xx = np.linspace(-6, 4, 400)
    ax.plot(xx, np.exp(-xx**2 / (2 * var_pred)) / np.sqrt(2 * np.pi * var_pred), color=ORANGE, lw=1.5,
            label=f"Selberg (leading term): variance ½ log log t = {var_pred:.2f}")
    ax.plot(xx, np.exp(-xx**2 / (2 * var_rmt)) / np.sqrt(2 * np.pi * var_rmt), color=AQUA, lw=1.5, ls="--",
            label=f"Keating–Snaith random matrices: variance ½(log N + γ + 1) = {var_rmt:.2f}")
    ax.set_xlim(-6, 4)
    ax.set_xlabel("log |ζ(½ + it)|")
    ax.set_title("The law of the bounce heights: Selberg's central limit theorem (1946)\n"
                 f"measured variance {L.var():.2f}; the random-matrix correction accounts for the gap", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="upper left")

    ax = fig.add_subplot(gs[1, 2])
    circle = np.exp(1j * np.linspace(0, 2 * np.pi, 400)) * np.sqrt(100.0)
    ax.plot(circle.real, circle.imag, color=GRAY, lw=0.8)
    ax.plot(st1[:, 0], st1[:, 1], "-o", color=AQUA, ms=3, lw=0.8)
    ax.set_aspect("equal")
    ax.set_xlabel("√m₁ · v₁ (small block)")
    ax.set_ylabel("√m₂ · v₂ (big block)")
    ax.set_title(f"Elastic blocks, mass ratio 100: {n1} collisions. Energy is a circle;\n"
                 f"each collision turns by 2·arctan(1/10). Counts for 100^k: {', '.join(map(str, counts))}", fontsize=10)
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
