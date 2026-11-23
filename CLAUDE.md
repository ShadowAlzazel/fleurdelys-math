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
- Documents are append-only (the user's rule, session 2): extend a document or create a new one; never rewrite earlier text. Corrections go in a new section. This covers the notes, the notes from Claude, and the write-up on claude.ai.

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
| Centers in window Re −2.2..4.2, Im −2.7..2.7 | 10 of period 2 (stable); at least 109 of period 3 (random-start search, not exhaustive: single runs find 71–101) |
| ζ(½) | ≈ −1.4604 |
| Zeros up to t = 50 / 1000 | 10 / 649 |
| Closest pair among first 400 zeros | #363, #364 at 630.4739, 630.8058 (gap 24% of mean) |
| Lehmer pair | #6709, #6710 at 7005.0629, 7005.1006 (gap 0.038, petal reach 0.004) |
| Davenport–Heilbronn off-line zeros | 0.80852 + 85.69935i, 0.65083 + 114.16334i (checked to 25 digits) |

## What a geometric proof of RH must do (session 2)

Four targets, each **proven equivalent** to RH. Proving any one for ζ proves RH.

- **A. Counting:** petals through 0 up to height T equal N(T), for every T (argument principle; Turing's method checks it numerically).
- **B. Off-line slices miss 0:** for every ½ < σ < 1, t ↦ ζ(σ + it) never hits 0.
- **C. No folds:** ζ′ ≠ 0 in 0 < Re s < ½ (Speiser 1934; Levinson–Montgomery 1974).
- **D. Valley:** |ξ(σ + it)| strictly increases as σ moves away from ½ (Sondow–Dumitrescu 2010) ⇔ Re(ξ′/ξ) > 0 for Re s > ½ (Lagarias 1999). In our language: **RH ⇔ every Newton step for ξ right of the line moves left** (one line from Lagarias; an equivalence, not progress; not yet checked whether it is stated this way in the literature). Numerically: 0 of 3,240 grid points right of the line move right for t in [82, 90].

No slack, both proven: Rodgers–Tao (Λ = 0 if RH holds) and Bohr (for ½ < σ < 1 the curve comes arbitrarily close to 0). So no "safe margin" argument can work.

**The Davenport–Heilbronn test.** f(s) = ((1 − iκ)/2)·L(s, χ) + ((1 + iκ)/2)·L(s, χ̄), χ mod 5 with χ(2) = i, κ = (√(10 − 2√5) − 2)/(√5 − 1). It has the same functional-equation shape as ζ and draws a similar flower, but it has zeros off the line and no Euler product. Between t = 82 and 90 its turning predicts about 5.4 petals, 3 pass through 0, and the off-line pair accounts for the other 2. Its Newton field breaks near the off-line pair (50 grid points right of the line move right).

Consequence: any argument using only the functional equation, symmetry, petal shape, growth or general Newton/Mandelbrot dynamics also "proves" a falsehood about f. A proof must use the Euler product (the primes) somewhere. Model of a geometric argument that does: 3 + 4cos φ + cos 2φ ≥ 0 prime by prime gives no zeros on Re s = 1 (prime number theorem).

**Test for any proposed property P:** (1) ζ provably has P at all heights, (2) P implies one of A–D, (3) the Davenport–Heilbronn function lacks P. Run `davenport_heilbronn.py` side by side.

## Code

```bash
pip install -r requirements.txt
python flower.py                 # the flower, t ±50 and ±1000
python newton_plane.py           # Newton on ζ, one function
python mandelbrot_copy.py        # parameter plane zoom, one seed
python overlay.py                # flower on the parameter plane
python find_centers.py --period 3
python near_misses.py            # slow (mpmath)
python zeros.py --T 10000        # 10142 zeros, matches mpmath.nzeros; cached
python zero_polar.py             # petals in the prime-spiral layout; the zeros hear the primes
python davenport_heilbronn.py    # zeta vs a look-alike with off-line zeros (Newton field ~15 min)
# open web/flower3d.html in a browser for the 3D viewer
```

- `zeta_fast.py`: vectorized ζ. Euler–Maclaurin for Re s ≥ 0, functional equation for Re s < 0. Keep N above t/(2π); raise it for large heights.
- `newton.py`: `newton(s, c)` returns (final points, iterations, state) with state 0 = trapped in a cycle (Mandelbrot region), 1 = converged to a root, 2 = escaped.
- `web/flower3d.html`: self-contained, with its own JS ζ (Euler–Maclaurin, N = max(24, T/3)). No build step, no dependencies.
- Outputs go to `output/` (git-ignored).
- Conventions: NumPy-vectorized math, argparse options on every script, plain matplotlib. Keep scripts small and runnable on their own.

## Petals in the prime-spiral layout (session 2)

- `zeros.py`: Riemann–Siegel Z with tabulated C0, C1 (mpmath, to dodge the removable 0/0 at p = ¼, ¾ that otherwise makes fake zeros) plus mpmath below t = 300. 10142 zeros up to 10⁴, equal to mpmath.nzeros, values within ~1e-7.
- Zero γ at radius γ, angle γ: featureless, as expected (Hlawka 1975: aγ is equidistributed mod 1 for every a ≠ 0).
- Angles γ·log x lean toward π exactly when x is a prime power (Landau 1912): mean of e^(iγ log 2) is −0.0768 vs predicted −0.0769; for x = 6, 10 it is 0. The weighted sum −2π√x Σ w(γ)cos(γ log x)/∫w has a spike of height log p at every prime power up to 32 (2: 0.68 vs 0.69, 3: 1.09 vs 1.10) and ≈ 0 elsewhere. Known (Landau; explicit formula), but the clearest picture so far of the petals carrying the primes. This is the kind of property the Davenport–Heilbronn function lacks (no Euler product).

## Collatz thread (session 2, a new field; no known link to RH)

- Negatives: 3n + 1 on negatives is 3n − 1 on positives. Down to −10⁶, every start lands in one of three cycles: (−1, −2), (−5, −14, −7, −20, −10), and an 18-cycle from −17. Each takes roughly a third of starts. Conjectured: no others.
- Complex extension f(z) = (2 + 7z − (2 + 5z)cos πz)/4 (Letherman–Schleicher–Wood 1999). f′(n) = ½ (even) or 3 (odd), so an integer cycle with k odd and m even steps has multiplier 3^k/2^m = 1/∏(1 + 1/(3n)) over its odd members. That product is the classical cycle equation used for cycle-length bounds (Steiner 1977 onward). Consequence (one line): positive integer cycles are attracting, negative ones repelling.
- Observed in our code: each integer cycle has a non-integer twin cycle very close by with multiplier ≈ 2 − λ (stability flipped). Offsets: 1.5e−3 (1,4,2), 5.7e−3 (−1,−2), 6.5e−5 (−5…), 4.4e−7 (−17…). Expected from generic holomorphic dynamics (two nearby fixed points of f^p); the twins depend on the chosen extension, the integer multipliers do not.
- The 1 → 4 → 2 basin in ℂ is tiny (radius about 0.01); its repelling twin bounds it.
- **Julia copies (user's observation, confirmed).** Next to every even integer n there is a critical point of f at about n − 2/(π²(2 + 5n)) (−1.97401 next to −2). It is captured by the nearby attracting cycle, so f∘f near the twin of (−1, −2) is quadratic-like (Douady–Hubbard). The twin's basin matches the filled Julia set of z² + c, c = λ/2 − λ²/4 = 0.18719, on 99.4% of pixels after only shifting, scaling and mirroring. The integer −1 sits exactly at the tip, playing the role of the β fixed point: 2β = 1.50126 vs multiplier 3/2. The integer cycle and its twin are the two fixed points of that quadratic (multipliers sum ≈ 2). Expected from Douady–Hubbard; same mechanism as the Mandelbrot copies in the ζ(s) − c family.
- **Steps plot structure (prime-spiral analogy).** Curves: steps(2n) = steps(n) + 1 (0 exceptions off the cycles up to 10⁵), so doubling chains trace log₂ curves. Dashes: 8k + 4 and 8k + 5 merge after 3 steps for every integer k (100% in data), and in general the first m moves depend only on n mod 2^m (Terras 1976). The mod-8 statistics are nearly identical for positive and negative n (46.0% vs 46.6% of consecutive pairs equal). Like the 3Blue1Brown prime spirals: residue classes seen through a smooth coordinate. Known, not new.
- Prime-spiral layout (`collatz_polar.py`): the arms are the layout (2π ≈ 44/7), not Collatz. Negatives' cycle choice is nearly independent of n mod 6 and mod 44 (shares 29–37% per class). Nearby numbers share a cycle more often than chance: 60.6% at distance 1, 38.5% at 44, 33.7% at 1000 vs 33.4% baseline, decaying smoothly with no spike at 44, 710 or 1024. Numerical observation, likely from orbits merging (as 8k + 4 and 8k + 5 do).
- Parallel with the Davenport–Heilbronn test: the negative integers follow the same rule but have extra cycles, so a proof for the positive integers must use something that fails for the negatives (the sign in ∏(1 + 1/(3n)) is one place it enters).

## Open threads

- [ ] The user's core observation about the flower (not yet revealed)
- [ ] Which zero of ζ″ is the canonical seed, or how to combine all of them
- [ ] What in the 4D picture singles out Re(s) = ½. The parameter plane only sees values of ζ, not which s produced them. Newton for ξ (not ζ) does see it: the line is invariant, and RH ⇔ the line pulls from both sides (target D).
- [ ] Any observation must pass the Davenport–Heilbronn test (it must use the primes).
- [ ] The user's fuller picture of Fleurdelys, beyond what is drawn so far
- [ ] The user's own Collatz patterns for negative and complex numbers (not yet revealed)
- [ ] Julia copies next to the 18-cycle at −17 (twin only 4·10⁻⁷ away)
- [ ] Why nearby numbers share a cycle: does orbit merging explain the whole decay curve?
- [ ] Is "Newton for ξ moves toward the line" stated in this form in the literature?
- [ ] Zero spectrum for the Davenport–Heilbronn function (expect no clean prime spikes)

## Session log

- Session 1 (Nov 22, 2026): the flower, Newton on ζ, Mandelbrot copies, 3D viewer. Notes from the start through "Code".
- Session 2 (Nov 23, 2026): proof targets, the Davenport–Heilbronn test, the petal spectrum, Collatz. See "Session 2" at the end of `Fleurdelys notes on the zeta flower.md`, "Session 2 note" in `A note from Claude Fleurdelys.md`, and the same section appended to the write-up on claude.ai.
- Session 2, continued (Nov 23, 2026): Julia copies next to the negative Collatz cycles (return-map degree 2^m: 2, 8, 2048), Julia copies around the flower (it crosses Mandelbrot copies at t = 24.11, 37.38, …; basilica at c = 0.852809 − 0.604099i, rabbit at 0.829974 − 0.608302i), `Observation checklist.md` and `lookalikes.py` (run any property on ζ, L(s, χ₄), Davenport–Heilbronn).

## Before the user shares the observation

Use `Observation checklist.md`: one-sentence statement, its kind, known-equivalent check, circularity, the two-sided look-alike test with `lookalikes.py` (must fail for DH, should hold for L(s, χ₄)), no margin, all heights, where the primes enter, literature. Then draw it for all three functions side by side.
- Session 2, continued again (Nov 23, 2026): petals in every spiral view. Twin primes take their own arms (mod 6: smaller twin 5, larger 1; mod 44: each avoids 2 of the 20 prime arms). Petals and twin petals (gap < 0.3 × average; 164 pairs up to 10⁴) show no arms. Consecutive zero gaps correlate −0.369. Spectrum with 35,673 zeros up to 30,000: all 35 prime powers ≤ 100 within 0.075 of log p, non-prime-powers below 0.042; twin primes get no special spike. Critical strip wrapped onto the spiral r = θ (top view) and unrolled with Z(t) (side view). Scripts: `petal_spiral.py`, `petal_spectrum.py`, `strip_spiral.py`.
- Pair spacing and spectroscopy (Nov 23, 2026; the user works with Fourier transforms): form factor of 35,644 zeros rises (slope 1.06) and is flat after τ = 1 (1.000 ± 0.021): prime pairs collectively (Montgomery; Goldston–Montgomery; Bogomolny–Keating), not twin primes alone. Spike at τ = 1.000 from Gram's law; spikes at 1.09 and 1.23 real but unexplained. Spectrogram of Z(t) shows one chirp per integer n. Prime wave over subsets (X = 2·10⁶, 29 zeros ≤ 100): twin +3.8 sd, cousin +2.5, sexy +3.1 above matched random; isolated primes −7.6 sd (inverted). Heuristic: clustering amplifies, isolation inverts. Scripts: `pair_spacing.py`, `zeta_spectroscopy.py`, `prime_subsets.py`.
- New open threads: explain the τ = 1.09 and 1.23 spikes (try the Bogomolny–Keating formula); test the clustering heuristic for the prime-subset strengths at other X and more zeros; literature check for that experiment.
- Green–Tao and twin primes vs RH (Nov 23, 2026): the user asked whether proving twin primes "appear on the petals" and are infinite would prove the twin prime conjecture while leaving RH open. Answer given: independence is right as far as known; a property of twin primes doesn't give infinitude; the petals already hear every prime (Landau, proven); RH is about zeros. `green_tao.py`: first k-term prime progressions (k = 3..12), counts vs the Green–Tao–Ziegler asymptotic (ratios 0.970 for 3-term, 0.964 for 4-term at N = 2·10⁵). C₃ = 1.32032 = 2 × twin constant; progressions have two free variables, twin primes one (parity problem / infinite complexity).
- The star shape (Nov 23, 2026): the user saw that 199 + 210j in the spiral layout looks like a Mandelbrot single-seed orbit (3Blue1Brown, Ben Sparks). Same geometry: fixed turn per step (0.4225 vs 0.4226 turns at c = −0.48 + 0.35i). Turn angles map to the main cardioid's edge, c = e^{iθ}/2 − e^{2iθ}/4; step 210 lies between the 2/5 and 3/7 bulbs. Geometry, not number theory. `star_rotation.py`.

