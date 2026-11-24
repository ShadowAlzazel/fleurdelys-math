# Fleurdelys

Pictures of the Riemann zeta function: the flower traced by the critical line, Newton's method on ζ, and Mandelbrot copies in its parameter plane.

This is a personal geometry playground, not a proof of anything.

## Setup

Needs Python 3.9 or newer.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## The 3D viewer (no Python needed)

Open `web/flower3d.html` in any browser. It runs entirely offline.

- Drag to rotate. "Look down the axis" collapses the 3D corkscrew into the flat flower.
- The σ slider moves off the critical line (the 4th dimension). Only σ = ½ hits the axis.
- The t-range slider goes up to ±200.
- The floor shows the flower's shadow, period-2 Mandelbrot centers and the critical value ζ(w).

## The scripts

Each one saves a PNG into `output/`. Run any with `--help` to see its options.

| Script | What it draws | Typical time |
| --- | --- | --- |
| `flower.py` | ζ(½ + it) for t from −50 to 50 and −1000 to 1000 | seconds |
| `newton_plane.py` | Newton's method on ζ: each starting point colored by the zero it reaches | ~15 s |
| `mandelbrot_copy.py` | Parameter plane of Newton for ζ(s) − c, zoomed on a Mandelbrot copy | ~1–2 min |
| `overlay.py` | The flower drawn on that parameter plane, with Mandelbrot centers marked | ~30 s |
| `find_centers.py` | Prints centers of Mandelbrot copies (c values where the seed is periodic) | ~10 s |
| `near_misses.py` | Closest pairs of zeros ("twin petals") and the Lehmer pair | ~1 min |
| `collatz_negative.py` | Collatz on −N … N: which cycle each start falls into, and how many steps it takes | seconds |
| `collatz_complex.py` | Collatz extended to ℂ by f(z) = (2 + 7z − (2 + 5z)cos πz)/4: basins, escape, zooms at 0, 1, −1, −5 | seconds |
| `collatz_twins.py` | The non-integer "twin" cycle next to each integer cycle, with flipped stability | seconds |
| `collatz_julia.py` | The orange basin next to −1 vs the filled Julia set of z² + 0.1872: they match after shifting, scaling and mirroring | ~1 min |
| `collatz_structure.py` | Why the steps plot has curves (doubling chains) and dashes (8k + 4 and 8k + 5 always merge) | seconds |
| `collatz_polar.py` | Collatz in the prime-spiral layout (radius \|n\|, angle n): primes, positives by steps, negatives by cycle | ~30 s |
| `zeros.py` | All zeros of ζ on the line up to height T (Riemann–Siegel + mpmath below 300), cached in `output/` | ~15 s for T = 10000 |
| `zero_polar.py` | The petals in the prime-spiral layout, angles γ·log x, and the spectrum where the zeros reproduce the primes (Landau) | ~10 s |
| `collatz_julia_cycles.py` | Julia copies next to the −1, −5 and −17 cycles: return maps of degree 2, 8 and 2048 | ~4 min |
| `zeta_julia.py` | The Mandelbrot copy the flower crosses, and the basilica and rabbit in the s-plane | ~4 min |
| `lookalikes.py` | Runs any property on ζ, L(s, χ₄) and Davenport–Heilbronn (the test in `Observation checklist.md`) | ~15 s |
| `petal_spiral.py` | Primes, twin primes, petals and twin petals in the prime-spiral layout, two scales | ~20 s |
| `petal_spectrum.py` | The zero spectrum up to x = 100 with twin primes marked (needs `python zeros.py --T 30000`) | ~40 s |
| `strip_spiral.py` | The critical strip wrapped onto the spiral (top view) and unrolled with Z(t) (side view) | ~5 s |
| `pair_spacing.py` | Pair correlation of the zeros and its Fourier transform (form factor) against random-matrix theory | ~5 s |
| `zeta_spectroscopy.py` | Spectrogram of Z(t); the prime wave over all primes, twin primes and a random control | ~1 min |
| `prime_subsets.py` | Which primes hear the zeros: twin, cousin, sexy, isolated vs matched random primes | ~3 min |
| `green_tao.py` | First progressions of k primes (k = 3..12) in the spiral, and counts against the proven Green–Tao–Ziegler formula | ~5 s |
| `star_rotation.py` | Why a prime progression in the spiral looks like a Mandelbrot orbit: both turn by a fixed angle | ~5 s |
| `sunflowers.py` | Sunflowers for three turn angles; arm counts from continued fractions | ~5 s |
| `other_flowers.py` | The flower of six functions (ζ, L(χ₄), Gaussian-integer zeta, Davenport–Heilbronn, a complex character, ζ off the line) | ~5 min |
| `fleurdelys_3d.py` | The 3D hourglass (Re F, Im F, t) for six functions, and ζ's σ-slices (4D) | ~2 min |
| `feigenbaum_zeta.py` | Period-doubling cascade in ζ's Newton family on the real line; gap ratios approach Feigenbaum's 4.6692 | ~10 min |
| `prime_fourier.py` | Fourier spectra of primes, twin primes and Collatz step counts, with predicted line heights | ~5 s |
| `zeta_bounce.py` | The flower as a bouncing ball: bounces, phase portrait, elasticity, phase lag S(t), Selberg's law, colliding blocks and π | ~10 s |
| `twin_circle.py` | A circle around the twin primes: the restatement, the 3-5-7 triple, counts against Hardy–Littlewood up to 10⁸ | ~5 s |
| `davenport_heilbronn.py` | ζ's flower next to the Davenport–Heilbronn function, a look-alike with zeros off the line; Newton step direction for both completed functions | flowers seconds, Newton field ~15 min |

Examples:

```bash
python flower.py --T 200
python mandelbrot_copy.py --center 0.83605 -0.59158 --radius 0.03
python mandelbrot_copy.py --center 1 0 --radius 4 --size 300     # wide view
python find_centers.py --period 3
python newton_plane.py --ext -4 4 0 40 --height 1000
```

## Files

- `zeta_fast.py`: vectorized ζ for NumPy (Euler–Maclaurin, plus the functional equation for Re(s) < 0). Accurate to about 1e-10 at moderate heights; raise `N` for large t (N should exceed t / 2π).
- `newton.py`: Newton iteration for ζ(s) − c, the default seed, and coloring helpers.
- `SEED` in `newton.py` is w ≈ −0.35508 + 3.59084i, a zero of ζ″. It is a free critical point of the Newton map for ζ(s) − c. Other zeros of ζ″ give other parameter pictures; −3.59577 on the real axis is another one.

## Key numbers

- First Mandelbrot copy found: c ≈ −0.432 + 0.463i, about 0.03 across.
- Critical value ζ(w) ≈ 0.4317 + 0.0979i: the hub where all basins meet in the parameter plane.
- Zeros up to t = 50: 10. Up to t = 1000: 649.
- Lehmer pair: t ≈ 7005.0629 and 7005.1006, gap 0.038 (about 4% of normal spacing).
