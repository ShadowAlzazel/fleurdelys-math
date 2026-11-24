"""How the critical line pulls Newton's method for the completed function (xi for zeta).

One Newton step for Lambda moves s by -Lambda/Lambda'. It moves left (toward the line, for s right of
it) exactly when Re(Lambda'/Lambda) > 0. Lagarias (1999): for zeta this holds for every s with
Re s > 1/2 if and only if RH. Under RH, Re(Lambda'/Lambda)(s) = sum over zeros (sigma - 1/2)/|s - rho|^2,
so the "pull" P(s) = Re(Lambda'/Lambda) / (sigma - 1/2) is positive, and largest near zeros.

Top: where a Newton step moves left (blue) or right (orange), for sigma in (1/2, 1.5], t up to T,
for zeta, L(s, chi_4) and Davenport-Heilbronn.
Bottom: the weakest pull at each height, min over sigma of P(sigma + it). Positive means the line
wins at that height; negative means some point is pushed away (an off-line zero nearby).

    python xi_pull.py
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from scipy.special import psi

from petal_ledger import FUNCS

BLUE, ORANGE, AQUA, GRAY, INK = "#2a78d6", "#eb6834", "#1baf7a", "#888780", "#3d3d3a"

DLOGG = {
    "ζ": lambda s: 1 / s + 1 / (s - 1) - 0.5 * np.log(np.pi) + 0.5 * psi(s / 2),
    "L(s, χ₄)": lambda s: 0.5 * np.log(4 / np.pi) + 0.5 * psi((s + 1) / 2),
    "Davenport–Heilbronn": lambda s: 0.5 * np.log(5 / np.pi) + 0.5 * psi((s + 1) / 2),
}


def log_derivative(name, s, h=1e-5):
    F = FUNCS[name]["F"]
    return DLOGG[name](s) + (F(s + h) - F(s - h)) / (2 * h) / F(s)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=float, default=200)
    ap.add_argument("--dt", type=float, default=0.05)
    ap.add_argument("--out", default="output/xi_pull.png")
    a = ap.parse_args()

    sig = np.linspace(0.51, 1.5, 100)
    ts = np.arange(1, a.T, a.dt)
    S, Tt = np.meshgrid(sig, ts, indexing="ij")
    grids = {}
    for name in FUNCS:
        s = (S + 1j * Tt).ravel()
        R = np.concatenate([np.real(log_derivative(name, s[i:i + 100000])) for i in range(0, s.size, 100000)]).reshape(S.shape)
        P = R / (S - 0.5)
        grids[name] = (R, P)
        bad = R < 0
        cols = np.nonzero(bad.any(axis=0))[0]
        runs = np.split(ts[cols], np.nonzero(np.diff(cols) > 1)[0] + 1) if cols.size else []
        print(f"{name:20s} grid points pushed right: {bad.sum()} of {bad.size}; "
              f"heights with any: {[f'{r[0]:.1f}-{r[-1]:.1f}' for r in runs]}; weakest pull min P = {P.min():+.3f}")

    fig = plt.figure(figsize=(16, 12), dpi=150)
    gs = fig.add_gridspec(4, 1, height_ratios=[1, 1, 1, 1.6])
    cmap = ListedColormap(["#f2b8a2", "#c9dcf3"])
    for i, (name, (R, P)) in enumerate(grids.items()):
        ax = fig.add_subplot(gs[i])
        ax.imshow((R > 0).astype(float), origin="lower", aspect="auto", cmap=cmap, vmin=0, vmax=1,
                  extent=[ts[0], ts[-1], sig[0], sig[-1]], interpolation="nearest")
        ax.set_ylabel("σ")
        bad = (R < 0).sum()
        ax.set_title(f"{name}: a Newton step moves toward the line (blue) or away (orange). Pushed away: {bad} of {R.size} points",
                     fontsize=10)
        ax.set_xticklabels([])
    ax = fig.add_subplot(gs[3])
    for name, col in zip(grids, [BLUE, AQUA, ORANGE]):
        P = grids[name][1]
        ax.plot(ts, P.min(axis=0), color=col, lw=0.9, label=name)
    ax.axhline(0, color=INK, lw=0.8)
    ax.set_yscale("symlog", linthresh=0.05)
    ax.set_xlabel("height t")
    ax.set_ylabel("weakest pull at this height\nmin over σ of Re(Λ′/Λ)/(σ − ½)")
    ax.set_title("The line wins where the weakest pull is positive. Davenport–Heilbronn goes negative at its off-line zeros", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    ax.set_xlim(ts[0], ts[-1])
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
