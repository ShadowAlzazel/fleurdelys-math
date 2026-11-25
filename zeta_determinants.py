"""Zeta functions as determinants of cycle matrices, and the places where RH is a theorem.

The Collatz cycle matrix B (cycle_matrix.py) has det(I - zB) = 1 - mu z^p. Multiply such factors over
all prime cycles of a dynamical system and you get a dynamical zeta function (Artin-Mazur 1965,
Ruelle 1976): prime cycles play the role of primes. Riemann's zeta is the same shape,
    zeta(s) = prod_p (1 - p^-s)^-1,   each prime a 1 x 1 "cycle matrix" [p^-s].
Where an RH-type statement is PROVEN, it says exactly: the eigenvalues of some matrix lie on a circle.

 (a) Euler factors: the zeros of 1 - p^-s lie on Re s = 0, spaced 2 pi / log p. No single factor
     vanishes in the critical strip; zeta's zeros (on Re s = 1/2, RH) appear only for the whole
     product after analytic continuation (compare euler_product.py).
 (b) Graphs (Ihara 1966, Hashimoto 1989): for a (q+1)-regular graph, Ihara's zeta = 1/det(I - uH),
     H the non-backtracking edge matrix (a shift on directed edges, like B). Its "RH": every
     nontrivial eigenvalue of H has |lambda| = sqrt(q). True exactly for Ramanujan graphs
     (Lubotzky-Phillips-Sarnak 1988). The Petersen graph and a random 3-regular graph pass
     (random graphs nearly always nearly do: Friedman 2008).
 (c) A 3-regular graph with bottlenecks fails: it has an Euler product but some eigenvalues leave
     the circle. An Euler product alone does not force RH.
 (d) Curves over finite fields (Hasse 1933, Weil 1948; Deligne 1974 in general): for the elliptic curve
     y^2 = x^3 + x + 1, the zeta function at p has a factor 1 - a_p T + p T^2 = det(I - T Frob), and
     its two eigenvalues alpha, conj(alpha) satisfy |alpha| = sqrt(p): RH, proven. Their angles follow
     the Sato-Tate law (2/pi) sin^2 (proven 2011).

    python zeta_determinants.py
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

from collatz_polar import primes_upto
from zeros import load

BLUE, ORANGE, AQUA, GRAY, INK, PURPLE = "#2a78d6", "#eb6834", "#1baf7a", "#888780", "#3d3d3a", "#534AB7"


def hashimoto(A):
    """Non-backtracking matrix on directed edges: (u->v) -> (v->w) with w != u."""
    edges = [(u, v) for u in range(len(A)) for v in np.nonzero(A[u])[0]]
    idx = {e: i for i, e in enumerate(edges)}
    H = np.zeros((len(edges), len(edges)))
    for (u, v), i in idx.items():
        for w in np.nonzero(A[v])[0]:
            if w != u:
                H[i, idx[(v, w)]] = 1
    return H


def petersen():
    A = np.zeros((10, 10))
    for i in range(5):
        for a, b in [(i, (i + 1) % 5), (i, i + 5), (i + 5, (i + 2) % 5 + 5)]:
            A[a, b] = A[b, a] = 1
    return A


def random_regular(n, d, rng):
    while True:
        stubs = rng.permutation(np.repeat(np.arange(n), d)).reshape(-1, 2)
        if np.any(stubs[:, 0] == stubs[:, 1]):
            continue
        A = np.zeros((n, n))
        ok = True
        for a, b in stubs:
            if A[a, b]:
                ok = False
                break
            A[a, b] = A[b, a] = 1
        if ok:
            return A


def block_ring(n):
    """n copies of K4 minus an edge, joined in a ring: 3-regular with bottlenecks."""
    A = np.zeros((4 * n, 4 * n))
    for b in range(n):
        v = [4 * b + i for i in range(4)]
        for i in range(4):
            for j in range(i + 1, 4):
                if (i, j) != (0, 3):
                    A[v[i], v[j]] = A[v[j], v[i]] = 1
        w = 4 * ((b + 1) % n)
        A[v[3], w] = A[w, v[3]] = 1
    return A


def frobenius_traces(P):
    """a_p = p + 1 - #E(F_p) for y^2 = x^3 + x + 1, primes p <= P not dividing 2 * 31."""
    out = []
    for p in primes_upto(P):
        if p in (2, 31):
            continue
        x = np.arange(p, dtype=np.int64)
        sq = np.zeros(p, dtype=int)
        sq[(x * x) % p] = 1                                     # squares mod p (0 included)
        v = (x * x % p * x + x + 1) % p
        chi = np.where(v == 0, 0, 2 * sq[v] - 1)               # Legendre symbol of x^3 + x + 1
        out.append((p, -int(chi.sum())))
    return np.array(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--P", type=int, default=20000, help="primes for the elliptic curve")
    ap.add_argument("--n", type=int, default=200, help="vertices of the random 3-regular graph")
    ap.add_argument("--ring", type=int, default=8, help="blocks in the bottleneck graph")
    ap.add_argument("--out", default="output/zeta_determinants.png")
    a = ap.parse_args()
    rng = np.random.default_rng(3)
    q = 2

    graphs = {"Petersen graph (10 vertices)": petersen(),
              f"random 3-regular graph ({a.n} vertices)": random_regular(a.n, 3, rng),
              f"ring of {a.ring} blocks (K₄ minus an edge), {4 * a.ring} vertices": block_ring(a.ring)}
    spectra = {}
    for name, A in graphs.items():
        lamA = np.sort(np.linalg.eigvalsh(A))
        ev = np.linalg.eigvals(hashimoto(A))
        nontriv = ev[(np.abs(ev - q) > 1e-6) & (np.abs(np.abs(ev) - 1) > 1e-6)]
        off = nontriv[np.abs(np.abs(nontriv) - np.sqrt(q)) > 1e-6]
        spectra[name] = (ev, off)
        print(f"{name}: second adjacency eigenvalue {lamA[-2]:.4f} vs 2 sqrt 2 = {2 * np.sqrt(2):.4f} -> "
              f"{'Ramanujan' if lamA[-2] <= 2 * np.sqrt(2) + 1e-9 and lamA[0] >= -2 * np.sqrt(2) - 1e-9 else 'NOT Ramanujan'}; "
              f"Hashimoto {ev.size}x{ev.size}: {nontriv.size} nontrivial eigenvalues, {off.size} off the circle |λ| = √2"
              + (f" (|λ| = {np.round(np.sort(np.abs(off)), 4).tolist()})" if off.size else ""))

    tr = frobenius_traces(a.P)
    p, ap_ = tr[:, 0].astype(float), tr[:, 1].astype(float)
    ratio = np.abs(ap_) / (2 * np.sqrt(p))
    theta = np.arccos(np.clip(ap_ / (2 * np.sqrt(p)), -1, 1))
    print(f"elliptic curve y^2 = x^3 + x + 1: {len(p)} primes up to {a.P}; max |a_p| / (2 sqrt p) = {ratio.max():.4f} "
          f"(Hasse: <= 1, i.e. both Frobenius eigenvalues on |alpha| = sqrt p)")
    h, edges = np.histogram(theta, bins=18, range=(0, np.pi), density=True)
    mid = (edges[1:] + edges[:-1]) / 2
    print(f"Sato-Tate: largest gap between the angle histogram and (2/pi) sin^2 = {np.abs(h - 2 / np.pi * np.sin(mid) ** 2).max():.3f}")

    g = load(10000)
    fig, axs = plt.subplots(2, 2, figsize=(16, 15), dpi=150)

    ax = axs[0, 0]
    T = 45
    for pr, col in zip((2, 3, 5, 7), (BLUE, AQUA, PURPLE, GRAY)):
        tz = np.arange(0, T, 2 * np.pi / np.log(pr))
        ax.plot(np.zeros_like(tz) + 0.012 * (pr - 4), tz, "o", color=col, ms=4,
                label=f"zeros of 1 − {pr}⁻ˢ: Re s = 0, spacing 2π/log {pr} = {2 * np.pi / np.log(pr):.2f}")
    ax.plot(np.full((g < T).sum(), 0.5), g[g < T], "*", color=ORANGE, ms=10, label="zeros of ζ (Re s = ½, RH)")
    ax.axvspan(0, 1, color=GRAY, alpha=0.08)
    ax.axvline(0.5, color=ORANGE, lw=0.8, ls="--")
    ax.set_xlim(-0.3, 1.3)
    ax.set_ylim(-1, T)
    ax.set_xlabel("Re s")
    ax.set_ylabel("Im s")
    ax.set_title("(a) ζ(s) = ∏ (1 − p⁻ˢ)⁻¹: each prime is a 1×1 cycle matrix [p⁻ˢ].\n"
                 "No factor vanishes in the strip (gray); ζ's zeros come from the whole product, continued.\n"
                 "(The factor zeros all lie on Re s = 0; they are nudged sideways here so they don't overlap)", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="upper right")

    circ = np.linspace(0, 2 * np.pi, 400)
    ax = axs[0, 1]
    for (name, (ev, off)), col, mk in zip(list(spectra.items())[:2], [AQUA, BLUE], ["o", "."]):
        ax.plot(ev.real, ev.imag, mk, color=col, ms=6 if mk == "o" else 5, alpha=0.8,
                label=f"{name}: {off.size} nontrivial eigenvalues off the circle")
    ax.plot(np.sqrt(q) * np.cos(circ), np.sqrt(q) * np.sin(circ), color=INK, lw=1, label="circle |λ| = √2 (graph RH)")
    ax.plot([q, 1, -1], [0, 0, 0], "x", color=ORANGE, ms=9, label="trivial eigenvalues 2, ±1")
    ax.set_aspect("equal")
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-2.6, 2.6)
    ax.set_title("(b) Graphs: Ihara zeta = 1/det(I − uH), H the non-backtracking shift on directed edges.\n"
                 "RH for the graph ⇔ Ramanujan ⇔ eigenvalues on the circle. Petersen passes; this random graph misses by a hair\n"
                 "(λ₂ = 2.834 vs 2√2 = 2.828), as Friedman's theorem (2008) allows: random graphs are nearly Ramanujan", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="lower left")

    ax = axs[1, 0]
    name, (ev, off) = list(spectra.items())[2]
    ax.plot(ev.real, ev.imag, "o", color=PURPLE, ms=5, label=name)
    ax.plot(off.real, off.imag, "o", color=ORANGE, ms=9, mfc="none", mew=1.6,
            label=f"{off.size} eigenvalues off the circle (|λ| = {', '.join(f'{x:.3f}' for x in np.unique(np.round(np.abs(off), 3)))})")
    ax.plot(np.sqrt(q) * np.cos(circ), np.sqrt(q) * np.sin(circ), color=INK, lw=1)
    ax.set_aspect("equal")
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-2.6, 2.6)
    ins = ax.inset_axes([0.62, 0.66, 0.35, 0.32])
    A = graphs[name]
    pos = []
    for b in range(a.ring):
        c = np.exp(2j * np.pi * b / a.ring)
        for i, off_ in enumerate([0, 0.18j, -0.18j, 0.3]):
            pos.append(c * (1 + off_ * np.exp(-0.0j)))
    pos = np.array(pos)
    for u, v in zip(*np.nonzero(np.triu(A))):
        ins.plot([pos[u].real, pos[v].real], [pos[u].imag, pos[v].imag], color=GRAY, lw=0.7)
    ins.plot(pos.real, pos.imag, "o", color=PURPLE, ms=3)
    ins.set_aspect("equal")
    ins.axis("off")
    ins.set_title("the graph: dense blocks, thin links", fontsize=7)
    ax.set_title("(c) RH fails for a graph with bottlenecks: it still has an Euler product over its cycles,\n"
                 "but some eigenvalues leave the circle. An Euler product alone does not force RH", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="lower left")

    ax = axs[1, 1]
    alpha = (ap_ + 1j * np.sqrt(np.maximum(4 * p - ap_ ** 2, 0))) / 2 / np.sqrt(p)
    ax.plot(alpha.real, alpha.imag, ".", color=BLUE, ms=2, alpha=0.6)
    ax.plot(alpha.real, -alpha.imag, ".", color=BLUE, ms=2, alpha=0.6, label=f"α/√p and its conjugate, {len(p):,} primes ≤ {a.P:,}")
    ax.plot(np.cos(circ), np.sin(circ), color=INK, lw=0.8)
    ax.set_aspect("equal")
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.45, 1.3)
    ax.set_title("(d) Curves over finite fields: for y² = x³ + x + 1, the factor 1 − aₚT + pT² = det(I − T·Frob).\n"
                 f"RH (Hasse 1933, Weil, Deligne): |α| = √p, so every α/√p is on the unit circle (max |aₚ|/2√p = {ratio.max():.3f})",
                 fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    ins = ax.inset_axes([0.33, 0.3, 0.34, 0.3])
    ins.bar(mid, h, width=np.pi / 18, color=BLUE, alpha=0.5)
    xs = np.linspace(0, np.pi, 200)
    ins.plot(xs, 2 / np.pi * np.sin(xs) ** 2, color=ORANGE, lw=1.4)
    ins.set_title("angles vs Sato–Tate (2/π)sin²θ", fontsize=7)
    ins.tick_params(labelsize=6)
    fig.tight_layout()
    fig.savefig(a.out)
    print("saved", a.out)
