"""Collatz on the complex plane.

The entire function
    f(z) = (2 + 7z - (2 + 5z) cos(pi z)) / 4
equals n/2 at even integers and 3n + 1 at odd integers, so it extends the Collatz
map to every complex number (this extension is studied in Letherman, Schleicher
and Wood, "The (3n+1)-problem and holomorphic dynamics", 1999).

At an integer, f'(n) is 1/2 (even) or 3 (odd), so an integer cycle with k odd and
m even steps has multiplier 3^k / 2^m. Positive cycles are attracting, negative
cycles are repelling (see the printout).

Colors: blue = orbit converges to 1 -> 4 -> 2, gray = converges to 0,
yellow = other bounded behaviour, shades of violet = escapes (darker = later).

    python collatz_complex.py
    python collatz_complex.py --r 0.02          # tighter zooms
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb


def f(z):
    return (2 + 7 * z - (2 + 5 * z) * np.cos(np.pi * z)) / 4


def classify(z, iters=200, R=1e6):
    z = z.copy()
    esc = np.full(z.shape, -1)
    alive = np.ones(z.shape, bool)
    with np.errstate(all="ignore"):
        for k in range(iters):
            z[alive] = f(z[alive])
            bad = alive & (~np.isfinite(z) | (np.abs(z) > R) | (np.abs(z.imag) > 50))
            esc[bad] = k
            alive &= ~bad
    # after many iterations an attracted orbit sits on its cycle; test 3 more steps
    cls = np.full(z.shape, 3)          # 3 = escaped
    cls[alive] = 2                     # 2 = bounded, other
    w = z.copy()
    near0 = np.zeros(z.shape, bool)
    near1 = np.zeros(z.shape, bool)
    with np.errstate(all="ignore"):
        for _ in range(3):
            near0 |= np.abs(w) < 1e-3
            near1 |= np.min(np.abs(w[..., None] - np.array([1, 2, 4])), axis=-1) < 1e-3
            w = f(w)
    cls[alive & near1] = 0
    cls[alive & near0] = 1
    return cls, esc


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--ext", type=float, nargs=4, default=[-22, 6, -1.4, 1.4], help="re_min re_max im_min im_max")
    p.add_argument("--width", type=int, default=2000)
    p.add_argument("--zoom", type=int, default=700, help="pixels across each zoom panel")
    p.add_argument("--r", type=float, default=0.06, help="radius of the zooms around 1, -1, -5")
    p.add_argument("--iters", type=int, default=200)
    p.add_argument("--out", default="output/collatz_complex.png")
    a = p.parse_args()

    for name, c in [("1,4,2", [1, 4, 2]), ("-1,-2", [-1, -2]), ("-5,...", [-5, -14, -7, -20, -10]),
                    ("-17,...", [-17, -50, -25, -74, -37, -110, -55, -164, -82, -41, -122, -61, -182, -91, -272, -136, -68, -34])]:
        k = sum(n % 2 for n in c)
        print(f"cycle {name:8s} {k} odd, {len(c) - k} even steps: multiplier 3^{k}/2^{len(c) - k} = {3**k / 2**(len(c) - k):.4f}")

    def render(ext, width):
        x0, x1, y0, y1 = ext
        h = max(1, int(width * (y1 - y0) / (x1 - x0)))
        X, Y = np.meshgrid(np.linspace(x0, x1, width), np.linspace(y0, y1, h))
        cls, esc = classify(X + 1j * Y, a.iters)
        img = np.ones(cls.shape + (3,))
        img[cls == 0] = to_rgb("#2a78d6")
        img[cls == 1] = to_rgb("#888780")
        img[cls == 2] = to_rgb("#eda100")
        e = cls == 3
        t = np.clip(np.log1p(esc[e]) / np.log1p(30), 0, 1)[:, None]
        img[e] = (1 - t) * np.array(to_rgb("#efedfb")) + t * np.array(to_rgb("#3c3489"))
        return img, cls

    zooms = [(0, 1.2, "around 0 (attracting fixed point)"),
             (1, a.r, "around 1 (attracting cycle 1, 4, 2)"),
             (-1, a.r, "around −1 (repelling cycle −1, −2)"),
             (-5, a.r, "around −5 (repelling 5-cycle)")]
    fig = plt.figure(figsize=(14, 12.5), dpi=150)
    gs = fig.add_gridspec(3, 4, height_ratios=[0.9, 2, 2])
    ax = fig.add_subplot(gs[0, :])
    img, cls = render(a.ext, a.width)
    for i, name in enumerate(["-> 1,4,2", "-> 0", "other bounded", "escapes"]):
        print(f"wide view: {name:14s} {100 * (cls == i).mean():5.2f}% of pixels")
    x0, x1, y0, y1 = a.ext
    ax.imshow(img, origin="lower", extent=a.ext, interpolation="nearest", aspect="auto")
    ints = np.arange(int(np.ceil(x0)), int(np.floor(x1)) + 1)
    ax.plot(ints, np.zeros_like(ints), "k.", ms=2.5)
    ax.set_title("Wide view. Dots: integers", fontsize=9)
    for k, (c, r, title) in enumerate(zooms):
        ax = fig.add_subplot(gs[1 + k // 2, 2 * (k % 2): 2 * (k % 2) + 2])
        ext = [c - r, c + r, -r, r]
        img, cls = render(ext, a.zoom)
        print(f"{title:38s} -> 1,4,2: {100 * (cls == 0).mean():5.2f}%  -> 0: {100 * (cls == 1).mean():5.2f}%  escapes: {100 * (cls == 3).mean():5.2f}%")
        ax.imshow(img, origin="lower", extent=ext, interpolation="nearest")
        ax.plot([c], [0], "k+", ms=10)
        ax.set_title(f"{title}, radius {r:g}", fontsize=9)
    fig.suptitle("Collatz on ℂ: f(z) = (2 + 7z − (2 + 5z)cos πz)/4.   Blue → 1, 4, 2    gray → 0    "
                 "yellow: other bounded    violet: escapes (darker = later)", fontsize=10)
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
