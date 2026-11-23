"""Find centers of Mandelbrot copies: values of c where the seed is periodic.

Solves N_c^p(seed) = seed for c, from many random starting guesses.
"""
import argparse

import numpy as np

from newton import SEED, newton_map
from zeta_fast import zeta


def g(c, p, seed):
    s = np.full(c.shape, seed, complex)
    for _ in range(p):
        s = newton_map(s, c)
    return s - seed


def find(p, ext, seed=SEED, guesses=6000, rng_seed=3):
    rng = np.random.default_rng(rng_seed)
    c = rng.uniform(ext[0], ext[1], guesses) + 1j * rng.uniform(ext[2], ext[3], guesses)
    for _ in range(50):
        h = 1e-7
        gc = g(c, p, seed)
        c = c - gc / ((g(c + h, p, seed) - gc) / h)
        c = np.where(np.isfinite(c) & (np.abs(c) < 20), c, np.nan)
    ok = np.isfinite(c)
    cc = np.nan_to_num(c)
    ok &= np.abs(g(cc, p, seed)) < 1e-8
    ok &= np.abs(cc - zeta(np.array([seed]))[0]) > 1e-4  # drop the period-1 center
    for q in range(1, p):  # drop lower periods that divide p
        if p % q == 0:
            ok &= np.abs(g(cc, q, seed)) > 1e-6
    u = np.unique(np.round(cc[ok], 4))
    inside = (u.real > ext[0]) & (u.real < ext[1]) & (u.imag > ext[2]) & (u.imag < ext[3])
    return u[inside]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--period", type=int, default=2)
    ap.add_argument("--ext", type=float, nargs=4, default=[-2.2, 4.2, -2.7, 2.7])
    a = ap.parse_args()
    centers = find(a.period, a.ext)
    print(f"{len(centers)} period-{a.period} centers")
    for c in centers:
        print(f"  {c.real:+.4f} {c.imag:+.4f}i")
