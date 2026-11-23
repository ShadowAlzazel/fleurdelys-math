"""Twin cycles next to the integer Collatz cycles, for the complex extension
f(z) = (2 + 7z - (2 + 5z) cos(pi z)) / 4.

Each integer cycle of period p has multiplier lam = 3^k / 2^m. Very close to it,
f^p has a second fixed point (a non-integer "twin" cycle) whose multiplier is
about 2 - lam: f^p(z) - z ~ (lam - 1)u + c u^2 near the integer, which has roots
u = 0 and u = (1 - lam)/c. So stability flips: the attracting positive cycle has a
repelling twin (which bounds its tiny basin), and each repelling negative cycle
has an attracting twin.

    python collatz_twins.py
"""
import mpmath as mp

mp.mp.dps = 40
CYCLES = {"1, 4, 2": (1, 3), "-1, -2": (-1, 2), "-5, ... (5)": (-5, 5), "-17, ... (18)": (-17, 18)}


def f(z):
    return (2 + 7 * z - (2 + 5 * z) * mp.cos(mp.pi * z)) / 4


def fp(z):
    return (7 - 5 * mp.cos(mp.pi * z) + mp.pi * (2 + 5 * z) * mp.sin(mp.pi * z)) / 4


def fpow(z, p):
    for _ in range(p):
        z = f(z)
    return z


def multiplier(z, p):
    m = 1
    for _ in range(p):
        m *= fp(z)
        z = f(z)
    return m


if __name__ == "__main__":
    for name, (n, p) in CYCLES.items():
        lam = multiplier(mp.mpf(n), p)
        c = mp.diff(lambda z: fpow(z, p), n, 2) / 2
        z = mp.findroot(lambda z: fpow(z, p) - z, n + (1 - lam) / c)
        mu = multiplier(z, p)
        print(f"{name:14s} integer multiplier {mp.nstr(lam, 5):>7s} ({'attracting' if lam < 1 else 'repelling'})"
              f" | twin at {mp.nstr(z, 12):>17s}, offset {mp.nstr(z - n, 3):>9s},"
              f" multiplier {mp.nstr(mu, 5)} ({'attracting' if abs(mu) < 1 else 'repelling'}), 2 - lam = {mp.nstr(2 - lam, 5)}")
