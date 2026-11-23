"""Julia copies next to each negative Collatz cycle: degree 2, 8 and 2048.

For the complex extension f(z) = (2 + 7z - (2 + 5z) cos(pi z)) / 4, each repelling
integer cycle has an attracting twin cycle. Next to every EVEN member n of the cycle
sits a critical point (about n - 2/(pi^2 (2 + 5n))), and it lies in the twin's
immediate basin. Odd members have none there. So the return map f^p on a basin
component has degree 2^m, where m is the number of halvings in the cycle:

    -1 -> -2           m = 1   degree 2
    -5 -> ...  (5)     m = 3   degree 8
    -17 -> ... (18)    m = 11  degree 2048

Each panel zooms on the basin component around one even member, where a critical
point sits (marked x); the twin point is marked +.

    python collatz_julia_cycles.py
"""
import argparse

import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np
from matplotlib.colors import to_rgb

from collatz_complex import f

mp.mp.dps = 40
F = lambda z: (2 + 7 * z - (2 + 5 * z) * mp.cos(mp.pi * z)) / 4
FP = lambda z: (7 - 5 * mp.cos(mp.pi * z) + mp.pi * (2 + 5 * z) * mp.sin(mp.pi * z)) / 4

CASES = [  # (label, integer start, period, guess for the twin next to the start, even member to zoom on)
    ("−1 → −2, degree 2", -1, 2, "-0.994269", -2),
    ("−5 → … (5 steps), degree 8", -5, 5, "-4.99993520467", -14),
    ("−17 → … (18 steps), degree 2048", -17, 18, "-16.999999557", -34),
]


def fpow(z, p):
    for _ in range(p):
        z = F(z)
    return z


def cycle(z, p):
    o = [z]
    for _ in range(p - 1):
        o.append(F(o[-1]))
    return o


def in_basin(z, T, p, cycles):
    z = z.copy()
    with np.errstate(all="ignore"):
        for _ in range(p * cycles):
            z = f(z)
            z[~np.isfinite(z) | (np.abs(z) > 1e7)] = np.nan
    d = np.nan_to_num(np.min(np.abs(z[..., None] - T), axis=-1), nan=1.0)
    return d < 1e-6, np.isnan(z)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=520)
    ap.add_argument("--out", default="output/collatz_julia_cycles.png")
    a = ap.parse_args()

    fig, axs = plt.subplots(1, 3, figsize=(16, 5.8), dpi=150)
    for ax, (label, n, p, guess, zoom) in zip(axs, CASES):
        twin = mp.findroot(lambda z: fpow(z, p) - z, mp.mpf(guess))
        T = cycle(twin, p)
        ints = [int(mp.nint(x)) for x in cycle(mp.mpf(n), p)]
        t = complex(T[ints.index(zoom)])
        crit = complex(mp.findroot(FP, zoom - 2 / (mp.pi**2 * (2 + 5 * zoom))))
        Tn = np.array([complex(x) for x in T])
        lam = float(abs(mp.fprod(FP(x) for x in T)))

        # size the window from the component's extent along the real axis
        def edge(start, direction, h):
            z = start
            while in_basin(np.array([z + direction * h]), Tn, p, 400)[0][0]:
                z += direction * h
            return z
        h = abs(crit.real - t.real) / 60
        xl, xr = edge(t, -1, h).real, edge(t, +1, h).real
        # the component is often taller than it is wide, and can be pinched above the critical point:
        # scan upward from several points along the real axis and keep the highest
        top = max(edge(complex(x, 0), 1j, h).imag for x in np.linspace(xl, xr, 9)[1:-1])
        mid, r = (xl + xr) / 2, 0.58 * max(xr - xl, 2 * top)
        ext = [mid - r, mid + r, -r, r]
        X, Y = np.meshgrid(np.linspace(ext[0], ext[1], a.n), np.linspace(ext[2], ext[3], a.n))
        inside, escaped = in_basin(X + 1j * Y, Tn, p, int(60 / (1 - lam)) // 1 + 40)
        img = np.ones(inside.shape + (3,)) * np.array(to_rgb("#efedfb"))
        img[escaped] = to_rgb("#c9c4ee")
        img[inside] = to_rgb("#eda100")
        ax.imshow(img, origin="lower", extent=[(e - zoom) if i < 2 else e for i, e in enumerate(ext)], interpolation="nearest")
        ax.plot([t.real - zoom], [0], "k+", ms=10)
        ax.plot([crit.real - zoom], [crit.imag], "kx", ms=7)
        ax.set_title(f"{label}\ncomponent next to {zoom} (axes: z − ({zoom})); twin multiplier {lam:.4f}", fontsize=10)
        ax.ticklabel_format(style="sci", scilimits=(-2, 2))
        print(f"{label}: twin at {zoom}{t.real - zoom:+.3e}, critical point at {zoom}{crit.real - zoom:+.3e}, "
              f"component spans [{xl - zoom:+.3e}, {xr - zoom:+.3e}] along the real axis and up to {top:.3e} above it, multiplier {lam:.5f}")
    fig.suptitle("Julia copies next to the negative Collatz cycles. Yellow: basin of the twin cycle.  +: twin point.  x: critical point", fontsize=11)
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
