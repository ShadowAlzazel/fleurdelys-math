"""Fast vectorized Davenport-Heilbronn function (and Dirichlet L-functions mod q) for NumPy arrays.

L(s, chi) = q^(-s) * sum_{a=1}^{q} chi(a) * zeta(s, a/q), with the Hurwitz zeta function
zeta(s, a) computed by Euler-Maclaurin summation (as zeta_fast.py does for zeta). Good for
Re s >= 0 and |Im s| up to about 2 pi N q. Checked against mpmath (python dh_fast.py).
"""
from math import factorial

import numpy as np

_B = [1 / 6, -1 / 30, 1 / 42, -1 / 30, 5 / 66, -691 / 2730, 7 / 6, -3617 / 510]


def hurwitz(s, a, N=200):
    s = np.asarray(s, dtype=complex)
    total = np.zeros_like(s)
    for n in range(N):
        total += np.exp(-s * np.log(n + a))
    x = N + a
    xs = np.exp(-s * np.log(x))
    total += x * xs / (s - 1) + xs / 2
    poch = s.copy()
    for k, b in enumerate(_B, 1):
        total += b / factorial(2 * k) * poch * xs * x ** (-(2 * k - 1))
        poch = poch * (s + 2 * k - 1) * (s + 2 * k)
    return total


def dirichlet_L(s, chi, N=200):
    q = len(chi)
    s = np.asarray(s, dtype=complex)
    out = np.zeros_like(s)
    for a in range(1, q):
        if chi[a] != 0:
            out += chi[a] * hurwitz(s, a / q, N)
    return np.exp(-s * np.log(q)) * out


_R5 = np.sqrt(5)
KAPPA = (np.sqrt(10 - 2 * _R5) - 2) / (_R5 - 1)
CHI = [0, 1, 1j, -1j, -1]
CHIB = [0, 1, -1j, 1j, -1]


def dh(s, N=200):
    return (1 - 1j * KAPPA) / 2 * dirichlet_L(s, CHI, N) + (1 + 1j * KAPPA) / 2 * dirichlet_L(s, CHIB, N)


if __name__ == "__main__":
    import mpmath as mp

    from lookalikes import DH

    for s in [0.5 + 14j, 0.80852 + 85.69935j, 1.05 + 300j, 1.2 + 1400j]:
        fast = complex(dh(np.array([s]))[0])
        ref = complex(DH.value(mp.mpc(s)))
        print(f"s = {s}: fast {fast:.10f}  mpmath {ref:.10f}  difference {abs(fast - ref):.1e}")
