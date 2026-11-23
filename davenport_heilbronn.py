"""A flower that misses a petal: the Davenport-Heilbronn function next to zeta.

The Davenport-Heilbronn function f(s) is a combination of two Dirichlet L-functions
mod 5. It satisfies a functional equation of the same shape as zeta's, so on the
critical line it is also "real length times a turning direction" and draws a
flower. But it has no Euler product, and it has zeros OFF the line, e.g.
0.8085 + 85.6993i. So any argument that uses only the functional equation and the
shape of the flower would also "prove" a false statement about f.

Saves two pictures:
  output/dh_flower.png  zeta's flower vs f's flower near t = 86, and f at sigma = 0.8085
  output/newton_xi.png  horizontal direction of the Newton step for the completed
                        functions (xi for zeta, Lambda for f), same window

    python davenport_heilbronn.py
    python davenport_heilbronn.py --t0 110 --t1 118 --sigma 0.65083 --zt 114.16334   # 2nd off-line zero
"""
import argparse

import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np

mp.mp.dps = 15
R5 = mp.sqrt(5)
KAPPA = (mp.sqrt(10 - 2 * R5) - 2) / (R5 - 1)
CHI = [0, 1, 1j, -1j, -1]     # character mod 5 with chi(2) = i
CHIB = [0, 1, -1j, 1j, -1]    # its conjugate
A, B = (1 - 1j * KAPPA) / 2, (1 + 1j * KAPPA) / 2

PURPLE, ORANGE, GREEN = "#534AB7", "#D85A30", "#1D9E75"


def dh(s, derivative=0):
    return A * mp.dirichlet(s, CHI, derivative) + B * mp.dirichlet(s, CHIB, derivative)


def curve(fn, sigma, t0, t1, n):
    ts = np.linspace(t0, t1, n)
    return ts, np.array([complex(fn(mp.mpc(sigma, t))) for t in ts])


def zero_hits(v, tol):
    """Count local minima of |v| that come within tol of 0."""
    a = np.abs(v)
    m = (a[1:-1] < a[:-2]) & (a[1:-1] < a[2:]) & (a[1:-1] < tol)
    return int(m.sum()), float(a.min())


def log_deriv_zeta_completed(s):
    # xi'/xi for xi(s) = s(s-1)/2 pi^(-s/2) Gamma(s/2) zeta(s)
    return 1 / s + 1 / (s - 1) - mp.log(mp.pi) / 2 + mp.digamma(s / 2) / 2 + mp.zeta(s, 1, 1) / mp.zeta(s)


def log_deriv_dh_completed(s):
    # Lambda'/Lambda for Lambda(s) = (5/pi)^((s+1)/2) Gamma((s+1)/2) f(s)   (odd characters)
    return mp.log(5 / mp.pi) / 2 + mp.digamma((s + 1) / 2) / 2 + dh(s, 1) / dh(s)


def step_field(logd, sig, ts):
    """Real part of the Newton step  N(s) - s = -1 / (log-derivative)."""
    out = np.empty((len(ts), len(sig)))
    for i, t in enumerate(ts):
        for j, x in enumerate(sig):
            out[i, j] = float(mp.re(-1 / logd(mp.mpc(x, t))))
    return out


def style(ax, title):
    ax.plot([0], [0], "o", color=ORANGE, ms=6, zorder=5)
    ax.axhline(0, color="gray", lw=0.4)
    ax.axvline(0, color="gray", lw=0.4)
    ax.set_aspect("equal")
    ax.set_title(title, fontsize=10)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--t0", type=float, default=82)
    p.add_argument("--t1", type=float, default=90)
    p.add_argument("--sigma", type=float, default=0.80852, help="real part of the off-line zero")
    p.add_argument("--zt", type=float, default=85.69935, help="height of the off-line zero")
    p.add_argument("--grid", type=int, default=81)
    a = p.parse_args()

    # 1. Flowers
    tz, vz = curve(mp.zeta, 0.5, a.t0, a.t1, 3000)
    tf, vf = curve(dh, 0.5, a.t0, a.t1, 3000)
    ts, vs = curve(dh, a.sigma, a.t0, a.t1, 3000)
    hz, hf, hs = zero_hits(vz, 0.02), zero_hits(vf, 0.02), zero_hits(vs, 0.02)
    print(f"zeta on the line:  {hz[0]} hits of 0, closest {hz[1]:.2e}")
    print(f"f on the line:     {hf[0]} hits of 0, closest {hf[1]:.2e}")
    print(f"f at sigma={a.sigma}: {hs[0]} hits of 0, closest {hs[1]:.2e}")

    fig, axs = plt.subplots(1, 3, figsize=(15, 5.4), dpi=150)
    for ax, v, title in [
        (axs[0], vz, f"ζ(½ + it): {hz[0]} petals through 0"),
        (axs[1], vf, f"Davenport–Heilbronn f(½ + it): {hf[0]} petals through 0"),
        (axs[2], vs, f"f({a.sigma:g} + it): hits 0 off the line"),
    ]:
        ax.plot(v.real, v.imag, color=PURPLE, lw=0.9)
        style(ax, title)
    fig.suptitle(f"t from {a.t0:g} to {a.t1:g}.  Same functional-equation shape, but f has a zero off the line.")
    fig.tight_layout()
    fig.savefig("output/dh_flower.png")
    print("saved output/dh_flower.png")

    # 2. Horizontal pull of Newton's method for the completed functions
    sig = np.linspace(-0.5, 1.5, a.grid)
    tt = np.linspace(a.t0, a.t1, a.grid)
    fz = step_field(log_deriv_zeta_completed, sig, tt)
    ff = step_field(log_deriv_dh_completed, sig, tt)
    right = lambda F: int(((F > 1e-9) & (sig[None, :] > 0.5)).sum())
    print(f"grid points right of the line where the Newton step moves RIGHT: xi {right(fz)}, Lambda_f {right(ff)}")

    fig, axs = plt.subplots(1, 2, figsize=(11, 6), dpi=150, sharey=True)
    lim = 0.15
    for ax, F, title in [(axs[0], fz, "ξ (completed ζ)"), (axs[1], ff, "Λ (completed Davenport–Heilbronn)")]:
        im = ax.imshow(np.clip(F, -lim, lim), origin="lower", aspect="auto", cmap="RdBu",
                       vmin=-lim, vmax=lim, extent=[sig[0], sig[-1], tt[0], tt[-1]])
        ax.contour(sig, tt, F, levels=[0], colors="k", linewidths=0.6)
        ax.axvline(0.5, color="gray", lw=0.8, ls="--")
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("Re(s) = σ")
    axs[1].plot([a.sigma, 1 - a.sigma], [a.zt, a.zt], "o", mfc="none", mec="k", ms=9)
    axs[0].set_ylabel("t")
    cb = fig.colorbar(im, ax=axs, shrink=0.8)
    cb.set_label("Re(N(s) − s): red = Newton step moves left, blue = moves right")
    fig.suptitle("Newton's method on the completed function: which way does one step move horizontally?")
    fig.savefig("output/newton_xi.png", bbox_inches="tight")
    print("saved output/newton_xi.png")
