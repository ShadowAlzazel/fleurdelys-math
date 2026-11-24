"""The petal ledger: all zeros N(T) against the petals through 0, N0(T).

For F = zeta, L(s, chi_4) and the Davenport-Heilbronn function, with completed function
Lambda(s) = G(s) F(s) (entire, Lambda(s) = Lambda(1 - s), real on the critical line):

    N(T)  = all zeros with 0 < Im <= T in the strip  = (1/pi) * change of arg Lambda along 2 -> 2 + iT -> 1/2 + iT
            (argument principle; the other half of the rectangle gives the same by symmetry)
    N0(T) = zeros ON the line = sign changes of the real function Lambda(1/2 + it) / |G| (the petals through 0)
    deficit N(T) - N0(T) = 2 x (zeros to the right of the line, up to height T)

RH for zeta is exactly: deficit = 0 for every T (target A). For Davenport-Heilbronn the deficit
jumps by 2 at each off-line zero.

    python petal_ledger.py
    python petal_ledger.py --T 300
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import loggamma

from dh_fast import dh, dirichlet_L
from zeta_fast import zeta

BLUE, ORANGE, AQUA, GRAY, INK = "#2a78d6", "#eb6834", "#1baf7a", "#888780", "#3d3d3a"


def _n_terms(s):
    return int(np.max(np.abs(np.imag(s))) / (2 * np.pi)) + 60


FUNCS = {
    "ζ": dict(
        F=lambda s: zeta(s, N=_n_terms(s)),
        logG=lambda s: np.log(s) + np.log(s - 1) - np.log(2) - s / 2 * np.log(np.pi) + loggamma(s / 2),
        color=BLUE),
    "L(s, χ₄)": dict(
        F=lambda s: dirichlet_L(s, [0, 1, 0, -1], N=_n_terms(s)),
        logG=lambda s: (s + 1) / 2 * np.log(4 / np.pi) + loggamma((s + 1) / 2),
        color=AQUA),
    "Davenport–Heilbronn": dict(
        F=lambda s: dh(s, N=_n_terms(s)),
        logG=lambda s: (s + 1) / 2 * np.log(5 / np.pi) + loggamma((s + 1) / 2),
        color=ORANGE),
}


def petals(fn, Tmax):
    """Heights of the sign changes of the real function Lambda(1/2 + it)/|G|: the petals through 0."""
    F, logG = fn["F"], fn["logG"]
    tl = np.arange(0.3, Tmax + 0.002, 0.002)
    sl = 0.5 + 1j * tl
    Zr = np.real(np.exp(1j * np.imag(logG(sl))) * F(sl))
    return tl[1:][np.sign(Zr[1:]) != np.sign(Zr[:-1])]


def ledger(fn, Ts, sig_from=2.0, dt=0.01, nh=500):
    """N(T) via the argument principle and N0(T) via sign changes, for each T in Ts."""
    F, logG = fn["F"], fn["logG"]
    # vertical path 2 -> 2 + i Tmax
    tv = np.arange(0, Ts.max() + dt, dt)
    sv = sig_from + 1j * tv
    av = np.unwrap(np.angle(F(sv)))
    N = np.empty(len(Ts))
    for k, T in enumerate(Ts):
        a0 = np.interp(T, tv, av)
        sh = np.linspace(sig_from, 0.5, nh) + 1j * T
        ah = np.unwrap(np.angle(F(sh)))
        ah = ah - ah[0] + a0          # continue the unwrapped angle from the vertical path
        total = ah[-1] + np.imag(logG(sh[-1])) - np.imag(logG(sig_from + 0j))
        N[k] = total / np.pi
    flips = petals(fn, Ts.max())
    N0 = np.searchsorted(flips, Ts)
    return N, N0, flips


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=float, default=200)
    ap.add_argument("--out", default="output/petal_ledger.png")
    a = ap.parse_args()

    Ts = np.arange(5.0, a.T, 0.25)
    # skip heights within 0.01 of any petal (a zero on the line), where the count is ambiguous
    allflips = np.sort(np.concatenate([petals(fn, a.T) for fn in FUNCS.values()]))
    near = np.abs(Ts[:, None] - allflips[None, :]).min(axis=1) < 0.01
    Ts = Ts[~near]
    print(f"{near.sum()} grid heights skipped for sitting within 0.01 of a zero on the line")
    res = {}
    for name, fn in FUNCS.items():
        N, N0, flips = ledger(fn, Ts)
        frac = np.max(np.abs(N - np.round(N)))
        Nr = np.round(N).astype(int)
        d = Nr - N0
        jumps = Ts[1:][np.diff(d) != 0]
        res[name] = (Nr, N0, d)
        print(f"{name:20s} N({Ts[-1]:.0f}) = {Nr[-1]}, petals N0 = {N0[-1]}, deficit {d[-1]}; "
              f"largest distance of N from an integer {frac:.3f}; deficit changes near t = {np.round(jumps, 1).tolist()}")
    g = np.load("output/zeros_10000.npy")
    Nz = np.searchsorted(g, Ts)
    print(f"check: zeta's N(T) against the stored zeros list: max difference {np.max(np.abs(res['ζ'][0] - Nz))}")

    fig, axs = plt.subplots(1, 2, figsize=(16, 6.4), dpi=150, gridspec_kw={"width_ratios": [1.3, 1]})
    ax = axs[0]
    for name, fn in FUNCS.items():
        Nr, N0, d = res[name]
        ax.step(Ts, Nr, where="post", color=fn["color"], lw=1.4, label=f"{name}: all zeros N(T)")
        ax.step(Ts, N0, where="post", color=fn["color"], lw=1.0, ls="--", label=f"{name}: petals through 0, N₀(T)")
    ax.set_xlabel("height T")
    ax.set_ylabel("count up to T")
    ax.set_title("The petal ledger: every zero (solid) against the petals through 0 (dashed)", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax = axs[1]
    for name, fn in FUNCS.items():
        ax.step(Ts, res[name][2], where="post", color=fn["color"], lw=1.8, label=name)
    ax.set_xlabel("height T")
    ax.set_ylabel("petal deficit N(T) − N₀(T)")
    ax.set_yticks(range(0, int(max(r[2].max() for r in res.values())) + 2, 2))
    ax.set_title("Petal deficit = 2 × zeros right of the line.\nRH for ζ: it stays 0 forever (target A)", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
