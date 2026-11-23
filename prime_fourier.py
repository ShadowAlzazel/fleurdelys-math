"""Fourier spectra of the primes, the twin primes, and the Collatz step counts.

Treat each as a signal on n = 1..N and take |FFT| at frequency alpha (cycles per unit n).
N = 720720 is divisible by every q <= 16, so every fraction a/q with q <= 16 is an exact bin.

Predicted lines (from the equidistribution of primes in residue classes: Dirichlet, Siegel-Walfisz;
this is the circle method behind Vinogradov and Green-Tao):
    primes:            at alpha = a/q (a coprime to q), height |mu(q)| / phi(q):
                       lines only for square-free q, e.g. 1/2, 1/3, 1/5, 1/6; none at 1/4, 1/8, 1/9.
    twin primes p      (p and p + 2 prime): p is spread evenly over the residues r mod q with
                       r and r + 2 both coprime to q (Hardy-Littlewood), so the height is
                       |sum over those r of e^{2 pi i a r / q}| / (number of those r).
    Collatz steps:     the first m moves depend only on n mod 2^m (Terras), so lines are expected at
                       fractions a/2^m.

    python prime_fourier.py
"""
import argparse
from math import gcd

import matplotlib.pyplot as plt
import numpy as np

from collatz_polar import primes_upto

BLUE, ORANGE, AQUA, GRAY, INK = "#2a78d6", "#eb6834", "#1baf7a", "#888780", "#3d3d3a"


def phi(q):
    return sum(1 for r in range(1, q + 1) if gcd(r, q) == 1)


def mobius_abs(q):
    d = 2
    while d * d <= q:
        if q % (d * d) == 0:
            return 0
        d += 1
    return 1


def collatz_steps(N):
    steps = np.zeros(N + 1, np.int32)
    for n in range(2, N + 1):
        m, k = n, 0
        while m >= n:
            m = m // 2 if m % 2 == 0 else 3 * m + 1
            k += 1
        steps[n] = k + steps[m]
    return steps


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=720720)
    ap.add_argument("--qmax", type=int, default=16)
    ap.add_argument("--out", default="output/prime_fourier.png")
    a = ap.parse_args()
    N = a.N

    P = primes_upto(N)
    S = set(P.tolist())
    tw = np.array([p for p in P if p + 2 in S and p + 2 <= N])
    sig_p = np.zeros(N)
    sig_p[P - 1] = 1
    sig_t = np.zeros(N)
    sig_t[tw - 1] = 1
    st = collatz_steps(N).astype(float)[1:]
    sig_c = st - st.mean()

    freqs = np.fft.rfftfreq(N)
    Fp = np.abs(np.fft.rfft(sig_p)) / len(P)
    Ft = np.abs(np.fft.rfft(sig_t)) / len(tw)
    Fc = np.abs(np.fft.rfft(sig_c)) / np.abs(sig_c).sum()

    rows = []
    for q in range(2, a.qmax + 1):
        for k in range(1, q // 2 + 1):
            if gcd(k, q) != 1:
                continue
            idx = k * N // q
            R = [r for r in range(q) if gcd(r, q) == 1 and gcd(r + 2, q) == 1]
            pred_t = abs(sum(np.exp(2j * np.pi * k * r / q) for r in R)) / len(R)
            rows.append((k, q, idx, mobius_abs(q) / phi(q), Fp[idx], pred_t, Ft[idx], Fc[idx]))
    print(f"N = {N}: {len(P)} primes, {len(tw)} twin-prime pairs")
    print(" a/q    primes: predicted measured   twin primes: predicted measured   Collatz steps")
    for k, q, idx, pp, mp_, pt, mt, mc in rows:
        print(f"{k:2d}/{q:<2d}         {pp:6.3f}   {mp_:6.3f}                {pt:6.3f}   {mt:6.3f}        {mc:7.4f}")
    err_p = max(abs(r[3] - r[4]) for r in rows)
    err_t = max(abs(r[5] - r[6]) for r in rows)
    print(f"largest gap between predicted and measured line heights: primes {err_p:.3f}, twin primes {err_t:.3f}")
    top = np.argsort(Fc[1:])[::-1][:8] + 1
    print("Collatz steps, strongest frequencies:", ", ".join(f"{freqs[i]:.5f} (≈ {np.round(freqs[i] * 64)}/64)" for i in top))

    fig, axs = plt.subplots(3, 1, figsize=(16, 11), dpi=150, sharex=True)
    for ax, F, col, key, lab in [
        (axs[0], Fp, BLUE, 3, f"primes ≤ {N:,} ({len(P):,})"),
        (axs[1], Ft, ORANGE, 5, f"twin primes p (p + 2 also prime), p ≤ {N:,} ({len(tw):,})"),
        (axs[2], Fc, AQUA, None, f"Collatz step counts for n ≤ {N:,}"),
    ]:
        ax.plot(freqs[1:], F[1:], color=col, lw=0.5)
        if key is not None:
            for r in rows:
                if r[key] > 0.02:
                    ax.plot(r[2] / N, r[key], "o", mfc="none", mec=INK, ms=6)
                    ax.text(r[2] / N, r[key] + 0.03, f"{r[0]}/{r[1]}", fontsize=7, ha="center", color=INK)
            ax.set_ylim(0, 1.12)
            ax.set_title(f"Spectrum of the {lab}. Circles: predicted line heights", fontsize=10)
        else:
            for m in (2, 4, 8, 16):
                for k in range(1, m // 2 + 1, 2 if m > 2 else 1):
                    ax.axvline(k / m, color=GRAY, lw=0.5, ls=":")
            ax.set_title(f"Spectrum of the {lab}. Dotted: fractions a/2ᵐ", fontsize=10)
        ax.set_ylabel("|Fourier coefficient|, normalized")
    axs[2].set_xlabel("frequency α (cycles per unit n)")
    axs[2].set_xlim(0, 0.5)
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
