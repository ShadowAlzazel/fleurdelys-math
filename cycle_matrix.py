"""What the Collatz cycle matrix B knows (companion to cycle_kernels/plot_cycle_kernels.py).

For a p-cycle q_0, ..., q_(p-1) put a_j = f'(q_j): 3 at an odd step, 1/2 at an even step (for the
integer cycle). B is the p x p weighted cyclic shift B[(j+1) mod p, j] = a_j, so B^p = mu I with
mu = prod a_j = 3^k / 2^m (k odd steps, m even steps).

Four facts, each checked below:
 1. Eigenvalues: the p-th roots of mu, a regular p-gon on the circle of radius mu^(1/p).
    It lies ON the unit circle only if 3^k = 2^m, which never happens. Inside: attracting, outside: repelling.
 2. Eigenvectors: B = D (mu^(1/p) P) D^-1 with P the plain cyclic shift and D diagonal, so every
    eigenvector is a discrete Fourier mode e^(-2 pi i jk/p) times ONE magnitude profile |v_j|.
    The phase picture is exactly the DFT matrix; the Collatz information is in the magnitudes,
    and the profile follows the cycle's own orbit |q_j| / mu^(j/p).
 3. The cycle is the resolvent of B at 1: q_(j+1) = a_j q_j + eps_j (eps = 1 at odd steps), so
        q = (I - B)^(-1) e,   det(I - B) = 1 - mu = (2^m - 3^k) / 2^m.
    This is the classical cycle equation (Boehm-Sontacchi 1978) in matrix form. Every parity pattern
    gives exactly one rational cycle (Lagarias 1990); the integer ones are the cycles of 3n + 1.
 4. A positive cycle with all odd members >= N0 needs 0 < m log 2 - k log 3 <= k / (3 N0)
    (from prod (1 + 1/(3n)) = 2^m / 3^k). So its polygon must sit just inside the unit circle,
    and k must be large: this is how cycle-length lower bounds are proved (Steiner 1977, Eliahou 1993).

    python cycle_matrix.py
    python cycle_matrix.py --pmax 20
"""
import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np

from collatz_twins import fpow, multiplier

BLUE, ORANGE, AQUA, GRAY, INK, PURPLE, RED = "#2a78d6", "#eb6834", "#1baf7a", "#888780", "#3d3d3a", "#534AB7", "#c0392b"
LOG2_3 = np.log2(3)


def collatz(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1


def integer_cycle(start):
    pts = [start]
    n = collatz(start)
    while n != start:
        pts.append(n)
        n = collatz(n)
    return pts


def cycle_matrix(weights):
    p = len(weights)
    B = np.zeros((p, p))
    B[(np.arange(p) + 1) % p, np.arange(p)] = weights
    return B


def all_word_cycles(pmax):
    """For every parity word of length p <= pmax, the rational cycle q_0 = num/den, den = 2^m - 3^k.

    Returns per-word arrays (p, k, mu, q0) and the set of integer cycles found (checked by iterating)."""
    pow3 = 3 ** np.arange(pmax + 1, dtype=np.int64)
    pow2 = 2 ** np.arange(pmax + 1, dtype=np.int64)
    out_p, out_k, out_mu, out_q = [], [], [], []
    found = {}
    n_integer_words = 0
    for p in range(1, pmax + 1):
        words = np.arange(2 ** p, dtype=np.int64)
        bits = (words[:, None] >> np.arange(p)) & 1          # bits[:, j] = 1 if step j is odd
        k = bits.sum(axis=1)
        m = p - k
        num = np.zeros(words.size, dtype=np.int64)
        K = np.zeros(words.size, dtype=np.int64)               # odd steps after j
        M = np.zeros(words.size, dtype=np.int64)               # even steps after j
        for j in range(p - 1, -1, -1):
            num += bits[:, j] * pow3[K] * pow2[m - M]
            K += bits[:, j]
            M += 1 - bits[:, j]
        den = pow2[m] - pow3[k]
        q0 = num / den
        out_p.append(np.full(words.size, p))
        out_k.append(k)
        out_mu.append(pow3[k] / pow2[m])
        out_q.append(q0)
        for i in np.nonzero(num % den == 0)[0]:
            n0 = int(num[i] // den[i])
            n, ok = n0, True
            for j in range(p):
                if n % 2 != bits[i, j]:
                    ok = False
                    break
                n = collatz(n)
            if ok and n == n0:
                n_integer_words += 1
                cyc = integer_cycle(n0)
                key = min(cyc, key=abs)
                found[key] = integer_cycle(key)
    return (np.concatenate(out_p), np.concatenate(out_k), np.concatenate(out_mu), np.concatenate(out_q),
            found, n_integer_words)


def twin_multiplier(n, p):
    lam = multiplier(mp.mpf(n), p)
    c = mp.diff(lambda z: fpow(z, p), n, 2) / 2
    z = mp.findroot(lambda z: fpow(z, p) - z, n + (1 - lam) / c)
    return float(multiplier(z, p)), float(z - n)


def k_lower_bound(N0, kmax):
    """Smallest k <= kmax with 0 < m log 2 - k log 3 <= k log(1 + 1/(3 N0)) for m = ceil(k log2 3)."""
    k = np.arange(1, kmax + 1, dtype=np.float64)
    m = np.ceil(k * LOG2_3)
    delta = m * np.log(2) - k * np.log(3)
    ok = np.nonzero(delta <= k * np.log1p(1 / (3 * N0)))[0]
    return (int(k[ok[0]]), int(m[ok[0]])) if ok.size else (None, None)


def k_lower_bound_cf(N0, terms=60):
    """Same bound for huge N0, scanning upper best approximations m/k > log2 3 (convergents and
    semiconvergents) with mpmath. Any admissible k has delta_k <= k c, and delta_k is at least the
    smallest delta among best approximations with denominator <= k, so the first best approximation
    k* with delta(k*) <= K c for the next one K gives a valid lower bound."""
    mp.mp.dps = 80
    x = mp.log(3) / mp.log(2)
    a, y = [], x
    for _ in range(terms):
        ai = int(mp.floor(y))
        a.append(ai)
        y = 1 / (y - ai)
    c = mp.log(1 + mp.mpf(1) / (3 * N0))
    h0, h1, k0, k1 = 1, a[0], 0, 1
    cands = []
    for i in range(1, terms):
        for t in range(1, a[i] + 1):                        # semiconvergents, then the convergent
            h, kk = t * h1 + h0, t * k1 + k0
            if mp.mpf(h) / kk > x:
                cands.append((kk, h))
        h0, h1, k0, k1 = h1, a[i] * h1 + h0, k1, a[i] * k1 + k0
    cands.sort()
    best = mp.inf
    for kk, h in cands:
        d = h * mp.log(2) - kk * mp.log(3)
        best = min(best, d)
        if best <= kk * c:
            return kk, h
    return None, None


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pmax", type=int, default=22, help="enumerate every parity pattern up to this length")
    ap.add_argument("--kmax", type=int, default=10**6)
    ap.add_argument("--data", default="cycle_kernels/cycle_eigenvectors.json")
    ap.add_argument("--out", default="output/cycle_matrix.png")
    a = ap.parse_args()

    starts = {1: BLUE, -1: AQUA, -5: PURPLE, -17: ORANGE}
    info = {}
    for s in starts:
        q = integer_cycle(s)
        p = len(q)
        w = np.array([0.5 if n % 2 == 0 else 3.0 for n in q])
        eps = np.array([n % 2 for n in q], float)
        B = cycle_matrix(w)
        mu = w.prod()
        k = int((w == 3).sum())
        ev = np.linalg.eigvals(B)
        lam0 = mu ** (1 / p)
        # fact 2: eigenvectors are Fourier modes times one profile
        prof = np.cumprod(np.concatenate([[1.0], w[:-1]])) / lam0 ** np.arange(p)
        V = np.column_stack([prof * np.exp(-2j * np.pi * np.arange(p) * kk / p) for kk in range(p)])
        lam = lam0 * np.exp(2j * np.pi * np.arange(p) / p)
        res = np.abs(B @ V - V * lam[None, :]).max()
        # fact 3: resolvent
        qq = np.linalg.solve(np.eye(p) - B, np.roll(eps, 1))
        tm, tz = twin_multiplier(s, p)
        info[s] = dict(q=q, p=p, k=k, m=p - k, mu=mu, ev=ev, lam0=lam0, prof=prof, twin_mu=tm, twin_off=tz)
        print(f"cycle from {s:4d}: p = {p:2d}, k = {k}, m = {p - k}, mu = 3^{k}/2^{p - k} = {mu:.6f}, polygon radius {lam0:.6f}; "
              f"twin mu {tm:.6f} (radius {abs(tm) ** (1 / p):.6f}, sum of multipliers {mu + tm:.4f})")
        print(f"     Fourier-mode eigenvectors: max |B v - lam v| = {res:.1e}; det(I - B) = {np.linalg.det(np.eye(p) - B):+.6f} "
              f"vs 1 - mu = {1 - mu:+.6f}; resolvent reproduces the cycle to {np.abs(qq - q).max():.1e}; "
              f"corr(log profile, log |q_j|/lam0^j) = {np.corrcoef(np.log(prof), np.log(np.abs(q) / lam0 ** np.arange(p)))[0, 1]:.4f}")

    # check the uploaded data: phase image = DFT matrix, one magnitude profile
    if Path(a.data).exists():
        d = json.load(open(a.data))
        for c in d["cases"]:
            for name in ("integer", "twin"):
                V = np.array(c[name]["V"]["real"]) + 1j * np.array(c[name]["V"]["imag"])
                p = V.shape[0]
                jj, kk = np.meshgrid(np.arange(p), np.arange(p), indexing="ij")
                dphase = np.abs(np.angle(V * np.exp(2j * np.pi * jj * kk / p))).max()
                spread = (np.abs(V).max(1) - np.abs(V).min(1)).max()
                print(f"uploaded data, cycle {c['start']}, {name}: phase minus DFT phase max {dphase:.1e}; "
                      f"magnitude differs between columns by at most {spread:.1e}")

    P, K, MU, Q0, found, nint = all_word_cycles(a.pmax)
    print(f"parity patterns of length <= {a.pmax}: {P.size:,}; each gives one rational cycle; "
          f"{nint} patterns give integer cycles, which are exactly {len(found)} cycles:")
    for key, cyc in sorted(found.items()):
        print(f"     {cyc[:6]}{' ...' if len(cyc) > 6 else ''} (length {len(cyc)})")

    bounds = {}
    for N0 in (1, 10**3, 10**6):
        bounds[N0] = k_lower_bound(N0, a.kmax)
    for N0 in (2**40, 2**68):
        bounds[N0] = k_lower_bound_cf(N0)
    for N0, (kb, mb) in bounds.items():
        print(f"positive cycle with odd members >= {N0:.3g}: needs k >= {kb} odd steps and m >= {mb} halvings (first m/k = {mb}/{kb}; {mb + kb if kb else None} steps of n -> 3n + 1, n/2)")

    fig, axs = plt.subplots(2, 2, figsize=(16, 15), dpi=150)
    ax = axs[0, 0]
    ph = np.linspace(0, 2 * np.pi, 600)
    ax.plot(np.cos(ph), np.sin(ph), color=INK, lw=1.4, label="unit circle (|λ| = 1: neutral)")
    for s, col in starts.items():
        I = info[s]
        ang = np.sort(np.angle(I["ev"]))
        r_int, r_tw = I["lam0"], abs(I["twin_mu"]) ** (1 / I["p"])
        for r, ls, lab in [(r_int, "-", "integer"), (r_tw, "--", "twin")]:
            xs = r * np.cos(np.append(ang, ang[0]))
            ys = r * np.sin(np.append(ang, ang[0]))
            ax.plot(xs, ys, ls=ls, color=col, lw=1.1, marker="o" if ls == "-" else "x", ms=3.5,
                    label=f"{s:+d} cycle ({I['p']} steps), {lab}: radius {r:.4f}")
    ax.set_aspect("equal")
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.35, 1.6)
    ax.legend(frameon=False, fontsize=7, loc="upper center", ncol=2)
    ax.set_title("(a) Eigenvalues of B: a regular p-gon of radius μ^(1/p), μ = 3ᵏ/2ᵐ.\n"
                 "Integer cycle (solid) and its twin (dashed) sit on opposite sides of the circle", fontsize=10)
    ins = ax.inset_axes([0.62, 0.05, 0.36, 0.3])
    for s, col in starts.items():
        I = info[s]
        for r, mk in [(I["lam0"], "o"), (abs(I["twin_mu"]) ** (1 / I["p"]), "x")]:
            ins.plot([r], [0], mk, color=col, ms=6, mfc="none" if mk == "o" else col)
    ins.axvline(1, color=INK, lw=1)
    ins.set_xlim(0.9, 1.1)
    ins.set_yticks([])
    ins.set_title("vertices at angle 0 (zoom on the real axis near 1)", fontsize=7)
    ins.tick_params(labelsize=6)

    ax = axs[0, 1]
    I = info[-17]
    j = np.arange(I["p"])
    orbit = np.abs(np.array(I["q"], float)) / I["lam0"] ** j
    ax.plot(j, I["prof"] / I["prof"][0], "o-", color=ORANGE, lw=1.4, label="|vⱼ| of every eigenvector (one shared profile)")
    ax.plot(j, orbit / orbit[0], "s--", color=INK, lw=0.9, ms=4, label="the cycle itself: |qⱼ| / λ₀ʲ  (−17, −50, −25, …)")
    for jj, n in enumerate(I["q"]):
        ax.annotate(str(n), (jj, I["prof"][jj] / I["prof"][0]), xytext=(0, 7), textcoords="offset points", fontsize=6,
                    ha="center", color=ORANGE)
    ax.set_yscale("log")
    ax.set_ylim(0.8, 60)
    ax.set_xlabel("position j along the 18-cycle")
    ax.set_ylabel("magnitude (relative to j = 0)")
    ax.set_title("(b) Eigenvectors = Fourier modes × one profile. The phase image is exactly the DFT matrix\n"
                 "e^(−2πijk/p); the Collatz content is the magnitude: ×3 up, ÷2 down, drift removed", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    ins = ax.inset_axes([0.70, 0.70, 0.27, 0.27])
    p = I["p"]
    jj, kk = np.meshgrid(np.arange(p), np.arange(p), indexing="ij")
    ins.imshow(np.angle(np.exp(-2j * np.pi * jj * kk / p)), origin="lower", cmap="twilight", vmin=-np.pi, vmax=np.pi)
    ins.set_title("DFT phase −2πjk/18\n(same as the uploaded phase panel)", fontsize=7)
    ins.set_xticks([])
    ins.set_yticks([])

    ax = axs[1, 0]
    x = np.abs(1 - MU)
    y = np.abs(Q0)
    sel = y > 0
    ax.hexbin(np.log10(x[sel]), np.log10(y[sel]), gridsize=120, bins="log", cmap="Greys", mincnt=1)
    for s, col in starts.items():
        I = info[s]
        ax.plot(np.full(I["p"], np.log10(abs(1 - I["mu"]))), np.log10(np.abs(I["q"])), "o", color=col, ms=7, mec="white",
                label=f"{s:+d} cycle: |1 − μ| = |2ᵐ − 3ᵏ|/2ᵐ = {abs(1 - I['mu']):.4g}")
    xx = np.linspace(np.log10(x[sel]).min(), 0.5, 50)
    ax.plot(xx, -xx + np.log10(3), color=RED, lw=1, ls=":", label="|q| = 3/|1 − μ|")
    ax.set_xlim(-2.2, 3.5)
    ax.set_xlabel("log₁₀ |1 − μ| = log₁₀ |det(I − B)|   (how close a vertex comes to 1)")
    ax.set_ylabel("log₁₀ |q₀|")
    ax.set_title(f"(c) The cycle is the resolvent: q = (I − B)⁻¹e. Each of the {P.size:,} parity patterns of length ≤ {a.pmax}\n"
                 f"gives one rational cycle (gray density); only the {len(found)} known integer cycles are integers. Big q needs μ near 1",
                 fontsize=10)
    ax.legend(frameon=False, fontsize=7.5, loc="lower left")

    ax = axs[1, 1]
    kk = np.arange(1, a.kmax + 1, dtype=np.float64)
    mm = np.ceil(kk * LOG2_3)
    delta = mm * np.log(2) - kk * np.log(3)
    rec = np.minimum.accumulate(delta)
    ax.plot(kk[::7], delta[::7], ",", color=GRAY, alpha=0.15)
    ax.plot(kk, rec, color=INK, lw=1, label="smallest m log 2 − k log 3 > 0 so far (best upper approximations of log₂ 3)")
    for N0, col in [(1, BLUE), (10**3, AQUA), (10**6, PURPLE)]:
        ax.plot(kk, kk * np.log1p(1 / (3 * N0)), color=col, lw=1, ls="--", label=f"allowed if every odd member ≥ {N0:g}: k/(3N₀)")
        kb, mb = bounds[N0]
        if kb:
            ax.plot([kb], [mb * np.log(2) - kb * np.log(3)], "o", color=col, ms=6)
            ax.annotate(f"k ≥ {kb}" + ("  (the 1 → 4 → 2 cycle)" if N0 == 1 else ""), (kb, mb * np.log(2) - kb * np.log(3)),
                        xytext=(6, -12), textcoords="offset points", fontsize=7.5, color=col)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(1e-8, 2)
    ax.set_xlabel("k (odd steps in the cycle)")
    ax.set_ylabel("log μ⁻¹ = m log 2 − k log 3  (distance of the polygon inside the circle, × p)")
    k40, m40 = bounds[2**40]
    k68, m68 = bounds[2**68]
    ax.set_title("(d) A new positive cycle needs a polygon just inside the circle: 0 < log μ⁻¹ ≤ k/(3N₀).\n"
                 f"Odd members ≥ 2⁴⁰ ⇒ m ≥ {m40:,} halvings (Eliahou 1993); ≥ 2⁶⁸ ⇒ m ≥ {m68:,}", fontsize=10)
    ax.legend(frameon=False, fontsize=7.5, loc="lower left")
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
