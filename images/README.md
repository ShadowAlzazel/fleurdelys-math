# Fleurdelys: picture gallery

These are pictures from one person's exploration of the Riemann zeta function ζ(s), made with
Claude as a working colleague. **This is not a proof of the Riemann Hypothesis**, and none of it claims to be.
It is a geometry playground: draw the objects, look for patterns, and check each pattern against
what is already known.

**What you are looking at.** The *flower* is the curve t ↦ ζ(½ + it): the values of ζ along the
critical line, drawn in the plane. Every time the curve passes through 0 (a "petal" through the
origin), that height t is a zero of ζ. The Riemann Hypothesis says every nontrivial zero lies on
that line. *Fleurdelys* is the project's name for the whole 4D object, the graph of ζ over the
critical strip; the flower is the shadow of one slice of it.

**How to read the captions.** The project keeps three things apart: proven theorems (named, with
the people who proved them), open conjectures, and numerical observations from the code. Most
patterns here turned out to be known results, seen in a new picture. One recurring test is the
*Davenport–Heilbronn function*. It looks like ζ and draws a similar flower, but it has zeros off
the line, so any argument for RH must fail for it.

The pictures are listed in the order of the journey. Each is a reduced copy; the script named
next to it redraws the full-size version into `output/`. The full story, with tables of theorems
and a step-by-step log, is in `Fleurdelys notes on the zeta flower.md` at the repository root.


## The flower

**1. The flower: ζ(½ + it) for t up to ±50 and ±1000. Every petal that passes through 0 is a zero of ζ.** (`flower.py`)

![The flower: ζ(½ + it) for t up to ±50 and ±1000. Every petal that passes through 0 is a zero of ζ.](01_flower.jpg)

**2. Newton's method on ζ, colored by which zero each starting point reaches.** (`newton_plane.py`)

![Newton's method on ζ, colored by which zero each starting point reaches.](02_newton_plane.png)

**3. A Mandelbrot set copy in the parameter plane of the Newton family for ζ(s) − c (McMullen: Mandelbrot copies are universal).** (`mandelbrot_copy.py`)

![A Mandelbrot set copy in the parameter plane of the Newton family for ζ(s) − c (McMullen: Mandelbrot copies are universal).](03_mandelbrot_copy.png)

**4. The flower drawn on that parameter plane, with the Mandelbrot copy centers marked.** (`overlay.py`)

![The flower drawn on that parameter plane, with the Mandelbrot copy centers marked.](04_overlay.png)


## What a proof of RH must do

**5. ζ's flower beside the Davenport–Heilbronn function: the same kind of flower, but it has zeros off the line (no Euler product).** (`davenport_heilbronn.py`)

![ζ's flower beside the Davenport–Heilbronn function: the same kind of flower, but it has zeros off the line (no Euler product).](05_dh_flower.png)

**6. Newton steps for the completed functions: for ζ they always move toward the critical line; for Davenport–Heilbronn they break near its off-line zeros.** (`davenport_heilbronn.py`)

![Newton steps for the completed functions: for ζ they always move toward the critical line; for Davenport–Heilbronn they break near its off-line zeros.](06_newton_xi.png)


## The petals hear the primes

**7. The zeros in the prime-spiral layout. The angles γ·log x lean toward π exactly when x is a prime power (Landau 1912).** (`zero_polar.py`)

![The zeros in the prime-spiral layout. The angles γ·log x lean toward π exactly when x is a prime power (Landau 1912).](07_zero_polar.png)


## Collatz

**8. Collatz on negative numbers: every start down to −10⁶ ends in one of three cycles.** (`collatz_negative.py`)

![Collatz on negative numbers: every start down to −10⁶ ends in one of three cycles.](08_collatz_negative.png)

**9. The complex Collatz map f(z) = (2 + 7z − (2 + 5z)cos πz)/4, with zooms at 0, 1, −1, −5.** (`collatz_complex.py`)

![The complex Collatz map f(z) = (2 + 7z − (2 + 5z)cos πz)/4, with zooms at 0, 1, −1, −5.](09_collatz_complex.png)

**10. A filled Julia set of z² + c hiding next to the cycle (−1, −2): 99.4% of pixels match (Douady–Hubbard).** (`collatz_julia.py`)

![A filled Julia set of z² + c hiding next to the cycle (−1, −2): 99.4% of pixels match (Douady–Hubbard).](10_collatz_julia.png)

**11. Structure in the steps plot: doubling chains, and 8k + 4, 8k + 5 merging after 3 steps (Terras 1976).** (`collatz_structure.py`)

![Structure in the steps plot: doubling chains, and 8k + 4, 8k + 5 merging after 3 steps (Terras 1976).](11_collatz_structure.png)

**12. Collatz in the prime-spiral layout. The arms come from the layout (2π ≈ 44/7), not from Collatz.** (`collatz_polar.py`)

![Collatz in the prime-spiral layout. The arms come from the layout (2π ≈ 44/7), not from Collatz.](12_collatz_polar.jpg)

**13. Julia set copies next to −2, −14 and −34 (return maps of degree 2, 8 and 2048).** (`collatz_julia_cycles.py`)

![Julia set copies next to −2, −14 and −34 (return maps of degree 2, 8 and 2048).](13_collatz_julia_cycles.png)


## Julia copies around the flower

**14. Where the flower crosses a Mandelbrot copy, with the basilica and the rabbit in the s-plane.** (`zeta_julia.py`)

![Where the flower crosses a Mandelbrot copy, with the basilica and the rabbit in the s-plane.](14_zeta_julia.jpg)


## Spirals and spectra

**15. Primes, twin primes, petals and twin petals in the spiral layout, at two scales.** (`petal_spiral.py`)

![Primes, twin primes, petals and twin petals in the spiral layout, at two scales.](15_petal_spiral.png)

**16. The petal spectrum from 35,673 zeros: a spike of height log p at every prime power up to 100.** (`petal_spectrum.py`)

![The petal spectrum from 35,673 zeros: a spike of height log p at every prime power up to 100.](16_petal_spectrum.png)

**17. The critical strip wrapped onto a spiral (top view) and unrolled with Z(t) (side view).** (`strip_spiral.py`)

![The critical strip wrapped onto a spiral (top view) and unrolled with Z(t) (side view).](17_strip_spiral.png)

**18. Pair correlation of the zeros and its Fourier transform, against random-matrix theory (Montgomery).** (`pair_spacing.py`)

![Pair correlation of the zeros and its Fourier transform, against random-matrix theory (Montgomery).](18_pair_spacing.png)

**19. Spectrogram of Z(t), with one chirp per integer n; the prime wave over all primes, twin primes and a random control.** (`zeta_spectroscopy.py`)

![Spectrogram of Z(t), with one chirp per integer n; the prime wave over all primes, twin primes and a random control.](19_zeta_spectroscopy.jpg)

**20. How strongly twin, cousin, sexy and isolated primes show in the zeros, against matched random primes.** (`prime_subsets.py`)

![How strongly twin, cousin, sexy and isolated primes show in the zeros, against matched random primes.](20_prime_subsets.png)


## Prime patterns

**21. The first prime progressions of length 3 to 12, and their counts against the Green–Tao–Ziegler formula.** (`green_tao.py`)

![The first prime progressions of length 3 to 12, and their counts against the Green–Tao–Ziegler formula.](21_green_tao.png)

**22. The star shape of 199 + 210j: a fixed turn per step, like a Mandelbrot orbit on the main cardioid's edge.** (`star_rotation.py`)

![The star shape of 199 + 210j: a fixed turn per step, like a Mandelbrot orbit on the main cardioid's edge.](22_star_rotation.png)


## Other flowers

**23. Sunflowers (Vogel's model) for the golden angle, 1 radian and step 210: arm counts come from continued fractions.** (`sunflowers.py`)

![Sunflowers (Vogel's model) for the golden angle, 1 radian and step 210: arm counts come from continued fractions.](23_sunflowers.jpg)

**24. Flowers of six functions: the hourglass shape is shared by every L-function with real coefficients.** (`other_flowers.py`)

![Flowers of six functions: the hourglass shape is shared by every L-function with real coefficients.](24_other_flowers.png)


## Feigenbaum and Fourier

**25. A period-doubling cascade in ζ's Newton family; the gap ratios approach Feigenbaum's δ = 4.669.** (`feigenbaum_zeta.py`)

![A period-doubling cascade in ζ's Newton family; the gap ratios approach Feigenbaum's δ = 4.669.](25_feigenbaum_zeta.png)

**26. Fourier spectra of the primes, twin primes and Collatz step counts: lines at fractions a/q.** (`prime_fourier.py`)

![Fourier spectra of the primes, twin primes and Collatz step counts: lines at fractions a/q.](26_prime_fourier.png)

**27. The 3D curve (Re ζ, Im ζ, t) along the critical line: the 'hourglass'.** (`fleurdelys_3d.py`)

![The 3D curve (Re ζ, Im ζ, t) along the critical line: the 'hourglass'.](27_fleurdelys_3d.png)


## The flower as a bouncing ball

**28. |Z(t)| bounces at each zero: phase portrait, elasticity, Gram's law, and the colliding blocks that count π.** (`zeta_bounce.py`)

![|Z(t)| bounces at each zero: phase portrait, elasticity, Gram's law, and the colliding blocks that count π.](28_zeta_bounce.png)


## Twin primes

**29. 'A circle that holds every twin prime' as a restatement, the 3-5-7 triple, and counts against Hardy–Littlewood up to 10⁸.** (`twin_circle.py`)

!['A circle that holds every twin prime' as a restatement, the 3-5-7 triple, and counts against Hardy–Littlewood up to 10⁸.](29_twin_circle.png)


## Chaos

**30. Escape regions, ζ's Euler-product floor, Lyapunov exponents, and zero spacings (GUE vs random).** (`chaos_bridges.py`)

![Escape regions, ζ's Euler-product floor, Lyapunov exponents, and zero spacings (GUE vs random).](30_chaos_bridges.png)


## Testing the targets

**31. The petal ledger: all zeros against petals through 0. Davenport–Heilbronn's deficit jumps by 2 at each off-line zero.** (`petal_ledger.py`)

![The petal ledger: all zeros against petals through 0. Davenport–Heilbronn's deficit jumps by 2 at each off-line zero.](31_petal_ledger.png)

**32. How strongly the critical line pulls Newton steps. Only Davenport–Heilbronn has pockets pushed away.** (`xi_pull.py`)

![How strongly the critical line pulls Newton steps. Only Davenport–Heilbronn has pockets pushed away.](32_xi_pull.png)

**33. The Euler product: partial products never reach 0, the 3-4-1 trick, and log-coefficients only on prime powers.** (`euler_product.py`)

![The Euler product: partial products never reach 0, the 3-4-1 trick, and log-coefficients only on prime powers.](33_euler_product.png)


## Eigenvalues

**34. The Redheffer matrix (determinant = Mertens function), its eigenvalues, and zero spacings against a random matrix.** (`eigen_rh.py`)

![The Redheffer matrix (determinant = Mertens function), its eigenvalues, and zero spacings against a random matrix.](34_eigen_rh.png)

**35. Hilbert–Pólya: w = 1 − 1/s turns the critical line into the unit circle; RH ⇔ every zero on it (Li's criterion).** (`hilbert_polya.py`)

![Hilbert–Pólya: w = 1 − 1/s turns the critical line into the unit circle; RH ⇔ every zero on it (Li's criterion).](35_hilbert_polya.png)

**36. The Collatz cycle matrix: polygon eigenvalues, Fourier eigenvectors, the cycle equation, and cycle-length bounds.** (`cycle_matrix.py`)

![The Collatz cycle matrix: polygon eigenvalues, Fourier eigenvectors, the cycle equation, and cycle-length bounds.](36_cycle_matrix.png)

**37. Zeta functions as determinants. Where RH is a theorem (graphs, curves over finite fields) it says: eigenvalues on a circle.** (`zeta_determinants.py`)

![Zeta functions as determinants. Where RH is a theorem (graphs, curves over finite fields) it says: eigenvalues on a circle.](37_zeta_determinants.png)


## The user's own figures

Two figures from the user's work on eigenspaces of Collatz cycles are kept at full size in [`../cycle_kernels/`](../cycle_kernels/), with their own README.


## Rebuilding

Run the scripts (see the main README), then `python make_gallery.py`.
