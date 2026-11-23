"""Find the closest pairs of zeta zeros (twin petals) and the Lehmer pair.

Uses mpmath, so it is slower: about 1 minute for 400 zeros.
"""
import argparse
import math

import mpmath as mp

mp.mp.dps = 15


def mean_gap(t):
    return 2 * math.pi / math.log(t / (2 * math.pi))


def petal_reach(a, b, steps=40):
    return max(abs(float(mp.siegelz(a + k * (b - a) / steps))) for k in range(1, steps))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--count", type=int, default=400)
    p.add_argument("--top", type=int, default=5)
    a = p.parse_args()
    g = [float(mp.zetazero(n).imag) for n in range(1, a.count + 1)]
    rows = sorted(((g[i + 1] - g[i]) / mean_gap((g[i] + g[i + 1]) / 2), i + 1) for i in range(len(g) - 1))
    print("zeros        heights                gap     vs mean  petal reach")
    for ratio, i in rows[:a.top]:
        x, y = g[i - 1], g[i]
        print(f"#{i},#{i+1}  {x:.4f} {y:.4f}  {y-x:.4f}  {ratio:.0%}  {petal_reach(x, y):.4f}")
    x, y = float(mp.zetazero(6709).imag), float(mp.zetazero(6710).imag)
    print(f"Lehmer pair #6709,#6710  {x:.4f} {y:.4f}  {y-x:.4f}  {(y-x)/mean_gap(x):.0%}  {petal_reach(x, y):.4f}")
