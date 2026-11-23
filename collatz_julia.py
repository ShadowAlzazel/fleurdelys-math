"""Is the orange blob next to -1 a Julia set? Compare it with one.

In the complex Collatz extension f(z) = (2 + 7z - (2 + 5z) cos(pi z)) / 4, the
repelling cycle -1, -2 has an attracting twin 2-cycle (-0.99427, -1.98269).
A critical point of f sits at -1.97401, next to -2, inside the twin's basin.
So f∘f near the twin is quadratic-like (degree 2 with one critical point), and by
Douady-Hubbard its basin should be a distorted copy of the filled Julia set of
z^2 + c, where c makes the attracting fixed point have the same multiplier:
c = lam/2 - lam^2/4 with lam = 0.49874, so c = 0.18719.

Left: the blob (points whose f-orbit converges to the twin cycle).
Right: the filled Julia set of z^2 + c.

    python collatz_julia.py
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

from collatz_complex import f

TWIN = np.array([-0.994269035585, -1.982686712])
LAM = 0.498743


def basin(ext, n, iters=400):
    x0, x1, y0, y1 = ext
    X, Y = np.meshgrid(np.linspace(x0, x1, n), np.linspace(y0, y1, n))
    z = X + 1j * Y
    with np.errstate(all="ignore"):
        for _ in range(iters):
            z = f(z)
            z[~np.isfinite(z) | (np.abs(z) > 1e6)] = np.nan
    return np.nan_to_num(np.min(np.abs(z[..., None] - TWIN), axis=-1), nan=1) < 1e-4


def filled_julia(c, ext, n, iters=300):
    x0, x1, y0, y1 = ext
    X, Y = np.meshgrid(np.linspace(x0, x1, n), np.linspace(y0, y1, n))
    z = X + 1j * Y
    alive = np.ones(z.shape, bool)
    for _ in range(iters):
        z[alive] = z[alive] ** 2 + c
        alive &= np.abs(z) < 4
    return alive


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=900)
    p.add_argument("--out", default="output/collatz_julia.png")
    a = p.parse_args()

    c = LAM / 2 - LAM**2 / 4
    ext_b = [-1.0035, -0.9775, -0.013, 0.013]
    ext_j = [-1.3, 1.3, -1.3, 1.3]
    B = basin(ext_b, a.n)
    J = filled_julia(c, ext_j, a.n)

    # Affine match: K_c meets the real axis in [-beta, beta]; the blob meets it in [xl, xr].
    beta = (1 + np.sqrt(1 - 4 * c)) / 2
    # walk outward from the twin along the real axis until the basin ends
    def edge(direction, h=2e-6):
        x = TWIN[0]
        while basin([x + direction * h] * 2 + [0, 0], 1)[0, 0]:
            x += direction * h
        return x
    xl, xr = edge(-1), edge(+1)
    mid, scale = (xl + xr) / 2, -(xr - xl) / (2 * beta)   # negative: mirror, so beta lands on the left tip
    print(f"c = {c:.5f}, beta = {beta:.5f}; blob meets the real axis in [{xl:.5f}, {xr:.5f}], scale {scale:.5f}")

    # Fraction of pixels where the affinely moved K_c and the blob agree
    X, Y = np.meshgrid(np.linspace(ext_b[0], ext_b[1], a.n), np.linspace(ext_b[2], ext_b[3], a.n))
    w = (X - mid + 1j * Y) / scale
    Jm = np.zeros_like(B)
    zz = w.copy(); alive = np.ones(w.shape, bool)
    for _ in range(300):
        zz[alive] = zz[alive] ** 2 + c
        alive &= np.abs(zz) < 4
    Jm = alive
    agree = (Jm == B).mean()
    iou = (Jm & B).sum() / (Jm | B).sum()
    print(f"after the affine match: pixels agree {100 * agree:.1f}%, overlap / union {100 * iou:.1f}%")

    print(f"left tip of the blob {xl:.6f} vs the integer -1;  multiplier of beta for z^2+c: 2*beta = {2 * beta:.5f} vs 3/2 for the cycle -1, -2")
    fig, axs = plt.subplots(1, 2, figsize=(12, 6.2), dpi=150)
    for ax, M, ext, title in [
        (axs[0], B, ext_b, "Collatz on ℂ: basin of the twin 2-cycle next to −1\n(violet outline: K_c moved by z ↦ mid + scale·z)"),
        (axs[1], J, ext_j, f"Filled Julia set of z² + c, c = {c:.4f}"),
    ]:
        img = np.where(M[..., None], np.array([0.929, 0.631, 0.0]), np.array([0.937, 0.929, 0.984]))
        ax.imshow(img, origin="lower", extent=ext, interpolation="nearest")
        ax.set_title(title, fontsize=10)
    axs[0].contour(X, Y, Jm.astype(float), levels=[0.5], colors="#3c3489", linewidths=0.7)
    axs[0].plot([-1], [0], "k+", ms=10)
    axs[0].plot([TWIN[0]], [0], "kx", ms=7)
    axs[0].text(-1, -0.0022, "−1", ha="center", fontsize=8)
    axs[0].text(TWIN[0], 0.0012, "twin", ha="center", fontsize=8)
    fig.suptitle("Douady–Hubbard prediction: the blob is a distorted copy of a quadratic Julia set", fontsize=11)
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
