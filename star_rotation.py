"""Why a prime progression in the spiral layout looks like a Mandelbrot orbit.

Both turn by a fixed angle at every step, and connecting consecutive points of anything that
turns by close to p/q of a full turn draws a star with q points.

    prime progression a + d j in the spiral layout: each step turns by d mod 2 pi; the radius
        grows by d. For 199 + 210 j, the turn is 0.4225 of a full turn.
    orbit of z -> z^2 + c from 0, for c in the main cardioid: near the attracting fixed point z*,
        z_{n+1} - z* ~ lambda (z_n - z*), so each step turns by arg(lambda) and shrinks by |lambda|.
        For c = -0.48 + 0.35i, the turn is 0.4226 of a full turn.

The main cardioid is exactly the set of c whose fixed point turns by a given angle:
c = lambda/2 - lambda^2/4 with |lambda| < 1. On its edge (|lambda| = 1) the angle p/q is where
the p/q bulb attaches, whose orbits settle on a cycle of q points visited p/q of a turn apart.
So every progression step d picks a point on the cardioid's edge: c(d) = e^{id}/2 - e^{2id}/4.
This is shared geometry (rotation), not number theory: the cardioid does not know which d give primes.

    python star_rotation.py
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

BLUE, ORANGE, AQUA, GRAY, INK = "#2a78d6", "#eb6834", "#1baf7a", "#b4b2a9", "#3d3d3a"


def turns(x):
    return np.mod(x / (2 * np.pi), 1)


def mandelbrot(ext, n, iters=200):
    X, Y = np.meshgrid(np.linspace(ext[0], ext[1], n), np.linspace(ext[2], ext[3], n))
    c = X + 1j * Y
    z = np.zeros_like(c)
    alive = np.ones(c.shape, bool)
    for _ in range(iters):
        z[alive] = z[alive] ** 2 + c[alive]
        alive &= np.abs(z) < 2
    return alive


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--c", type=complex, default=complex(-0.48, 0.35))
    ap.add_argument("--out", default="output/star_rotation.png")
    a = ap.parse_args()

    fig, axs = plt.subplots(1, 3, figsize=(18, 6.4), dpi=150)

    # 1. prime progression in the spiral layout
    ax = axs[0]
    v = 199 + 210 * np.arange(10, dtype=float)
    ax.plot(v * np.cos(v), v * np.sin(v), "-o", color=ORANGE, ms=5, lw=1.3)
    for k, x in enumerate(v):
        ax.annotate(str(int(x)), (x * np.cos(x), x * np.sin(x)), xytext=(4, 4), textcoords="offset points", fontsize=7, color=INK)
    ax.plot(0, 0, "+", color=INK)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"10 primes 199 + 210j in the spiral layout\neach step turns {turns(210):.4f} of a full turn; radius grows",
                 fontsize=10)

    # 2. Mandelbrot orbit
    ax = axs[1]
    lam = 1 - np.sqrt(1 - 4 * a.c)
    zs = lam / 2
    z = 0j
    orb = [z]
    for _ in range(60):
        z = z * z + a.c
        orb.append(z)
    orb = np.array(orb)
    ax.plot(orb.real, orb.imag, "-o", color=BLUE, ms=3.5, lw=0.9)
    ax.plot(zs.real, zs.imag, "x", color=INK, ms=8)
    ax.annotate("fixed point z*", (zs.real, zs.imag), xytext=(8, -12), textcoords="offset points", fontsize=8, color=INK)
    ax.set_aspect("equal")
    ax.set_title(f"orbit of z² + c from 0, c = {a.c.real:+.2f}{a.c.imag:+.2f}i\n"
                 f"each step turns {turns(np.angle(lam)):.4f} of a full turn around z*; shrinks by |λ| = {abs(lam):.3f}",
                 fontsize=10)
    ax.grid(color="#e8e7e2", lw=0.6)

    # 3. where each rotation lives on the Mandelbrot set
    ax = axs[2]
    ext = [-1.05, 0.55, -0.85, 0.95]
    M = mandelbrot(ext, 900)
    ax.imshow(np.where(M[..., None], 0.12, 0.96) * np.ones(3), origin="lower", extent=ext, interpolation="nearest")
    th = np.linspace(0, 2 * np.pi, 600)
    w = np.exp(1j * th)
    card = w / 2 - w * w / 4
    ax.plot(card.real, card.imag, color=GRAY, lw=0.8)
    for d, col, lab in [(210, ORANGE, "step 210 (199 + 210j)"), (150, AQUA, "step 150 (7 + 150j)"), (30, "#6250d6", "step 30 (7 + 30j)")]:
        w = np.exp(1j * d)
        cd = w / 2 - w * w / 4
        ax.plot(cd.real, cd.imag, "o", color=col, ms=8, mec="white", mew=1)
        ax.annotate(f"{lab}: {turns(d):.3f} turn", (cd.real, cd.imag), xytext=(6, 4), textcoords="offset points", fontsize=7.5,
                    color=col, bbox=dict(fc="white", ec="none", alpha=0.8, pad=1))
    ax.plot(a.c.real, a.c.imag, "o", color=BLUE, ms=7, mec="white", mew=1)
    ax.annotate(f"c = {a.c.real:+.2f}{a.c.imag:+.2f}i", (a.c.real, a.c.imag), xytext=(6, -12), textcoords="offset points",
                fontsize=7.5, color=BLUE, bbox=dict(fc="white", ec="none", alpha=0.8, pad=1))
    for p, q in [(2, 5), (3, 7)]:
        w = np.exp(2j * np.pi * p / q)
        cb = w / 2 - w * w / 4
        ax.annotate(f"{p}/{q} bulb", (cb.real, cb.imag), xytext=(-62, 14 if q == 5 else -4), textcoords="offset points", fontsize=7.5,
                    color=INK, bbox=dict(fc="white", ec="none", alpha=0.85, pad=1), arrowprops=dict(arrowstyle="-", color=INK, lw=0.6))
    ax.set_xlim(ext[:2])
    ax.set_ylim(ext[2:])
    ax.set_title("Each turn angle is a point on the main cardioid's edge:\nc = e^{iθ}/2 − e^{2iθ}/4 (gray). Step 210 sits between the 2/5 and 3/7 bulbs",
                 fontsize=10)

    print(f"progression step 210 turns {turns(210):.4f}; orbit at c = {a.c} turns {turns(np.angle(lam)):.4f} (|lambda| {abs(lam):.3f})")
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
