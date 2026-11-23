"""Heights of the zeros of zeta on the critical line (the petal heights), fast.

Uses the Riemann-Siegel formula for the real Hardy Z-function, finds every sign
change on a fine grid, and refines each one by bisection. Results are cached in
output/zeros_<T>.npy. Checked against mpmath.zetazero and mpmath.nzeros.

    python zeros.py --T 10000
"""
import argparse
import os

import numpy as np


def theta(t):
    return t / 2 * np.log(t / (2 * np.pi)) - t / 2 - np.pi / 8 + 1 / (48 * t) + 7 / (5760 * t**3)


def _table(n=4001):
    """C0(p) = psi(p) and C1(p) = -psi'''(p) / (96 pi^2) on a grid, computed with mpmath.
    psi has removable 0/0 points at p = 1/4 and 3/4; mpmath's high precision handles them."""
    import mpmath as mp
    mp.mp.dps = 30
    psi = lambda q: mp.cos(2 * mp.pi * (q * q - q - mp.mpf(1) / 16)) / mp.cos(2 * mp.pi * q)
    P = np.linspace(0, 1, n)
    C0, C1 = [], []
    for q in P:
        q = mp.mpf(q) + mp.mpf("1e-25")          # step off the exact removable points
        C0.append(float(psi(q)))
        C1.append(float(-mp.diff(psi, q, 3) / (96 * mp.pi**2)))
    return P, np.array(C0), np.array(C1)


_P, _C0, _C1 = _table()


def Z(t):
    """Riemann-Siegel Z(t) with the first two correction terms. For t > 10."""
    t = np.atleast_1d(np.asarray(t, float))
    a = np.sqrt(t / (2 * np.pi))
    N = np.floor(a).astype(int)
    p = a - N
    out = np.zeros_like(t)
    th = theta(t)
    for n in range(1, N.max() + 1):
        m = n <= N
        out[m] += 2 / np.sqrt(n) * np.cos(th[m] - t[m] * np.log(n))
    # remainder terms C0(p), C1(p), interpolated from a high-precision table
    C0 = np.interp(p, _P, _C0)
    C1 = np.interp(p, _P, _C1)
    sign = np.where((N - 1) % 2 == 0, 1.0, -1.0)
    out += sign * a ** (-0.5) * (C0 + C1 / a)
    return out


def find_zeros(T, dt=0.005, t0=10.0):
    ts = np.arange(t0, T, dt)
    zs = np.concatenate([Z(ts[i:i + 200000]) for i in range(0, len(ts), 200000)])
    idx = np.nonzero(np.sign(zs[:-1]) != np.sign(zs[1:]))[0]
    lo, hi = ts[idx], ts[idx + 1]
    zlo = zs[idx]
    for _ in range(40):
        mid = (lo + hi) / 2
        zm = Z(mid)
        left = np.sign(zm) == np.sign(zlo)
        lo = np.where(left, mid, lo)
        zlo = np.where(left, zm, zlo)
        hi = np.where(left, hi, mid)
    return (lo + hi) / 2


def find_all(T, t_switch=300.0):
    """mpmath for the first zeros (Riemann-Siegel is weak at small t), Riemann-Siegel above."""
    import mpmath as mp
    low = []
    k = 1
    while True:
        g = float(mp.zetazero(k).imag)
        if g > t_switch:
            break
        low.append(g)
        k += 1
    high = find_zeros(T, t0=t_switch)
    return np.concatenate([low, high])


def load(T):
    path = f"output/zeros_{int(T)}.npy"
    if os.path.exists(path):
        return np.load(path)
    g = find_all(T)
    os.makedirs("output", exist_ok=True)
    np.save(path, g)
    return g


if __name__ == "__main__":
    import mpmath as mp

    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=float, default=10000)
    a = ap.parse_args()
    g = load(a.T)
    n_true = mp.nzeros(a.T)
    print(f"found {len(g)} zeros up to T = {a.T:g}; mpmath.nzeros says {n_true}")
    for k in [1, 2, 100, 1000, len(g) // 2, len(g)]:
        if k <= len(g):
            ref = float(mp.zetazero(k).imag)
            print(f"  zero #{k}: {g[k - 1]:.8f}  mpmath {ref:.8f}  diff {abs(g[k - 1] - ref):.1e}")
