# Cycles near −17 and 1: eigenvectors and kernels

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

## In the Fleurdelys repository (added Nov 25, 2026)

The files above are kept as delivered. One change to `plot_cycle_kernels.py`: `--out` now defaults to
`output/cycle_kernels` (git-ignored), and README.md and the ZIP are written only with `--package`.
Before this change, running it with `--out .` from the repository root would have overwritten the
repository's own README.md. From the repository root:

    python cycle_kernels/plot_cycle_kernels.py --size 520 --returns 500

Reproduced on Nov 25, 2026: same twin offsets (4.4303563429e−7 and 0.0014721821280), the same
basin shares (40.4% and 35.9%), and residuals near 5e−16. Run time about 24 s.

What the matrix B encodes is worked out in `cycle_matrix.py` at the repository root, with its
figure in `output/cycle_matrix.png`, and in the notes ("Session 2, continued: the cycle matrix").
