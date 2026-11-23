"""Green-Tao: the primes contain arithmetic progressions of every length.

Left: primes in the prime-spiral layout (radius = angle = p) with three progressions drawn
in order: 7 + 30j (6 terms), 7 + 150j (7 terms), 199 + 210j (10 terms). Each step turns by
d mod 2 pi radians.
Middle: the progression of each length k with the smallest last term (found by search).
Right: the number of k-term progressions of primes up to N, divided by the asymptotic count
that Green, Tao and Ziegler proved,
    C_k * integral da dd / prod_j log(a + j d),
    C_k = prod_{p <= k} (1/p)(p/(p-1))^(k-1) * prod_{p > k} (1 - (k-1)/p)(p/(p-1))^(k-1).
C_3 = 1.32032 is twice the twin-prime constant.

    python green_tao.py
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

from collatz_polar import primes_upto

BLUE, AQUA, ORANGE, GRAY, INK = "#2a78d6", "#1baf7a", "#eb6834", "#b4b2a9", "#3d3d3a"


def Ck(k, pmax=10**6):
    c = 1.0
    for p in primes_upto(pmax).astype(float):
        c *= (1 / p) * (p / (p - 1)) ** (k - 1) if p <= k else (1 - (k - 1) / p) * (p / (p - 1)) ** (k - 1)
    return c


def predicted(k, N, C, n=1400):
    tot = 0.0
    a = np.linspace(2, N, n)
    da = a[1] - a[0]
    for ai in a:
        dmax = (N - ai) / (k - 1)
        if dmax <= 0:
            continue
        d = np.linspace(0, dmax, 400)[1:]
        f = np.ones_like(d)
        for j in range(k):
            f /= np.log(ai + j * d)
        tot += f.sum() * (d[1] - d[0] if d.size > 1 else 0) * da
    return C * tot


def smallest_progressions(kmax, N, isp, P):
    out = {}
    for k in range(3, kmax + 1):
        step = int(np.prod([q for q in [2, 3, 5, 7, 11, 13] if q < k]))
        best = None
        for d in range(step, N // (k - 1) + 1, step):
            a = P[P + (k - 1) * d <= N]
            m = np.ones(a.size, bool)
            for j in range(1, k):
                m &= isp[a + j * d]
            if m.any():
                cand = (int(a[m][0]), d, int(a[m][0] + (k - 1) * d))
                if best is None or cand[2] < best[2]:
                    best = cand
            if best and (k - 1) * d > best[2]:
                break
        out[k] = best
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=200000)
    ap.add_argument("--out", default="output/green_tao.png")
    a = ap.parse_args()

    NN = max(a.N, 400000)
    isp = np.zeros(NN + 1, bool)
    P = primes_upto(NN)
    isp[P] = True
    best = smallest_progressions(12, 400000, isp, P)
    for k, (s, d, last) in best.items():
        print(f"k = {k:2d}: {s} + {d}·j, last term {last}")

    C3, C4 = Ck(3), Ck(4)
    Ns = [5000, 10000, 20000, 50000, 100000, a.N]
    r3, r4 = [], []
    for N in Ns:
        Pn = P[P <= N]
        c3 = c4 = 0
        for i, p in enumerate(Pn):
            d = Pn[i + 1:] - p
            d = d[(d % 2 == 0) & (p + 2 * d <= N)]
            ok3 = isp[p + 2 * d]
            c3 += ok3.sum()
            d4 = d[ok3]
            d4 = d4[p + 3 * d4 <= N]
            c4 += isp[p + 3 * d4].sum()
        r3.append(c3 / predicted(3, N, C3))
        r4.append(c4 / predicted(4, N, C4))
        print(f"N = {N:6d}: 3-term {c3:8d} (ratio {r3[-1]:.3f}), 4-term {c4:7d} (ratio {r4[-1]:.3f})")
    print(f"C3 = {C3:.5f}, C4 = {C4:.5f}")

    fig = plt.figure(figsize=(18, 6.2), dpi=150)
    gs = fig.add_gridspec(1, 3, width_ratios=[1.15, 1, 1])
    ax = fig.add_subplot(gs[0])
    R = 2200
    pr = P[P <= R].astype(float)
    ax.scatter(pr * np.cos(pr), pr * np.sin(pr), s=3, color=GRAY, linewidths=0)
    for (s, d, k), col in [((7, 30, 6), BLUE), ((7, 150, 7), AQUA), ((199, 210, 10), ORANGE)]:
        v = s + d * np.arange(k, dtype=float)
        ax.plot(v * np.cos(v), v * np.sin(v), "-o", color=col, ms=4, lw=1.2,
                label=f"{s} + {d}j, {k} terms (turns {np.mod(d, 2 * np.pi):.2f} rad per step)")
    ax.set_aspect("equal")
    ax.axis("off")
    ax.legend(frameon=False, fontsize=8, loc="lower center", bbox_to_anchor=(0.5, -0.12))
    ax.set_title(f"Prime progressions in the spiral layout (primes ≤ {R} in gray)", fontsize=10)

    ax = fig.add_subplot(gs[1])
    ks = list(best)
    ax.semilogy(ks, [best[k][2] for k in ks], "o-", color=BLUE, ms=6)
    for k in ks:
        s, d, last = best[k]
        ax.annotate(f"{s} + {d}j", (k, last), xytext=(4, -10 if k % 2 else 6), textcoords="offset points", fontsize=7, color=INK)
    ax.set_xlabel("length k")
    ax.set_ylabel("smallest possible last term")
    ax.set_title("The first progression of k primes, for each k\n(Green–Tao: one exists for every k)", fontsize=10)

    ax = fig.add_subplot(gs[2])
    ax.semilogx(Ns, r3, "o-", color=BLUE, label="3-term progressions")
    ax.semilogx(Ns, r4, "o-", color=ORANGE, label="4-term progressions")
    ax.axhline(1, color=GRAY, ls="--", lw=1)
    ax.set_ylim(0.85, 1.03)
    ax.set_xlabel("N")
    ax.set_ylabel("count / proven asymptotic")
    ax.set_title("How many progressions of primes up to N:\nthe ratio to the Green–Tao–Ziegler count creeps toward 1", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
