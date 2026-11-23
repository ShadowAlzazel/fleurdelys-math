"""Spectroscopy of the flower: the side-view wave, and the primes <-> zeros transform.

1. Spectrogram of Z(t) (the side-view wave). Riemann-Siegel writes
       Z(t) = 2 sum_{n <= sqrt(t/2pi)} n^(-1/2) cos(theta(t) - t log n) + ...
   so its short-time Fourier transform shows chirp lines at angular frequency
       omega_n(t) = theta'(t) - log n  ~  (1/2) log(t / 2pi) - log n,   one line for EVERY integer n.

2. The transform the other way: P(t) = -sum_{p^k <= X} (log p) p^(-k/2) w(p^k) cos(t k log p).
   It approximates -Re zeta'/zeta(1/2 + it), so it peaks at the zero heights gamma.
   Only prime powers appear here because log zeta = sum Lambda(n)/log n * n^(-s): taking the
   logarithm keeps the primes (in signal-processing words, this is the cepstrum of zeta).

3. The same sum over twin primes only, and over a random set of primes with the same number in
   every range [2^j, 2^(j+1)) (the control). Line strength = mean of P at the zeros, in units of
   P's standard deviation.

    python zeta_spectroscopy.py
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import spectrogram

from collatz_polar import primes_upto
from zeros import Z, load

BLUE, ORANGE, GREEN, GRAY, INK = "#2a78d6", "#eb6834", "#1baf7a", "#888780", "#3d3d3a"


def prime_wave(ts, n, weight, X):
    """-sum weight(n) cos(t log n) with a Fejer taper (1 - log n / log X)."""
    amp = weight * (1 - np.log(n) / np.log(X))
    out = np.empty_like(ts)
    for i in range(0, len(ts), 400):
        out[i:i + 400] = -(np.cos(np.outer(ts[i:i + 400], np.log(n))) @ amp)
    return out


def line_strength(ts, P, zeros):
    m = ts > 12
    Pz = np.interp(zeros, ts, P)
    return (Pz.mean() - P[m].mean()) / P[m].std()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--X", type=int, default=2_000_000, help="primes up to X")
    ap.add_argument("--tmax", type=float, default=100)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out", default="output/zeta_spectroscopy.png")
    a = ap.parse_args()

    # 1. spectrogram of Z(t)
    dt = 0.25
    tz = np.arange(200, 2600, dt)
    zt = Z(tz)
    f, tc, Sxx = spectrogram(zt, fs=1 / dt, nperseg=480, noverlap=456, scaling="spectrum")
    omega = 2 * np.pi * f
    tcc = tz[0] + tc

    # 2-3. prime transforms
    P = primes_upto(a.X)
    S = set(P.tolist())
    twin = np.array([p for p in P if (p + 2 in S or p - 2 in S)])
    rng = np.random.default_rng(a.seed)
    ctrl = []
    for j in range(1, int(np.log2(a.X)) + 2):
        lo, hi = 2**j, 2 ** (j + 1)
        pool = P[(P >= lo) & (P < hi)]
        k = np.sum((twin >= lo) & (twin < hi))
        if k:
            ctrl.append(rng.choice(pool, size=k, replace=False))
    ctrl = np.sort(np.concatenate(ctrl))
    pp, wpp = [], []
    for p in P:
        q = p
        while q <= a.X:
            pp.append(q)
            wpp.append(np.log(p) / np.sqrt(q))
            q *= p
    pp, wpp = np.array(pp, float), np.array(wpp)
    ts = np.arange(0.5, a.tmax, 0.01)
    P_all = prime_wave(ts, pp, wpp, a.X)
    P_twin = prime_wave(ts, twin.astype(float), np.log(twin) / np.sqrt(twin), a.X)
    P_ctrl = prime_wave(ts, ctrl.astype(float), np.log(ctrl) / np.sqrt(ctrl), a.X)
    gz = load(10000)
    gz = gz[(gz > 12) & (gz < a.tmax)]
    strengths = {k: line_strength(ts, v, gz) for k, v in [("all", P_all), ("twin", P_twin), ("ctrl", P_ctrl)]}
    print(f"primes up to {a.X}: {len(P)}; twin-prime members: {len(twin)}; control set: {len(ctrl)}")
    print(f"line strength at the {len(gz)} zeros up to {a.tmax:g} (in standard deviations): "
          f"all prime powers {strengths['all']:.2f}, twin primes {strengths['twin']:.2f}, random control {strengths['ctrl']:.2f}")
    # the control again with 10 different random draws, to see how much one draw varies
    def control(seed):
        r = np.random.default_rng(seed)
        out = []
        for j in range(1, int(np.log2(a.X)) + 2):
            lo, hi = 2**j, 2 ** (j + 1)
            k = np.sum((twin >= lo) & (twin < hi))
            if k:
                out.append(r.choice(P[(P >= lo) & (P < hi)], size=k, replace=False))
        c = np.sort(np.concatenate(out)).astype(float)
        return line_strength(ts, prime_wave(ts, c, np.log(c) / np.sqrt(c), a.X), gz)
    draws = np.array([control(100 + k) for k in range(10)])
    print(f"random control over 10 draws: {draws.mean():.2f} ± {draws.std():.2f} (min {draws.min():.2f}, max {draws.max():.2f})")

    fig = plt.figure(figsize=(17, 12), dpi=150)
    gs = fig.add_gridspec(4, 1, height_ratios=[1.5, 1, 1, 1])
    ax = fig.add_subplot(gs[0])
    ax.pcolormesh(tcc, omega, 10 * np.log10(Sxx + 1e-12), shading="auto", cmap="Greys", vmin=-45, vmax=0)
    for n in range(1, 21):
        w = 0.5 * np.log(tcc / (2 * np.pi)) - np.log(n)
        m = w > 0.02
        ax.plot(tcc[m], w[m], color=ORANGE, lw=0.7, ls="--")
        if m.any():
            ax.text(tcc[m][-1] + 8, w[m][-1], f"n = {n}", fontsize=6.5, color=ORANGE, va="center")
    ax.set_ylim(0, 3.2)
    ax.set_xlim(tcc[0], tcc[-1] + 70)
    ax.set_ylabel("angular frequency ω")
    ax.set_title("Spectrogram of the side-view wave Z(t): one chirp line per whole number n, at ω = ½·log(t/2π) − log n (dashed)",
                 fontsize=10)

    for i, (Pt, col, lab, key) in enumerate([
        (P_all, BLUE, "all prime powers", "all"),
        (P_twin, ORANGE, f"twin primes only ({len(twin)} primes)", "twin"),
        (P_ctrl, GREEN, f"random primes, same count per range ({len(ctrl)} primes): the control", "ctrl")]):
        ax = fig.add_subplot(gs[1 + i])
        m = ts > 8
        ax.plot(ts[m], Pt[m] / Pt[ts > 12].std(), color=col, lw=0.8)
        for gg in gz:
            ax.axvline(gg, color=GRAY, lw=0.5, ls=":")
        ax.set_xlim(8, a.tmax)
        ax.set_ylabel("in std. dev.")
        ax.set_title(f"−Σ log p · p^(−1/2) · cos(t log p) over {lab}, p ≤ {a.X:,}.  Dotted: zeros.  "
                     f"Line strength at the zeros: {strengths[key]:.2f}", fontsize=10)
    ax.set_xlabel("t (height on the critical line)")
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
