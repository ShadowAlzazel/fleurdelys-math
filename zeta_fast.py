"""Fast vectorized Riemann zeta function for NumPy arrays.

Right half-plane: Euler-Maclaurin summation.
Left half-plane: the functional equation.
Accurate to roughly 1e-10 for |Im s| up to a few hundred with the defaults.
Raise N for larger heights (N should exceed |t| / (2*pi)).
"""
from math import factorial

import numpy as np
from scipy.special import loggamma

_B = [1/6, -1/30, 1/42, -1/30, 5/66, -691/2730, 7/6, -3617/510,
      43867/798, -174611/330, 854513/138, -236364091/2730]


def zeta_em(s, N=40):
    """Euler-Maclaurin zeta. Good for Re(s) >= 0."""
    s = np.asarray(s, dtype=complex)
    total = np.zeros_like(s)
    for n in range(1, N):
        total += np.exp(-s * np.log(n))
    Ns = np.exp(-s * np.log(N))
    total += N * Ns / (s - 1) + Ns / 2
    poch = s.copy()
    for k, b in enumerate(_B, 1):
        total += b / factorial(2 * k) * poch * Ns * N ** (-(2 * k - 1))
        poch = poch * (s + 2 * k - 1) * (s + 2 * k)
    return total


def zeta(s, N=40):
    """Zeta on the whole plane (except s = 1)."""
    s = np.atleast_1d(np.asarray(s, dtype=complex))
    out = np.empty_like(s)
    right = s.real >= 0
    out[right] = zeta_em(s[right], N)
    sl = s[~right]
    if sl.size:
        out[~right] = (np.exp(sl * np.log(2) + (sl - 1) * np.log(np.pi) + loggamma(1 - sl))
                       * np.sin(np.pi * sl / 2) * zeta_em(1 - sl, N))
    return out


def zeta_prime(s, h=1e-5, N=40):
    """Derivative of zeta by central difference."""
    s = np.asarray(s, dtype=complex)
    return (zeta(s + h, N) - zeta(s - h, N)) / (2 * h)


if __name__ == "__main__":
    import mpmath as mp
    for p in [0.5 + 14.134725j, -3.3 + 2j, 2 + 30j, -7 + 10j]:
        print(p, abs(zeta(p)[0] - complex(mp.zeta(p))))
