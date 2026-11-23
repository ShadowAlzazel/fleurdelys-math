"""One seed, pixel = c: the Newton parameter plane for zeta(s) - c.

The seed is a zero of zeta'' (a free critical point). Black pixels are c values
where the seed gets trapped in a cycle: Mandelbrot copies.

    python mandelbrot_copy.py                                   # default copy
    python mandelbrot_copy.py --center 0.83605 -0.59158 --radius 0.03
    python mandelbrot_copy.py --center 1 0 --radius 4           # wide view
"""
import argparse

import numpy as np

from newton import SEED, colorize, grid, newton, save_image

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--center", type=float, nargs=2, default=[-0.43193, 0.46305])
    p.add_argument("--radius", type=float, default=0.02)
    p.add_argument("--size", type=int, default=600)
    p.add_argument("--iters", type=int, default=200)
    p.add_argument("--seed", type=complex, default=SEED)
    p.add_argument("--out", default="output/mandelbrot_copy.png")
    a = p.parse_args()
    cx, cy = a.center
    r = a.radius
    ext = [cx - r, cx + r, cy - r, cy + r]
    W = H = a.size
    C = grid(ext, W, H)
    lim, n, st = newton(np.full(C.shape, a.seed), C, iters=a.iters)
    save_image(colorize(lim, n, st, H, W), a.out, ext, W, H)
    print("saved", a.out, " trapped fraction:", round((st == 0).mean(), 3))
