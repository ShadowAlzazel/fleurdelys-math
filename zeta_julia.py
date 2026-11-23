"""Julia copies around the zeta flower.

The flower t -> zeta(1/2 + it) lives in the parameter plane of Newton's method for
zeta(s) - c. Over t in [-200, 200] it passes through three Mandelbrot copies
(centers 0.836 - 0.592i, -0.032 - 0.393i, 1.310 + 0.852i). At t = 24.108 it crosses
the copy centered at c0 = 0.83605 - 0.59158i.

Inside that copy, parameters play the roles of points of the Mandelbrot set:
    c0          (period 2)  <->  c' = 0          (center)
    c_basilica  (period 4)  <->  c' = -1         (basilica)
    c_rabbit    (period 6)  <->  c' = -0.1226 + 0.7449i  (rabbit)
For each, the s-plane of the Newton map around the seed w (a zero of zeta'') shows
a copy of the matching quadratic Julia set (Douady-Hubbard). Black: points trapped
in the cycle through the seed. Colors: points converging to a root of zeta(s) - c.

    python zeta_julia.py
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

from find_centers import g
from newton import SEED, colorize, grid, newton
from zeta_fast import zeta

C0 = 0.83605 - 0.59158j
C_BASILICA = 0.85280 - 0.60410j
C_RABBIT_GUESS = 0.82997 - 0.60830j
T_CROSS = 24.108


def refine(c, p, steps=40):
    c = np.array([c], complex)
    for _ in range(steps):
        h = 1e-7
        gc = g(c, p, SEED)
        c = c - gc / ((g(c + h, p, SEED) - gc) / h)
    return complex(c[0]), float(abs(g(c, p, SEED))[0])


def filled_julia(c, ext, n, iters=300):
    X, Y = np.meshgrid(np.linspace(ext[0], ext[1], n), np.linspace(ext[2], ext[3], n))
    z = X + 1j * Y
    alive = np.ones(z.shape, bool)
    for _ in range(iters):
        z[alive] = z[alive] ** 2 + c
        alive &= np.abs(z) < 4
    return alive


def splane(ax, c, r, n, title):
    ext = [SEED.real - r, SEED.real + r, SEED.imag - r, SEED.imag + r]
    lim, it, st = newton(grid(ext, n, n), c, iters=250)
    ax.imshow(colorize(lim, it, st, n, n), origin="lower", extent=ext, interpolation="nearest")
    ax.plot(SEED.real, SEED.imag, "w+", ms=9)
    ax.set_title(title, fontsize=9)
    return (st == 0).mean()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=480)
    ap.add_argument("--r", type=float, default=0.7, help="radius of the s-plane windows around the seed")
    ap.add_argument("--out", default="output/zeta_julia.png")
    a = ap.parse_args()

    cb, rb = refine(C_BASILICA, 4)
    cr, rr = refine(C_RABBIT_GUESS, 6)
    cstar = complex(zeta(np.array([0.5 + 1j * T_CROSS]))[0])
    A = (cb - C0) / (-1)  # affine chart of the copy: c = C0 + A c'
    print(f"basilica parameter {cb:.6f} (residual {rb:.1e}); rabbit parameter {cr:.6f} (residual {rr:.1e})")
    print(f"flower crossing c* = zeta(1/2 + {T_CROSS}i) = {cstar:.5f}; in the copy's chart c' = {(cstar - C0) / A:.3f} "
          f"(main cardioid: |c'| well inside, so its Julia copy is a disk-like blob)")

    fig, axs = plt.subplots(2, 3, figsize=(16, 10.6), dpi=150)

    ax = axs[0, 0]
    R = 0.035
    ext = [C0.real - R, C0.real + R, C0.imag - R, C0.imag + R]
    lim, it, st = newton(np.full(a.n * a.n, SEED), grid(ext, a.n, a.n), iters=220)
    ax.imshow(colorize(lim, it, st, a.n, a.n), origin="lower", extent=ext, interpolation="nearest")
    t = np.linspace(0, 400, 400000)
    fl = np.concatenate([zeta(0.5 + 1j * t[i:i + 20000], N=max(60, int(t[i] / 4) + 60)) for i in range(0, len(t), 20000)])
    ax.plot(fl.real, fl.imag, color="white", lw=0.8)
    for c, lab in [(C0, "center (c' = 0)"), (cb, "basilica (c' = −1)"), (cr, "rabbit"), (cstar, f"flower, t = {T_CROSS}")]:
        ax.plot(c.real, c.imag, "o", mfc="none", mec="#eb6834", ms=7, mew=1.4)
        ax.annotate(lab, (c.real, c.imag), xytext=(5, 5), textcoords="offset points", color="white", fontsize=8)
    ax.set_xlim(ext[:2])
    ax.set_ylim(ext[2:])
    ax.set_title("Parameter plane: the Mandelbrot copy at 0.836 − 0.592i,\nwith the flower (white, t from 0 to 400) passing through it.\nPetals are circles of radius 1 to 3, so at this scale their arcs look straight", fontsize=9)

    f1 = splane(axs[0, 1], cb, a.r, a.n, f"s-plane at the basilica parameter {cb:.4f}\nblack: trapped in the period-4 cycle of the seed (+)")
    f2 = splane(axs[0, 2], cr, a.r, a.n, f"s-plane at the rabbit parameter {cr:.4f}\nblack: trapped in the period-6 cycle of the seed (+)")
    f3 = splane(axs[1, 0], cstar, a.r, a.n, f"s-plane at the flower point c* = ζ(½ + {T_CROSS}i)\nblack: trapped near the seed; ζ(s) − c* also has the root ½ + {T_CROSS}i")
    print(f"trapped share of the s-windows: basilica {100 * f1:.1f}%, rabbit {100 * f2:.1f}%, flower point {100 * f3:.1f}%")

    for ax, c, title in [(axs[1, 1], -1.0, "the basilica: filled Julia set of z² − 1"),
                         (axs[1, 2], -0.12256 + 0.74486j, "the rabbit: filled Julia set of z² + (−0.1226 + 0.7449i)")]:
        ext = [-1.7, 1.7, -1.7, 1.7]
        K = filled_julia(c, ext, a.n)
        ax.imshow(np.where(K[..., None], 0.0, np.array([0.82, 0.82, 0.80])), origin="lower", extent=ext, interpolation="nearest")
        ax.set_title(title, fontsize=9)

    fig.suptitle("Julia copies around the zeta flower (Newton's method for ζ(s) − c, seed w = −0.35508 + 3.59084i)", fontsize=11)
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
