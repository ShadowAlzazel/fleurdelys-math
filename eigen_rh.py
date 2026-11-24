"""Eigenvalues and RH: the Redheffer matrix, the Mertens function, and random matrices.

Redheffer matrix A_n (Redheffer 1977): a_ij = 1 if i divides j or j = 1, else 0.
    det(A_n) = M(n) = mu(1) + ... + mu(n), the Mertens function.
    RH  <=>  M(n) = O(n^(1/2 + eps)) for every eps > 0   (Littlewood 1912).
So RH is a statement about the determinants of simple 0/1 matrices. Their eigenvalues
(Barrett, Forcade, Pollington 1988; Barrett-Jarvis 1992; Vaughan): 1 with algebraic multiplicity
n - floor(log2 n) - 1, two real eigenvalues near +sqrt(n) and -sqrt(n), and a few small ones.
The eigenvalue 1 is defective (Jordan blocks), so floating-point rounding spreads it into a ring.

Hilbert-Polya idea: the zeros might be the eigenvalues of a self-adjoint operator (that would force
them onto the line). No such operator is known, but the zeros space like eigenvalues of large random
Hermitian (GUE) matrices.

    python eigen_rh.py
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

from zeros import load, theta

BLUE, ORANGE, AQUA, GRAY, INK = "#2a78d6", "#eb6834", "#1baf7a", "#888780", "#3d3d3a"


def redheffer(n):
    A = np.zeros((n, n))
    for i in range(1, n + 1):
        A[i - 1, i - 1::i] = 1
    A[:, 0] = 1
    return A


def mertens(N):
    mu = np.ones(N + 1, dtype=np.int8)
    mu[0] = 0
    isp = np.ones(N + 1, bool)
    isp[:2] = False
    for p in range(2, int(N**0.5) + 1):
        if isp[p]:
            isp[p * p::p] = False
    for p in np.nonzero(isp)[0]:
        mu[p::p] *= -1
        if p * p <= N:
            mu[p * p::p * p] = 0
    return np.cumsum(mu, dtype=np.int64)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=2000, help="size of the Redheffer matrix for the eigenvalues")
    ap.add_argument("--N", type=int, default=10**7, help="Mertens function up to N")
    ap.add_argument("--out", default="output/eigen_rh.png")
    a = ap.parse_args()

    M = mertens(a.N)
    for n in (10, 100, 300):
        print(f"det(A_{n}) = {np.linalg.det(redheffer(n)):+.4f}, M({n}) = {M[n]}")
    ev = np.linalg.eigvals(redheffer(a.n))
    big = ev[np.argsort(-np.abs(ev))[:2]]
    ring = ev[np.abs(ev - 1) < 0.2]
    small = ev[(np.abs(ev - 1) >= 0.2) & (np.abs(ev) < 5)]
    print(f"small eigenvalues away from 1: {small.size} (floor(log2 n) - 1 = {int(np.log2(a.n)) - 1}): {np.round(np.sort_complex(small), 3)}")
    print(f"n = {a.n}: two large eigenvalues {np.round(big.real, 3)} (sqrt n = {np.sqrt(a.n):.3f}); "
          f"{ring.size} eigenvalues within 0.2 of 1 (exact multiplicity of 1: {a.n - int(np.log2(a.n)) - 1}), ring radius up to {np.abs(ring - 1).max():.4f}")
    n = np.arange(1, a.N + 1)
    r = M[1:] / np.sqrt(n)
    print(f"Mertens up to {a.N:,}: max |M(n)|/sqrt(n) = {np.abs(r[100:]).max():.4f} at n = {np.argmax(np.abs(r[100:])) + 101:,}")

    rng = np.random.default_rng(0)
    Nm = 2000
    X = rng.normal(size=(Nm, Nm)) + 1j * rng.normal(size=(Nm, Nm))
    H = (X + X.conj().T) / 2
    lam = np.linalg.eigvalsh(H)
    # unfold: fit a smooth curve to the counting function (index against eigenvalue) and use it as the new scale
    idx = np.arange(Nm)
    fit = np.polynomial.Chebyshev.fit(lam, idx, 15)
    u = fit(lam)
    keep = slice(Nm // 10, Nm - Nm // 10)       # the bulk, away from the edges
    gue_sp = np.diff(u[keep])
    g = load(30000)
    g = g[g > 100]
    zsp = np.diff(theta(g) / np.pi)
    print(f"spacings: random GUE matrix {len(gue_sp)} (mean {gue_sp.mean():.3f}), zeros {len(zsp)} (mean {zsp.mean():.3f})")

    fig, axs = plt.subplots(2, 2, figsize=(15, 12), dpi=150)
    ax = axs[0, 0]
    ax.imshow(redheffer(48), cmap="Greys", interpolation="nearest")
    ax.set_title("The Redheffer matrix A₄₈: 1 where i divides j, or j = 1\n"
                 "det(Aₙ) = Mertens function M(n)   (Redheffer 1977)", fontsize=10)
    ax.set_xlabel("j")
    ax.set_ylabel("i")

    ax = axs[0, 1]
    ax.scatter(ev.real, ev.imag, s=6, color=BLUE)
    ax.axvline(np.sqrt(a.n), color=GRAY, ls=":", lw=0.8)
    ax.axvline(-np.sqrt(a.n), color=GRAY, ls=":", lw=0.8)
    ax.text(np.sqrt(a.n), 0.6, " +√n", color=GRAY, fontsize=8)
    ax.text(-np.sqrt(a.n), 0.6, " −√n", color=GRAY, fontsize=8)
    ax.set_ylim(-1, 1)
    ax.set_xlabel("Re λ")
    ax.set_ylabel("Im λ")
    ax.set_title(f"Eigenvalues of A_{a.n}: two near ±√n, {small.size + 1} small ones (near 0 to 0.95),\nand {a.n - int(np.log2(a.n)) - 1} copies of 1 (ring in the zoom)", fontsize=10)
    ins = ax.inset_axes([0.58, 0.08, 0.38, 0.38])
    ins.scatter(ring.real, ring.imag, s=3, color=BLUE)
    ins.plot([1], [0], "+", color=ORANGE, ms=10)
    ins.set_aspect("equal")
    ins.set_title("zoom at 1: rounding spreads the\ndefective eigenvalue into a ring", fontsize=7)
    ins.tick_params(labelsize=6)

    ax = axs[1, 0]
    step = max(1, a.N // 400000)
    ax.plot(n[::step], r[::step], color=BLUE, lw=0.3)
    ax.axhline(1, color=ORANGE, lw=1, ls="--")
    ax.axhline(-1, color=ORANGE, lw=1, ls="--")
    ax.set_xscale("log")
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlabel("n")
    ax.set_ylabel("M(n) / √n")
    ax.set_title("The determinants, scaled: M(n)/√n up to 10⁷. RH ⇔ M(n) = O(n^(½+ε)) (Littlewood).\n"
                 "The stronger |M(n)| < √n (dashed) is false (Odlyzko–te Riele 1985): no slack again", fontsize=10)

    ax = axs[1, 1]
    bins = np.arange(0, 3.5, 0.05)
    ax.hist(zsp, bins=bins, density=True, color=BLUE, alpha=0.6, label=f"zeros of ζ ({len(zsp):,} spacings)")
    ax.hist(gue_sp, bins=bins, density=True, histtype="step", color=AQUA, lw=1.4,
            label=f"eigenvalues of one random {Nm}×{Nm} Hermitian matrix")
    s = np.linspace(0, 3.5, 400)
    ax.plot(s, 32 / np.pi**2 * s**2 * np.exp(-4 * s**2 / np.pi), color=ORANGE, lw=1.4, label="GUE law (Wigner surmise)")
    ax.set_xlabel("spacing between neighbours (mean 1)")
    ax.set_title("Hilbert–Pólya: the zeros space like eigenvalues of a random Hermitian matrix", fontsize=10)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
