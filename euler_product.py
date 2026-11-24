"""The Euler product: the special part.

zeta(s) = prod_p (1 - p^-s)^-1 for Re s > 1. Three views of what it gives zeta and what the
Davenport-Heilbronn function (no Euler product) lacks.

Top: partial Euler products E_P(1/2 + it) = prod_{p <= P} (1 - p^(-1/2 - it))^-1 for P = 10, 100, 1000,
     next to zeta(1/2 + it). Every factor is nonzero, so a partial product never reaches 0: its flower
     has no petals through the origin. On the line the product does not converge; the petals appear
     only in the limit, through the analytic continuation.
Bottom left: the 3-4-1 trick (Hadamard, de la Vallee Poussin 1896; Mertens 1898). For sigma > 1,
     log|zeta(sigma)^3 zeta(sigma+it)^4 zeta(sigma+2it)| = sum_p sum_k p^(-k sigma)/k (3 + 4cos(k t log p) + cos(2k t log p)) >= 0,
     since 3 + 4 cos x + cos 2x = 2 (1 + cos x)^2. This rules out zeros on Re s = 1 (prime number theorem).
     Without an Euler product the same quantity can go negative.
Bottom right: coefficients b_n of log F = sum b_n n^-s, multiplied by log n. For zeta, b_n log n = Lambda(n):
     only prime powers. For Davenport-Heilbronn, composite n appear too.

    python euler_product.py
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

from collatz_polar import primes_upto
from dh_fast import KAPPA, dh
from zeta_fast import zeta

BLUE, ORANGE, AQUA, GRAY, INK, PURPLE = "#2a78d6", "#eb6834", "#1baf7a", "#888780", "#3d3d3a", "#534AB7"


def partial_product(s, P):
    out = np.ones_like(s)
    for p in primes_upto(P):
        out = out / (1 - np.exp(-s * np.log(p)))
    return out


def log_coefficients(a, nmax):
    """b_n with log(sum a_n n^-s) = sum b_n n^-s, a_1 = 1, via n-weighted Dirichlet convolution."""
    b = np.zeros(nmax + 1, dtype=complex)
    L = np.log(np.arange(nmax + 1) + 0.0 + (np.arange(nmax + 1) == 0))
    for n in range(2, nmax + 1):
        acc = a[n] * L[n]
        for d in range(2, n):
            if n % d == 0:
                acc -= a[n // d] * b[d] * L[d]
        b[n] = acc / L[n]
    return b


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=float, default=60)
    ap.add_argument("--sigma", type=float, default=1.05)
    ap.add_argument("--out", default="output/euler_product.png")
    a = ap.parse_args()

    ts = np.arange(10, a.T, 0.005)   # near t = 0 the partial products blow up; start at t = 10
    s = 0.5 + 1j * ts
    flowers = [(f"partial product, primes ≤ {P}", partial_product(s, P)) for P in (10, 100, 1000)]
    flowers.append(("ζ(½ + it)", zeta(s, N=60)))
    for name, v in flowers:
        print(f"{name:32s} closest approach to 0 for t in [10, {a.T:g}]: {np.abs(v).min():.4f}")

    # 3-4-1 quantity at sigma
    t2 = np.arange(0.5, 400, 0.01)
    sg = a.sigma
    def q341(F):
        return 3 * np.log(np.abs(F(np.array([sg + 0j]))[0])) + 4 * np.log(np.abs(F(sg + 1j * t2))) + np.log(np.abs(F(sg + 2j * t2)))
    Qz = q341(lambda x: zeta(x, N=200))
    Qd = q341(lambda x: dh(x, N=200))
    print(f"3-4-1 quantity at sigma = {sg}: zeta min {Qz.min():+.4f}; Davenport-Heilbronn min {Qd.min():+.4f} "
          f"(negative on {np.mean(Qd < 0):.1%} of t in [0.5, 400])")

    # log coefficients
    nmax = 60
    az = np.ones(nmax + 1)
    chi = np.array([0, 1, 1j, -1j, -1])
    ad = np.array([0] + [(chi[n % 5].real + KAPPA * chi[n % 5].imag) for n in range(1, nmax + 1)], dtype=complex)
    bz = log_coefficients(az.astype(complex), nmax)
    bd = log_coefficients(ad, nmax)
    n = np.arange(nmax + 1)
    comp = [k for k in range(4, nmax + 1) if len([p for p in primes_upto(k) if k % p == 0]) > 1]
    print(f"log-coefficients at composite non-prime-powers n <= {nmax}: zeta max |b_n log n| = "
          f"{np.max(np.abs(bz[comp] * np.log(comp))):.2e}; Davenport-Heilbronn max = {np.max(np.abs(bd[comp] * np.log(comp))):.3f}")

    fig = plt.figure(figsize=(18, 11), dpi=150)
    gs = fig.add_gridspec(2, 4, height_ratios=[1, 1.1])
    for i, (name, v) in enumerate(flowers):
        ax = fig.add_subplot(gs[0, i])
        ax.plot(v.real, v.imag, color=PURPLE, lw=0.5)
        ax.plot([0], [0], "o", color=ORANGE, ms=5)
        ax.set_aspect("equal")
        ax.set_xlim(-2.5, 6)
        ax.set_ylim(-4, 4)
        ax.set_title(f"{name}, t from 10 to {a.T:g}\nclosest to 0: {np.abs(v).min():.4f}", fontsize=9.5)
        ax.axhline(0, color=GRAY, lw=0.4)
        ax.axvline(0, color=GRAY, lw=0.4)
    ax = fig.add_subplot(gs[1, :2])
    ax.plot(t2, Qz, color=BLUE, lw=0.6, label="ζ (Euler product): never below 0")
    ax.plot(t2, Qd, color=ORANGE, lw=0.6, alpha=0.8, label="Davenport–Heilbronn (no Euler product)")
    ax.axhline(0, color=INK, lw=0.8)
    ax.set_xlabel("t")
    ax.set_ylabel(f"log|F(σ)³ F(σ+it)⁴ F(σ+2it)|, σ = {sg}")
    ax.set_title("The 3-4-1 trick: prime by prime 3 + 4cos x + cos 2x = 2(1 + cos x)² ≥ 0.\n"
                 "For ζ it keeps zeros off Re s = 1 (prime number theorem); without the Euler product it fails",
                 fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    ax = fig.add_subplot(gs[1, 2:])
    ax.stem(n[2:] - 0.15, np.real(bz[2:] * np.log(n[2:])), linefmt=BLUE, markerfmt="o", basefmt=" ", label="ζ: b_n · log n = Λ(n)")
    ax.stem(n[2:] + 0.15, np.abs(bd[2:]) * np.log(n[2:]), linefmt=ORANGE, markerfmt="s", basefmt=" ",
            label="Davenport–Heilbronn: |b_n| · log n")
    for k in comp[:6]:
        ax.annotate(str(k), (k, np.abs(bd[k]) * np.log(k)), xytext=(0, 5), textcoords="offset points", fontsize=7,
                    ha="center", color=ORANGE)
    ax.set_xlabel("n")
    ax.set_title("The 'cepstrum': coefficients of log F. Euler product ⇔ only prime powers (ζ).\n"
                 "Davenport–Heilbronn also has composite n (labelled)", fontsize=10)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
