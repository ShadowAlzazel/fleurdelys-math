# CLAUDE.md: Fleurdelys

Context for Claude when working in this repo. It carries over a long conversation (Nov 22, 2026) in which the user walked Claude through years of their own exploration of the Riemann zeta function.

Full write-up with pictures, tables of theorems and conjectures, and a step-by-step journey log:
https://claude.ai/artifact/RKDz6r8cJttnH1ExQXeryx

## What this project is

A personal geometry playground around ζ(s). It is **not** a proof of the Riemann Hypothesis, and the user knows that. The user is retracing a journey step by step toward an observation they have not revealed yet. Let them lead.

"Fleurdelys" is the user's name for the full 4D object: the graph of ζ over the critical strip, the pairs (s, ζ(s)) in ℂ². The "flower" is the image of the critical line, t ↦ ζ(½ + it), which is the shadow of one slice of that object.

## How to work with the user

- They know some holomorphic dynamics and analytic continuation, but have no formal training in writing proofs. Explain clearly, without condescending.
- They think visually and are very good at imagining 4D motion. Default to making pictures (PNG via matplotlib, or interactive HTML) over long prose.
- Be an honest colleague, not a fan. For each idea, say whether it is already known (and by whom), new, or breaks under scrutiny. Never imply RH is close to being proven.
- Keep three things separate: proven theorems, open conjectures, and numerical observations from our code.
- Check numbers before stating them. `zeta_fast.py` should be cross-checked against `mpmath` when accuracy matters.
- When a request is ambiguous (for example "iterate"), take the likeliest reading, say which one you took, and offer the alternative.

## Math context, compressed

- On the critical line: ζ(½ + it) = Z(t)·e^(−iθ(t)). Z is the real Hardy Z-function and θ the Riemann–Siegel theta. The flower is a polar curve turning clockwise.
- Petals are near-circles: the leading terms 1 + e^(−2iθ) trace the circle of radius 1 centered at 1, through 0. Higher terms of the approximate functional equation wobble it.
- Every zero on the line is a petal through the origin. Petals up to height T ≈ θ(T)/π + 1, which matches the Riemann–von Mangoldt count N(T) up to S(T).
- Blooming speed: about (1/2π)·log(t/2π) petals per unit height.
- RH restated: the flower never misses a petal (Turing's method checks this numerically).
- Off the line (σ ≠ ½), the curve skims past 0 without touching it, at every height checked.
- Newton family for ζ(s) − c: the free critical points are the zeros of ζ″, independent of c. The parameter c lives in the same plane as the flower.
- Relevant theorems: Speiser (RH ⇔ ζ′ has no zeros in 0 < Re s < ½), Bohr density, Voronin universality, Bagchi (RH ⇔ strong recurrence), Rodgers–Tao (Λ ≥ 0), McMullen (Mandelbrot set is universal), Douady–Hubbard, Tan Lei, Curry–Garnett–Sullivan, Ghys (Lorenz knots).

## Key numbers

| Quantity | Value |
| --- | --- |
| Default seed w (a zero of ζ″) | −0.35508 + 3.59084i |
| Another zero of ζ″ (real axis) | −3.59577 |
| Critical value ζ(w), the hub where basins meet | 0.43166 + 0.09786i |
| First Mandelbrot copy (period-2 center) | c ≈ −0.43193 + 0.46305i, about 0.03 across |
| Other period-2 centers | −0.0316 − 0.3925i, 0.8361 − 0.5916i, 1.3097 + 0.8523i, … (`find_centers.py`) |
| Centers in window Re −2.2..4.2, Im −2.7..2.7 | 10 of period 2, 76 of period 3 |
| ζ(½) | ≈ −1.4604 |
| Zeros up to t = 50 / 1000 | 10 / 649 |
| Closest pair among first 400 zeros | #363, #364 at 630.4739, 630.8058 (gap 24% of mean) |
| Lehmer pair | #6709, #6710 at 7005.0629, 7005.1006 (gap 0.038, petal reach 0.004) |

## Code

```bash
pip install -r requirements.txt
python flower.py                 # the flower, t ±50 and ±1000
python newton_plane.py           # Newton on ζ, one function
python mandelbrot_copy.py        # parameter plane zoom, one seed
python overlay.py                # flower on the parameter plane
python find_centers.py --period 3
python near_misses.py            # slow (mpmath)
# open web/flower3d.html in a browser for the 3D viewer
```

- `zeta_fast.py`: vectorized ζ. Euler–Maclaurin for Re s ≥ 0, functional equation for Re s < 0. Keep N above t/(2π); raise it for large heights.
- `newton.py`: `newton(s, c)` returns (final points, iterations, state) with state 0 = trapped in a cycle (Mandelbrot region), 1 = converged to a root, 2 = escaped.
- `web/flower3d.html`: self-contained, with its own JS ζ (Euler–Maclaurin, N = max(24, T/3)). No build step, no dependencies.
- Outputs go to `output/` (git-ignored).
- Conventions: NumPy-vectorized math, argparse options on every script, plain matplotlib. Keep scripts small and runnable on their own.

## Open threads

- [ ] The user's core observation about the flower (not yet revealed)
- [ ] Which zero of ζ″ is the canonical seed, or how to combine all of them
- [ ] What in the 4D picture singles out Re(s) = ½. The parameter plane only sees values of ζ, not which s produced them.
- [ ] The user's fuller picture of Fleurdelys, beyond what is drawn so far
