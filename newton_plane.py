"""One function, pixel = seed: Newton's method on zeta.

Each starting point is colored by the zero it reaches.
Dark: orbits that drift off to the right, where zeta flattens toward 1.
"""
import argparse

import matplotlib.colors as mc
import matplotlib.pyplot as plt
import numpy as np

from newton import grid, newton

ZEROS = np.array([14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
                  37.5862, 40.9187, 43.3271, 48.0052, 49.7738])

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--ext", type=float, nargs=4, default=[-6, 6, 0, 26], help="re_min re_max im_min im_max")
    p.add_argument("--height", type=int, default=900)
    p.add_argument("--out", default="output/newton_plane.png")
    a = p.parse_args()
    ext = a.ext
    H = a.height
    W = int(H * (ext[1] - ext[0]) / (ext[3] - ext[2]))
    lim, n, st = newton(grid(ext, W, H), 0j, iters=150, R=200)
    trivial = (np.abs(lim.imag) < 0.3) & (lim.real < -1)
    k = np.argmin(np.abs(lim.imag[:, None] - ZEROS[None, :]), axis=1)
    hue = np.mod(0.08 + k * 0.618034, 1.0)
    sat = np.full(n.shape, 0.6)
    val = 0.40 + 0.60 * np.exp(-n / 12)
    hue[trivial] = 0.72
    sat[trivial] = 0.35
    rgb = mc.hsv_to_rgb(np.stack([hue, sat, val], -1))
    rgb[st == 2] = [0.13, 0.15, 0.20]
    rgb[st == 0] = 0
    rgb = rgb.reshape(H, W, 3)
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(rgb, origin="lower", extent=ext, interpolation="bilinear")
    ax.plot([0.5] * len(ZEROS), ZEROS, "o", ms=3, mfc="white", mec="black", mew=0.6)
    ax.set_xlim(ext[:2]); ax.set_ylim(ext[2:]); ax.axis("off")
    fig.savefig(a.out)
    print("saved", a.out)
