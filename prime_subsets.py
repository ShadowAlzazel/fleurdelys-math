"""Which subsets of primes hear the zeros, and how strongly?

For a set A of primes, the wave P_A(t) = -sum_{p in A} (log p) p^(-1/2) (1 - log p/log X) cos(t log p)
peaks at the zero heights when A is all primes. "Line strength" = the mean of P_A at the zeros
(12 < gamma < 100) in units of P_A's standard deviation. Each set is compared with random sets of
primes that have the same count in every range [2^j, 2^(j+1)).

Observed (X = 2,000,000): twin, cousin and sexy primes hear the zeros MORE strongly than matched
random primes; isolated primes hear them with the opposite sign. Heuristic reading (not proven):
the zeros encode where primes are locally denser; pairs are denser there by roughly the square,
isolated primes rarer. So this is about clustering of primes, not about twin primes alone.

    python prime_subsets.py              # about 3 minutes
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

from collatz_polar import primes_upto
from zeros import load
from zeta_spectroscopy import line_strength, prime_wave

BLUE, ORANGE, GRAY = "#2a78d6", "#eb6834", "#888780"

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--X", type=int, default=2_000_000)
    ap.add_argument("--draws", type=int, default=5)
    ap.add_argument("--out", default="output/prime_subsets.png")
    a = ap.parse_args()

    P = primes_upto(a.X + 10)
    S = set(P.tolist())
    P = P[P <= a.X]
    ts = np.arange(0.5, 100, 0.01)
    gz = load(10000)
    gz = gz[(gz > 12) & (gz < 100)]

    def strength(A):
        A = np.asarray(A, float)
        return line_strength(ts, prime_wave(ts, A, np.log(A) / np.sqrt(A), a.X), gz)

    def control(A, seed):
        r = np.random.default_rng(seed)
        out = []
        for j in range(1, int(np.log2(a.X)) + 2):
            lo, hi = 2**j, 2 ** (j + 1)
            k = np.sum((A >= lo) & (A < hi))
            if k:
                out.append(r.choice(P[(P >= lo) & (P < hi)], size=k, replace=False))
        return np.concatenate(out)

    sets = {
        "all primes": P,
        "twin (p ± 2 prime)": np.array([p for p in P if p + 2 in S or p - 2 in S]),
        "cousin (p ± 4 prime)": np.array([p for p in P if p + 4 in S or p - 4 in S]),
        "sexy (p ± 6 prime)": np.array([p for p in P if p + 6 in S or p - 6 in S]),
        "isolated (no prime within 6)": np.array([p for p in P if not any((p + d in S) or (p - d in S) for d in (2, 4, 6))]),
    }
    rows = []
    for name, A in sets.items():
        s = strength(A)
        if name == "all primes":
            rows.append((name, len(A), s, np.nan, np.nan))
        else:
            c = np.array([strength(control(A, 200 + k)) for k in range(a.draws)])
            rows.append((name, len(A), s, c.mean(), c.std()))
        n, k, s, m, sd = rows[-1]
        print(f"{n:30s} {k:6d} primes: strength {s:+.2f}" + ("" if np.isnan(m) else f"   matched random {m:+.2f} ± {sd:.2f}   difference {(s - m) / sd:+.1f} sd"))

    fig, ax = plt.subplots(figsize=(10, 4.6), dpi=150)
    for i, (n, k, s, m, sd) in enumerate(rows):
        y = len(rows) - 1 - i
        if not np.isnan(m):
            ax.errorbar(m, y, xerr=2 * sd, fmt="o", color=GRAY, mfc="white", ms=7, capsize=4, lw=1.2)
        ax.plot(s, y, "o", color=ORANGE if "isolated" in n else BLUE, ms=8)
        ax.text(s, y + 0.22, f"{s:+.2f}", ha="center", fontsize=8)
    ax.axvline(0, color=GRAY, lw=0.6)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([f"{n}  ({k:,})" for n, k, *_ in rows][::-1], fontsize=9)
    ax.set_xlabel("line strength at the zeros (mean of the wave at the zeros, in standard deviations)")
    ax.set_title(f"Which primes hear the zeros? Filled: the subset. Open with bars: matched random primes, ±2 sd ({a.draws} draws)",
                 fontsize=10)
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
