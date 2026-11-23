"""The flower drawn on the Newton parameter plane for zeta(s) - c.

Both live in the same plane: values of zeta.
Black dot: 0. Green star: the critical value zeta(seed).
Orange circles: period-2 Mandelbrot centers. Pink squares: period-3 centers.
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

from find_centers import find
from newton import SEED, colorize, grid, newton
from zeta_fast import zeta, zeta_em

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--ext", type=float, nargs=4, default=[-2.2, 4.2, -2.7, 2.7])
    p.add_argument("--width", type=int, default=640)
    p.add_argument("--T", type=float, default=50)
    p.add_argument("--out", default="output/overlay.png")
    a = p.parse_args()
    ext = a.ext
    W = a.width
    H = int(W * (ext[3] - ext[2]) / (ext[1] - ext[0]))
    C = grid(ext, W, H)
    lim, n, st = newton(np.full(C.shape, SEED), C, iters=120)
    rgb = colorize(lim, n, st, H, W, escape_rgb=(0.90, 0.90, 0.88))

    t = np.linspace(-a.T, a.T, int(800 * a.T))
    fv = zeta_em(0.5 + 1j * t, N=max(60, int(a.T / 4)))

    fig = plt.figure(figsize=(W / 100, H / 100), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(rgb, origin="lower", extent=ext, interpolation="bilinear")
    ax.plot(fv.real, fv.imag, color="white", lw=1.6, alpha=0.9)
    ax.plot(fv.real, fv.imag, color="#26215C", lw=0.7)
    for per, col, mk, ms in [(2, "#D85A30", "o", 4.5), (3, "#D4537E", "s", 3.2)]:
        u = find(per, ext)
        print(f"period {per}: {len(u)} centers")
        ax.plot(u.real, u.imag, mk, ms=ms, mfc="none", mec=col, mew=1.2)
    cv = zeta(np.array([SEED]))[0]
    ax.plot([cv.real], [cv.imag], "*", ms=11, color="#1D9E75", mec="white", mew=0.6)
    ax.plot([0], [0], "o", ms=6, color="black", mec="white", mew=1)
    ax.set_xlim(ext[:2]); ax.set_ylim(ext[2:]); ax.axis("off")
    fig.savefig(a.out)
    print("saved", a.out)
