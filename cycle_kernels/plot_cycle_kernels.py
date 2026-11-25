"""Reproduce the Collatz cycle, eigenspace, and twin-prime figures.

Requires numpy, matplotlib, mpmath. No network, repository writes, or image assets.
Run: python plot_cycle_kernels.py --size 520 --returns 500 --out .

The matrices are explicitly chosen linearizations on cycle perturbations,
not a claim to reconstruct an unspecified private matrix construction.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.patches import Patch
import mpmath as mp
import numpy as np

mp.mp.dps = 60
INK = "#22334b"
MUTED = "#607087"
ORANGE = "#d88713"
BLUE = "#286fc0"
PAPER = "#fafbfe"


def integer_cycle(start):
    points = [start]
    n = start // 2 if start % 2 == 0 else 3 * start + 1
    while n != start:
        if len(points) > 1000:
            raise ValueError("Start did not close within the chosen budget")
        points.append(n)
        n = n // 2 if n % 2 == 0 else 3 * n + 1
    return points


def local_step_mp(u, n):
    sign = 1 if n % 2 == 0 else -1
    slope = mp.mpf("0.5") if sign == 1 else mp.mpf(3)
    return slope * u + sign * (2 + 5 * (n + u)) / 2 * mp.sin(mp.pi * u / 2) ** 2


def local_step(u, n):
    """Exact displacement identity; avoids subtracting a large integer each step.

    f(n+u) = Collatz(n) + local_step(u,n).
    This is algebraically the same entire extension as the repository's f.
    """
    sign = 1 if n % 2 == 0 else -1
    slope = 0.5 if sign == 1 else 3.0
    return slope * u + sign * (2 + 5 * (n + u)) / 2 * np.sin(np.pi * u / 2) ** 2


def return_mp(u, points):
    for n in points:
        u = local_step_mp(u, n)
    return u


def derivative_mp(u, n):
    return mp.diff(lambda x: local_step_mp(x, n), u)


def matrix_modes(weights):
    """B[j+1,j]=f'(q_j), with indices modulo p. Then B**p=mu*I."""
    p = len(weights)
    B = np.zeros((p, p), complex)
    B[(np.arange(p) + 1) % p, np.arange(p)] = weights
    mu = complex(np.prod(weights))
    root = np.exp(np.log(mu + 0j) / p)
    eigenvalues = root * np.exp(2j * np.pi * np.arange(p) / p)
    columns = []
    for lam in eigenvalues:
        v = np.ones(p, complex)
        for j in range(p - 1):
            v[j + 1] = weights[j] * v[j] / lam
        v /= np.linalg.norm(v)
        columns.append(v)
    V = np.column_stack(columns)
    residual = np.max(np.linalg.norm(B @ V - V * eigenvalues[None, :], axis=0))
    power_residual = np.linalg.norm(np.linalg.matrix_power(B, p) - mu * np.eye(p), ord=np.inf)
    shifted_nullities = []
    for lam in eigenvalues:
        singular = np.linalg.svd(B - lam * np.eye(p), compute_uv=False)
        shifted_nullities.append(int(np.sum(singular < 1e-10 * singular[0])))
    return dict(B=B, V=V, eigenvalues=eigenvalues, mu=mu,
                residual=float(residual), power_residual=float(power_residual),
                rank=int(np.linalg.matrix_rank(B)), shifted_nullities=shifted_nullities)


def build_case(start, guesses):
    points = integer_cycle(start)
    delta = mp.findroot(lambda u: return_mp(u, points) - u,
                        tuple(mp.mpf(v) for v in guesses), tol=mp.mpf("1e-48"))
    if abs(delta) < mp.mpf("1e-15"):
        raise AssertionError("Twin solver returned the integer cycle")
    u = delta
    offsets, twin_weights = [], []
    for n in points:
        offsets.append(u)
        twin_weights.append(float(derivative_mp(u, n)))
        u = local_step_mp(u, n)
    integer_weights = [0.5 if n % 2 == 0 else 3.0 for n in points]
    closure = abs(u - delta)
    if closure > mp.mpf("1e-42"):
        raise AssertionError("High precision twin closure failed")
    # Independently check the stable displacement identity against the original map.
    identity_errors = []
    for n in points[:5]:
        u_test = mp.mpc("0.00000031", "-0.00000019")
        z = n + u_test
        original = (2 + 7*z - (2 + 5*z)*mp.cos(mp.pi*z)) / 4
        nxt = n // 2 if n % 2 == 0 else 3*n + 1
        identity_errors.append(abs(original - (nxt + local_step_mp(u_test, n))))
    integer = matrix_modes(np.array(integer_weights))
    twin = matrix_modes(np.array(twin_weights))
    for mode in (integer, twin):
        if mode["residual"] > 1e-10 or mode["power_residual"] > 1e-9:
            raise AssertionError("Cycle matrix verification failed")
        if mode["rank"] != len(points) or any(k != 1 for k in mode["shifted_nullities"]):
            raise AssertionError("Unexpected matrix or eigenspace nullity")
    return dict(start=start, points=points, period=len(points), delta=float(delta),
                offsets=[float(x) for x in offsets], integer=integer, twin=twin,
                closure=str(closure), identity_error=str(max(identity_errors)))


def classify_grid(case, size, max_returns, extent=None, coordinate_scale=None):
    start, delta = case["start"], case["delta"]
    if start == -17:
        scale = 1e-3
        ext = [-0.10, 0.64, -0.37, 0.37]
        target = delta
    else:
        scale = 1e-3
        ext = [-18, 10, -14, 14]
        target = 0.0
    if extent is not None:
        ext = extent
    if coordinate_scale is not None:
        scale = coordinate_scale
    X, Y = np.meshgrid(np.linspace(ext[0], ext[1], size),
                       np.linspace(ext[2], ext[3], size))
    initial = (X + 1j * Y).ravel() * scale
    u = initial.copy()
    # 0: unresolved; 1: converged to target; 2: exceeded numerical bounds.
    state = np.zeros(u.size, np.uint8)
    time = np.zeros(u.size, np.int32)
    tolerance = scale * 2e-9
    for k in range(max_returns):
        ids = np.flatnonzero(state == 0)
        if ids.size == 0:
            break
        v = u[ids]
        with np.errstate(all="ignore"):
            for n in case["points"]:
                v = local_step(v, n)
                bad = (~np.isfinite(v)) | (np.abs(v.real) > 1e6) | (np.abs(v.imag) > 35)
                v[bad] = np.nan
        bad = ~np.isfinite(v)
        win = (~bad) & (np.abs(v - target) < tolerance)
        state[ids[bad]] = 2
        state[ids[win]] = 1
        time[ids[win]] = k + 1
        u[ids] = v
    return dict(state=state.reshape(X.shape), time=time.reshape(X.shape),
                extent=ext, scale=scale, tolerance=tolerance, returns=max_returns,
                resolution=[size,size],
                share_target=float(np.mean(state == 1)),
                share_unresolved=float(np.mean(state == 0)),
                share_left_bounds=float(np.mean(state == 2)))


def complex_data(values):
    a = np.asarray(values)
    return dict(real=a.real.tolist(), imag=a.imag.tolist())


def serialize_case(case):
    result = {k: case[k] for k in ("start", "points", "period", "delta", "offsets", "closure", "identity_error")}
    for name in ("integer", "twin"):
        mode = case[name]
        result[name] = {k: mode[k] for k in ("residual", "power_residual", "rank", "shifted_nullities")}
        result[name].update({k: complex_data(mode[k]) for k in ("B", "V", "eigenvalues", "mu")})
    result["basin"] = {k: v for k, v in case["basin"].items() if k not in ("state", "time")}
    return result


def draw_cycles(cases, output):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "text.color": INK, "axes.labelcolor": INK,
                         "xtick.color": MUTED, "ytick.color": MUTED,
                         "axes.titleweight": "bold", "axes.edgecolor": "#d0d8e5"})
    fig, axs = plt.subplots(2, 3, figsize=(18, 11), dpi=175,
                            gridspec_kw={"width_ratios": [1.10, 1.05, 1.10]})
    fig.patch.set_facecolor("white")
    theta = np.linspace(0, 2*np.pi, 700)
    for row, case in enumerate(cases):
        start, p = case["start"], case["period"]
        basin = case["basin"]
        color = ORANGE if start == -17 else BLUE
        ax = axs[row, 0]
        cmap = ListedColormap(["#cbd1db", color, "#f0edf8"])
        ax.imshow(basin["state"], origin="lower", extent=basin["extent"],
                  cmap=cmap, vmin=0, vmax=2, interpolation="nearest")
        integer_x, twin_x = 0.0, case["delta"] / basin["scale"]
        ax.plot(integer_x, 0, "+", color=INK, ms=11, mew=1.6)
        ax.plot(twin_x, 0, "x", color=INK, ms=8, mew=1.6)
        for x, label, shift in [(integer_x, str(start), (-4, -20)),
                                 (twin_x, "twin", (8, 9))]:
            ax.annotate(label, (x, 0), xytext=shift, textcoords="offset points",
                        fontsize=9, color=INK,
                        bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none", alpha=.86))
        power = int(round(-np.log10(basin["scale"])))
        ax.set_xlabel(f"Re(z − ({start})) × 10$^{power}$")
        ax.set_ylabel(f"Im(z) × 10$^{power}$")
        ax.set_title(f"Starting points near {start}: period {p}\n"
                     + ("Orange → attracting twin" if start == -17 else "Blue → integer cycle"), pad=10)
        ax.text(.025, .97, f"twin offset: {case['delta']:.3g}\n"
                f"budget: {basin['returns']} returns",
                transform=ax.transAxes, va="top", fontsize=8,
                bbox=dict(boxstyle="round,pad=.4", fc="white", ec="none", alpha=.9))
        if start == -17:
            closeup = ax.inset_axes([.57, .78, .40, .16])
            closeup.axhline(0, color="#cbd3df", lw=.9)
            closeup.plot(0, 0, "+", color=INK, ms=8, mew=1.4)
            closeup.plot(case["delta"]*1e7, 0, "x", color=ORANGE, ms=7, mew=1.4)
            closeup.text(0, .28, "−17", ha="center", fontsize=6)
            closeup.text(case["delta"]*1e7, .28, "twin", ha="center", fontsize=6)
            closeup.set_xlim(-1.0, 5.6)
            closeup.set_ylim(-.65, .9)
            closeup.set_yticks([])
            closeup.set_xticks([0, 2, 4])
            closeup.tick_params(labelsize=6, pad=1)
            closeup.set_title("real-axis detail: (z + 17) × 10⁷", fontsize=6, pad=3)

        ax = axs[row, 1]
        ax.set_facecolor(PAPER)
        ax.plot(np.cos(theta), np.sin(theta), color="#9aa9bd", ls="--", lw=1.0)
        ax.axhline(0, color="#dce2ed", lw=.7)
        ax.axvline(0, color="#dce2ed", lw=.7)
        for name, col, marker in [("integer", BLUE, "o"), ("twin", ORANGE, "x")]:
            mode = case[name]
            val = mode["eigenvalues"]
            radius = abs(mode["mu"]) ** (1/p)
            ax.scatter(val.real, val.imag, s=47 if p > 3 else 65, marker=marker,
                       color=col, facecolors="none" if marker == "o" else col,
                       linewidths=1.4, label=f"{name}: |λ| = {radius:.6f}")
        ax.set_xlim(-1.23, 1.23)
        ax.set_ylim(-1.23, 1.23)
        ax.set_aspect("equal")
        ax.set_xlabel("Re λ")
        ax.set_ylabel("Im λ")
        ax.set_title(f"Cycle transition matrix B ({p} × {p})\n"
                     f"μ integer = {case['integer']['mu'].real:.6f}; twin = {case['twin']['mu'].real:.6f}", pad=10)
        ax.legend(loc="lower center", bbox_to_anchor=(.5, -.03), fontsize=8,
                  frameon=True, facecolor="white", edgecolor="none")
        if p == 18:
            inset = ax.inset_axes([.68, .69, .28, .25])
            for name, col, marker in [("integer", BLUE, "o"), ("twin", ORANGE, "x")]:
                l = case[name]["eigenvalues"][0]
                inset.plot(l.real, l.imag, marker=marker, color=col, ms=5,
                           mfc="none" if marker == "o" else col)
            inset.axvline(1, color="#9aa9bd", ls="--", lw=.8)
            inset.set_xlim(.992, 1.008)
            inset.set_ylim(-.007, .007)
            inset.set_yticks([])
            inset.tick_params(labelsize=6)
            inset.set_title("zoom at +1", fontsize=7)

        ax = axs[row, 2]
        attracting_name = "twin" if start == -17 else "integer"
        mode = case[attracting_name]
        phase = np.angle(mode["V"])
        ax.imshow(phase, origin="lower", cmap="twilight", vmin=-np.pi, vmax=np.pi,
                  interpolation="nearest", aspect="auto")
        ticks = np.arange(p) if p == 3 else np.array([0, 3, 6, 9, 12, 15, 17])
        ax.set_xticks(ticks, ticks)
        ax.set_yticks(ticks, ticks)
        ax.set_xlabel("eigenmode k (one kernel basis vector per column)")
        ax.set_ylabel("cycle coordinate j")
        ax.set_title(f"Eigenvectors of the attracting {attracting_name}\n"
                     "Color = phase of vⱼ; each column spans ker(B − λₖI)", pad=10, fontsize=10)
        ax.text(.5, -.22, f"dim ker B = 0  •  dim ker(B − λₖI) = 1\n"
                f"largest eigenvector residual: {mode['residual']:.1e}",
                transform=ax.transAxes, ha="center", va="top", fontsize=8, color=MUTED)

    fig.suptitle("Collatz cycles: local basins, eigenvalues, and eigenspace kernels",
                 fontsize=20, x=.04, y=.985, ha="left", fontweight="bold")
    fig.text(.04, .945, "Matrix definition: Bⱼ₊₁,ⱼ = f′(qⱼ), cyclic indices.  Bᵖ = μI.  "
             "These are linearizations of the chosen complex Collatz extension.", fontsize=11, color=MUTED)
    patches = [Patch(facecolor=ORANGE, label="−17 twin basin"),
               Patch(facecolor=BLUE, label="1 → 4 → 2 basin"),
               Patch(facecolor="#f0edf8", label="left numerical bounds; fate unclassified"),
               Patch(facecolor="#cbd1db", label="unresolved within budget")]
    fig.legend(handles=patches, loc="lower left", bbox_to_anchor=(.04, .025), ncol=2,
               frameon=False, fontsize=9)
    cbax = fig.add_axes([.77, .047, .18, .014])
    cb = fig.colorbar(ScalarMappable(norm=Normalize(-np.pi,np.pi), cmap="twilight"),
                      cax=cbax, orientation="horizontal")
    cb.set_ticks([-np.pi, 0, np.pi], labels=["−π", "0", "+π"])
    cb.ax.tick_params(labelsize=8)
    fig.subplots_adjust(left=.065, right=.97, top=.87, bottom=.17, hspace=.53, wspace=.33)
    fig.savefig(output, facecolor="white")
    plt.close(fig)


def primes_upto(N):
    sieve = np.ones(N+1, bool)
    sieve[:2] = False
    for p in range(2, int(N**.5)+1):
        if sieve[p]:
            sieve[p*p::p] = False
    return sieve


def draw_primes(output):
    fig, axs = plt.subplots(1, 2, figsize=(15, 8.3), dpi=175)
    limit = 10000
    sieve = primes_upto(limit+2)
    allp = np.flatnonzero(sieve[:limit+1])
    starts = np.flatnonzero(sieve[:-2] & sieve[2:])
    starts = starts[starts+2 <= limit]
    counts = {}
    for ax, R in zip(axs, [300, 10000]):
        ps = allp[allp <= R].astype(float)
        twins = starts[starts+2 <= R].astype(float)
        counts[str(R)] = int(len(twins))
        ax.set_facecolor(PAPER)
        ax.scatter(ps*np.cos(ps),ps*np.sin(ps),s=12 if R==300 else 6,
                   color="#c6ccd7",linewidths=0,label="all primes")
        for values, col, label in [(twins,BLUE,"smaller twin p"),
                                    (twins+2,ORANGE,"larger twin p + 2")]:
            ax.scatter(values*np.cos(values),values*np.sin(values),
                       s=34 if R==300 else 14, color=col, linewidths=.3,
                       edgecolors="white", label=label)
        if R == 300:
            for p in [17, 19, 59, 61, 101, 103, 149, 151, 281, 283]:
                shift = (-16,-15) if p == 17 else ((8,-3) if p == 19 else (4,4))
                ax.annotate(str(p),(p*np.cos(p),p*np.sin(p)),xytext=shift,
                            textcoords="offset points",fontsize=7,color=INK)
        theta = np.linspace(0,2*np.pi,600)
        ax.plot(R*np.cos(theta),R*np.sin(theta),color="#d4dce9",lw=.8)
        ax.set_aspect("equal")
        ax.set_xlim(-1.12*R,1.12*R)
        ax.set_ylim(-1.12*R,1.12*R)
        ax.axis("off")
        ax.set_title(f"Primes ≤ {R:,}: {len(twins):,} complete twin pairs",pad=15,fontsize=13)
    fig.suptitle("Twin primes in the same spiral layout",fontsize=21,
                 x=.06,y=.98,ha="left",fontweight="bold")
    fig.text(.06,.925,"Each integer n is placed at (n cos n, n sin n); angles are in radians. "
             "Pair membership is exact; the spatial layout is a coordinate choice.",fontsize=10,color=MUTED)
    fig.legend(*axs[0].get_legend_handles_labels(),loc="lower center",ncol=3,
               frameon=False,bbox_to_anchor=(.5,.075),fontsize=11)
    fig.text(.06,.025,"Twin primes are shown as an arithmetic reference. "
             "No cycle matrix or eigenvector interpretation is assigned to the prime points.",fontsize=10,color=MUTED)
    fig.subplots_adjust(left=.04,right=.97,top=.84,bottom=.17,wspace=.13)
    fig.savefig(output,facecolor="white")
    plt.close(fig)
    return counts


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--size",type=int,default=520)
    ap.add_argument("--returns",type=int,default=500)
    ap.add_argument("--out",type=Path,default=Path("output/cycle_kernels"))
    ap.add_argument("--package",action="store_true",
                    help="also write README.md and the ZIP into --out (off by default so a run never overwrites a repo README)")
    args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    cases=[build_case(-17,("4e-7","5e-7")),build_case(1,("0.0014","0.0016"))]
    for case in cases:
        print(f"Cycle {case['start']}: p={case['period']}, twin offset {case['delta']:.16g}, "
              f"mu integer={case['integer']['mu'].real:.12g}, twin={case['twin']['mu'].real:.12g}",flush=True)
        case["basin"]=classify_grid(case,args.size,args.returns)
        np.savez_compressed(args.out/f"basin_{case['start']}_{args.size}.npz",
                            state=case["basin"]["state"],time=case["basin"]["time"])
        print(f"  target {case['basin']['share_target']:.1%}, unresolved {case['basin']['share_unresolved']:.1%}; "
              f"eigenvector residual {case['twin']['residual']:.2e}",flush=True)
    cycle_png=args.out/"Fleurdelys_Cycles_and_Kernels.png"
    prime_png=args.out/"Fleurdelys_Twin_Primes.png"
    draw_cycles(cases,cycle_png)
    counts=draw_primes(prime_png)
    data=dict(map="f(z) = (2+7z-(2+5z)cos(pi*z))/4",
              matrix="B[(j+1) mod p,j] = f'(q_j)",
              warning="Local cycle perturbations; not linear combinations of nonlinear cycles.",
              cases=[serialize_case(c) for c in cases],twin_pair_counts=counts)
    data_path=args.out/"cycle_eigenvectors.json"
    data_path.write_text(json.dumps(data,indent=2),encoding="utf-8")
    if not args.package:
        print("Saved",cycle_png,prime_png,data_path,sep="\n",flush=True)
        print("Twin-pair counts",counts,flush=True)
        return
    notes=args.out/"README.md"
    notes.write_text("""# Cycles near −17 and 1: eigenvectors and kernels

These figures use the complex Collatz extension
f(z) = (2 + 7z − (2 + 5z) cos(πz))/4 from the Fleurdelys repository.
This is an explicit interpretation of the request for neighborhoods near −17 and 1.

## Matrix definition

For a p-cycle q_0,...,q_(p−1), put a_j=f′(q_j). Define the p×p matrix
B[(j+1) mod p,j]=a_j, all other entries zero. It acts on the vector of
perturbations at the cycle points. This is the Jacobian of the simultaneous
cycle map H(x)[j+1]=f(x[j]) at its fixed vector of cycle coordinates.

B^p=μI, where μ=product(a_j) is the scalar return multiplier.
The eigenvalues are all p-th roots of μ. An eigenvector obeys
v_(j+1)=a_j*v_j/λ; set v_0=1 and normalize to Euclidean norm 1.
For these four cycles every a_j is nonzero, μ is nonzero, all eigenvalues
are distinct, ker(B)={0}, and each ker(B−λ_k I) is one-dimensional.

Every scalar multiple αv_k lies in its eigenspace, including α=0.
Every perturbation has a unique expansion sum_k α_k v_k. A combination of
different modes generally is not itself an eigenvector. Since an attracting
cycle has |μ|<1, all p modes of its B decay under iteration (possibly with
transient growth). These are local linearized statements; combinations of
cycle points are not generally cycles of f.

## What the figures show

The left panels vary the initial state z, not a parameter of the map.
The negative panel resolves the basin near −17 and its attracting twin,
only about 4.43e−7 away. The positive panel resolves the attracting integer
cycle 1→4→2 and its nearby repelling twin, about 0.001472 away.
Colored points converged to the indicated target within a finite iteration
budget. Pale purple means numerical bounds were exceeded; this is not
an escape theorem. Gray points are unresolved at that budget.

The middle panels plot the eigenvalues of B for the integer and twin cycles.
The right panels display the phase of every component of every eigenvector
of the attracting cycle's B. Column k is a basis for ker(B−λ_k I).
Magnitudes, phases via complex coordinates, matrices, and residuals are
provided in cycle_eigenvectors.json; the phase image alone omits magnitudes.

Twin primes use the same radius=n, angle=n-radians layout as earlier.
No matrix or spectral meaning has been assigned to those prime points.

## Numerical checks and reproduction

Twin cycles were solved at 60 decimal digits and checked for closure.
The stable local-coordinate iteration was independently checked against the
original entire formula at high precision. B^p=μI, eigenvector residuals,
matrix ranks, and shifted nullities were checked for all four cycle matrices.
The basin pictures are finite-resolution numerical experiments.

Install numpy, matplotlib, and mpmath. Then run:

    python plot_cycle_kernels.py --size 520 --returns 500 --out .

No GitHub files are changed by this script. The ZIP includes the script,
both PNG figures, this explanation, and the complex-valued numerical data.
""",encoding="utf-8")
    archive=args.out/"Fleurdelys_Cycle_Kernel_Plots.zip"
    with ZipFile(archive,"w",ZIP_DEFLATED) as zf:
        for path in [cycle_png,prime_png,data_path,notes,Path(__file__).resolve()]:
            zf.write(path,arcname=path.name)
    print("Saved",cycle_png,prime_png,archive,sep="\n",flush=True)
    print("Twin-pair counts",counts,flush=True)


if __name__=="__main__":
    main()
