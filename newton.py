"""Newton's method for zeta(s) - c, vectorized, plus coloring helpers."""
import warnings

import numpy as np
import matplotlib.colors as mc
import matplotlib.pyplot as plt

from zeta_fast import zeta, zeta_prime

warnings.filterwarnings("ignore")

# A zero of zeta'' : a free critical point of the Newton map for zeta(s) - c.
SEED = -0.35508 + 3.59084j


def newton_map(s, c=0j):
    return s - (zeta(s) - c) / zeta_prime(s)


def newton(s, c, iters=120, tol=1e-9, R=60):
    """Iterate Newton for zeta(s) - c.

    Returns (final points, iteration count, state)
    state: 0 = never settled (bounded cycle), 1 = converged to a root, 2 = escaped.
    """
    s = np.asarray(s, dtype=complex).ravel().copy()
    c = np.broadcast_to(np.asarray(c, dtype=complex), s.shape).ravel()
    n = np.full(s.shape, iters, float)
    state = np.zeros(s.shape, int)
    for k in range(iters):
        idx = np.where(state == 0)[0]
        if idx.size == 0:
            break
        z = s[idx]
        step = (zeta(z) - c[idx]) / zeta_prime(z)
        z2 = z - step
        bad = ~np.isfinite(z2) | (np.abs(z2) > R)
        s[idx] = np.where(bad, z, z2)
        conv = (np.abs(step) < tol) & ~bad
        n[idx[conv]] = k
        state[idx[conv]] = 1
        state[idx[bad]] = 2
        n[idx[bad]] = k
    return s, n, state


def grid(ext, W, H):
    x = np.linspace(ext[0], ext[1], W)
    y = np.linspace(ext[2], ext[3], H)
    X, Y = np.meshgrid(x, y)
    return (X + 1j * Y).ravel()


def colorize(lim, n, state, H, W, escape_rgb=(0.82, 0.82, 0.80)):
    hue = np.mod(np.angle(lim - 0.5) / (2 * np.pi) * 3 + lim.imag / 8, 1.0)
    val = 0.30 + 0.70 * np.exp(-n / 14)
    rgb = mc.hsv_to_rgb(np.stack([hue, np.full(n.shape, 0.55), val], -1))
    rgb[state == 2] = escape_rgb
    rgb[state == 0] = 0
    return rgb.reshape(H, W, 3)


def save_image(rgb, path, ext, W, H, dpi=100):
    fig = plt.figure(figsize=(W / dpi, H / dpi), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(rgb, origin="lower", extent=ext, interpolation="bilinear")
    ax.axis("off")
    fig.savefig(path)
    plt.close(fig)
