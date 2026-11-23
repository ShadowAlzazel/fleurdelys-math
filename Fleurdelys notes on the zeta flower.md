# Fleurdelys: notes on the zeta flower

Nov 22, 2026 · @ShadowAlzazel

## Where this comes from

These notes record a personal exploration of the Riemann zeta function, built up over years and retraced here step by step. It is a journey through pictures, not yet a proof attempt. The main observation is still to come.

The path so far:

1. Playing in code with the Lorenz attractor and the Mandelbrot set.
2. Looking for Mandelbrot shapes inside other dynamical systems, especially the parameter space of Newton's method.
3. Going back to the critical strip, inspired by 3Blue1Brown's picture of ζ on the critical line.
4. Seeing the image of the critical line as a flower whose petals all meet at the origin.
5. Lifting the flower into 3D and 4D, counting petals, and looking at near misses and twin petals.

Inspiration: David Smith, the hobbyist who found the aperiodic "hat" tile and then worked with professional mathematicians to prove it.

## Journey log

The conversation that produced these notes, step by step (November 22, 2026). Each row is what was asked or imagined, then what came out of it.

| Step | Idea or question | What we found |
| --- | --- | --- |
| 1 | Wanting to try an old idea on RH, believing a true theorem must have an elegant proof | Agreed to stress-test it honestly. Elegance is not guaranteed: the four color theorem and the classification of finite simple groups have huge proofs. |
| 2 | Background in holomorphic dynamics and analytic continuation; code experiments with the Lorenz attractor and the Mandelbrot set | Mapped the known bridges: Ghys (Lorenz knots are modular knots), dynamical zeta functions (Smale, Ruelle, Selberg), Deninger, Hilbert–Pólya and quantum chaos, Newton's method on ζ. |
| 3 | Finding Mandelbrot shapes inside other dynamical systems, like Newton's method parameter space | Known and explained: Curry–Garnett–Sullivan (1983), Douady–Hubbard polynomial-like maps, McMullen's universality. ζ alone has no parameter, so one must be added. |
| 4 | What shape does the critical line make under ζ? (3Blue1Brown) | Computed it for t from 0 to 35: clockwise loops through the origin. Polar form Z(t)·e^(−iθ(t)); Gram crossings mostly positive. |
| 5 | 3Blue1Brown's 2×2 grid (seed vs. function) and the 4D shape where Julia and Mandelbrot sets meet | Drew Newton on ζ (one function) and the parameter plane of ζ(s) − c seeded at a zero of ζ″ (one seed). Found a Mandelbrot copy at c ≈ −0.432 + 0.463i. Both pictures are slices of one 4D object, the pairs (c, s). |
| 6 | Start from very negative to very large t and see the full shape | The symmetric flower. Petals are near-circles because the leading terms 1 + e^(−2iθ) trace the circle of radius 1 centered at 1. |
| 7 | Naming the full 4D shape | Fleurdelys: the graph of ζ over the strip, in ℂ². RH restated: the surface meets ζ = 0 only above Re(s) = ½. |
| 8 | Plot the flower in 4D; what is the blooming speed? | 3D view with t as height and a slider for σ (the 4th dimension). Petals bloom at about (1/2π)·log(t/2π) per unit height. RH: the flower never misses a petal (Turing's method checks this). |
| 9 | How many petals from the side? | 10 touches up to t = 50 (9 full petals plus an opening arc); 649 zeros up to t = 1000. |
| 10 | The near misses, and twin primes vs. twin petals | Closest early pair: zeros #363 and #364 near t = 630.5. Lehmer pair at t ≈ 7005.06 reaches only 0.004 from the origin. Rodgers–Tao: RH, if true, is barely true. Twin primes shape petal pairing only statistically (Montgomery; Bogomolny–Keating). |
| 11 | Write down everything so far | This document. |
| 12 | Close the loop in 4D and map attracting points and Mandelbrot regions on it | The parameter c lives in the same plane as the flower. Overlay: all basins meet at the critical value ζ(w) ≈ 0.43 + 0.10i, not at 0. 10 period-2 and 76 period-3 centers sit on basin borders. Closed 3D loop hits the axis 20 times for t from −50 to 50. |
| 13 | Run it locally | A repo with Python scripts for every picture and a standalone 3D viewer page. |
| 14 | Keep the context alive | This log, plus a CLAUDE.md file in the repo for coding sessions. |

## The flower

The image of the critical line Re(s) = ½ under ζ is a flower of near-circles. Every petal passes through the origin, and each pass is a zero of ζ.

The functional equation splits ζ on the line into a real length times a turning direction:

```latex
\zeta\left(\tfrac12 + it\right) = Z(t)\, e^{-i\theta(t)}
```

Z(t) is the Hardy Z-function (real valued). θ(t) is the Riemann–Siegel theta function, an angle that keeps increasing. So the flower is a polar curve: a clockwise-turning arrow whose signed length is Z(t).

The petals are near-circles because of the approximate functional equation. Keeping only its n = 1 terms gives 1 + e^(−2iθ(t)), the circle of radius 1 centered at 1, which passes exactly through 0. The n = 2, 3, … terms wobble that circle, changing its size and moving its center.

What the picture shows:

- Zeros are clean pass-throughs. When Z changes sign, the curve crosses the origin with nonzero speed.
- Gram points are where θ(t) = nπ, so ζ is real there. Usually the crossing is on the positive side (Gram's law). All 13 Gram points checked from t ≈ 9.67 to 57.55 were positive.
- Mirror symmetry: ζ(s̄) is the conjugate of ζ(s), so negative t traces the same petals reflected across the real axis.
- The big left loop is the stretch near t = 0, through ζ(½) ≈ −1.46. Above it the petals stay mostly right of the origin, swinging around 1, the average value of ζ on the line.
- Seen end-on the flower is flat. Seen from the side, with t as height, each petal gets its own height band.

&#91;image: The zeta flower: zeta(1/2 + it) for t from -50 to 50 (top) and from -1000 to 1000 (bottom). Orange is 0, green is 1.\]

## Function map

Each part of the flower is controlled by a specific function.

| Function | Part of the flower it controls |
| --- | --- |
| θ(t), Riemann–Siegel theta | The turning of the petals and the blooming speed. It turns at about ½·log(t/2π) per unit t. |
| Z(t), Hardy Z-function | The signed petal size. Each sign change is a petal touching the origin. |
| χ(s), factor in the functional equation | Makes the critical line special: χ has absolute value 1 on it, so ζ is real up to a rotation there. χ(½ + it) = e^(−2iθ(t)). |
| 1 + e^(−2iθ), leading terms | The base circle: radius 1, center 1, through the origin. |
| n ≥ 2 terms of the approximate functional equation | The wobble: petal sizes and centers drifting from the base circle. |
| Gram points, θ(t) = nπ | Where the curve crosses the real axis, usually on the positive side. |
| N(T), Riemann–von Mangoldt formula | Total number of zeros up to height T, about (T/2π)·log(T/2π) − T/2π + 7/8. |
| S(T) = (1/π)·arg ζ(½ + iT) | The small wobble between the smooth petal count and the true count. |
| Conjugate symmetry, ζ(s̄) = conjugate of ζ(s) | The mirror half of the flower (negative t). |
| ζ′(s) | The speed at which a petal passes through the origin. Its zeros are critical points (Speiser's theorem). |
| ζ″(s) | Its zeros are the free critical points (seeds) of the Newton family for ζ(s) − c. |
| N\_c(s) = s − (ζ(s) − c)/ζ′(s), Newton map | Basins of the zeros and the Mandelbrot copies in parameter space. |
| ζ(σ + it) for σ ≠ ½ | Nearby curves that skim past the origin without touching it (at every height checked). |
| Riemann's explicit formula | The primes: each zero adds a wave of roughly cos(γ·log x), and the primes are the interference of all petals together. |

## Experiments and numbers

Everything here was computed numerically (mpmath, plus a fast Euler–Maclaurin ζ checked against mpmath). These are observations, not proofs.

### Newton's method on ζ (one function, pixel = seed)

Each starting point is colored by the zero it converges to. Window: Re(s) from −6 to 6, Im(s) from 0 to 26.

- Large basins belong to the first zeros (14.13, 21.02, 25.01) and to the trivial zeros at −2, −4, …
- A large region to the right never converges. There ζ flattens toward 1 and has no roots, so orbits drift right forever. Polynomial Newton maps don't do this.

&#91;image: Newton's method on zeta. Each pixel is a starting point, colored by the zero it reaches. White dots are the first three zeros on Re(s) = 1/2. Dark: orbits that drift off to the right.\]

### Newton parameter plane for ζ(s) − c (one seed, pixel = c)

The family ζ(s) − c is the analog of z² + c. Its Newton map N\_c has free critical points at the zeros of ζ″, which do not depend on c.

- Seed: w ≈ −0.35508 + 3.59084i, a zero of ζ″ (another is on the real axis at −3.59577).
- Period-2 centers (c where w is periodic) include −0.43193 + 0.46305i, −0.03158 − 0.39254i and 0.83605 − 0.59158i.
- A clean Mandelbrot copy sits at c ≈ −0.432 + 0.463i, roughly 0.03 across.
- Expected from McMullen's universality theorem, so this confirms the setup rather than finding something new.

&#91;image: Mandelbrot copy in the parameter plane of Newton's method for zeta(s) - c, seeded at a zero of zeta''. Window: c within 0.02 of -0.432 + 0.463i. Black: the seed is trapped in a cycle.\]

### The flower in 3D and 4D

The graph of ζ, the pairs (s, ζ(s)), lives in ℂ², which is 4 real dimensions. On the critical line Re(s) is fixed at ½, so that slice is a 3D curve: height t, plus Re ζ and Im ζ. The 4th coordinate, Re(s) = σ, was explored with a slider.

- At σ = ½, the curve hits the axis ζ = 0 exactly 10 times for t from 0 to 50, giving 9 complete petals plus an opening arc.
- At every other σ tried, the curve skims past the axis without touching it.
- Looking down the t-axis collapses the 3D corkscrew into the flat flower.

### Petal counts and blooming speed

- Petals up to height T: about θ(T)/π + 1, the same as the Riemann–von Mangoldt count up to S(T).
- Blooming rate: about (1/2π)·log(t/2π) petals per unit height.
- Counted: 10 zeros up to t = 50 and 649 up to t = 1000.

### Near misses (twin petals)

| Zeros | Heights | Gap | Gap vs. mean spacing | Petal reach from origin |
| --- | --- | --- | --- | --- |
| #363, #364 | 630.4739, 630.8058 | 0.332 | 24% | 0.097 |
| #315, #316 | 564.1609, 564.5061 | 0.345 | 25% | 0.125 |
| #6709, #6710 (Lehmer pair) | 7005.0629, 7005.1006 | 0.038 | 4% | 0.004 |

The first two are the closest pairs among the first 400 zeros. Petal reach is the largest value of Z(t) between the two zeros. Typical petals at these heights reach about 1 to 3.

### The flower on the parameter plane

The parameter c of ζ(s) − c lives in the same plane as the flower: both are values of ζ. So the flower can be drawn directly on the Newton parameter plane.

- All colored basins spiral together at the critical value ζ(w) ≈ 0.4317 + 0.0979i. At that c the seed is itself a root, the analog of the center c = 0 of the Mandelbrot set. It sits among the petals near 1, not at the origin where the petals meet.
- In the window Re(c) from −2.2 to 4.2, Im(c) from −2.7 to 2.7: 10 period-2 centers and at least 109 period-3 centers (the earlier figure of 76 came from a single random-start search, which is not exhaustive). They lie along the fractal borders between basins, with no visible pattern relative to the petals or the origin.
- Gray region: the seed's orbit escapes to infinity. The big outer petals pass through it.
- Closing the loop in 3D: with t from −50 to 50 the curve hits the axis 20 times (10 zeros and their mirrors) and joins through ζ(½) ≈ −1.46 at t = 0.

Two caveats. The overlay depends on the seed: ζ″ has infinitely many zeros, each with its own parameter picture. And the parameter plane only sees values of ζ, not which s produced them, so nothing in it singles out Re(s) = ½ yet.

&#91;image: The flower (dark line, t from -50 to 50) on the Newton parameter plane for zeta(s) - c. Black dot: 0. Green star: the critical value zeta(w). Orange circles: period-2 Mandelbrot centers. Pink squares: period-3 centers. Gray: the seed's orbit escapes.\]

## What is proven

These results are theorems, and each one came up along the way.

| Result | Who, when | What it says for the flower |
| --- | --- | --- |
| Functional equation | Riemann, 1859 | ζ(s) = χ(s)·ζ(1 − s). It gives the polar form Z(t)·e^(−iθ(t)) on the critical line. |
| Infinitely many zeros on the line | Hardy, 1914 | The flower has infinitely many petals. |
| A positive proportion of zeros on the line | Selberg (1942), Levinson (1974), Conrey (1989) | At least 40% of zeros are proven to be petals (Conrey's bound). |
| Riemann–von Mangoldt formula | von Mangoldt, 1905 | Counts all zeros up to height T: the expected number of petals. |
| Turing's method and large verifications | Turing (1953); Platt and Trudgian (2021) | Petal count matches the zero count up to height 3·10¹². |
| Speiser's theorem | Speiser, 1934 | RH is equivalent to ζ′ having no zeros in 0 < Re(s) < ½. |
| Bohr's density theorem | Bohr, 1910s | For ½ < σ < 1, the image of the line Re(s) = σ is dense in the plane. |
| Voronin universality | Voronin, 1975 | Shifts of ζ in the strip ½ < Re(s) < 1 approximate any non-vanishing analytic function. |
| Bagchi's theorem | Bagchi, 1981 | RH is equivalent to ζ approximating its own shifts (strong recurrence). |
| De Bruijn–Newman constant is at least 0 | Rodgers and Tao (2018 preprint, 2020) | RH is equivalent to Λ ≤ 0, so if RH holds, Λ = 0 exactly. "RH, if true, is barely true." |
| Lehmer's near-miss pair | Lehmer, 1956 | A twin petal at t ≈ 7005 that barely touches the origin. |
| Mandelbrot copies in Newton's method | Curry, Garnett and Sullivan, 1983 | Small Mandelbrot sets appear in the parameter space of Newton's method for cubics. |
| Polynomial-like maps | Douady and Hubbard, 1985 | Explains why Mandelbrot copies appear: local quadratic-like behavior. |
| The Mandelbrot set is universal | McMullen, 2000 | Mandelbrot copies appear in essentially every holomorphic family with this behavior. |
| Similarity of M and Julia sets | Tan Lei, 1990 | At Misiurewicz points, zooming into M and into the matching Julia set gives the same picture. |
| Lorenz knots are modular knots | Ghys, 2006–2007 | Ties the Lorenz attractor to the modular group and number theory. |

## What is open

None of these is proven. Each one touches the flower.

| Open problem | Kind | What it would mean for the flower |
| --- | --- | --- |
| Riemann Hypothesis | Hypothesis (Riemann, 1859) | Every nontrivial zero is a petal. The flower never misses one. |
| Lindelöf hypothesis | Hypothesis (implied by RH) | Petals grow slower than any power of t. |
| Simple zeros conjecture | Conjecture | Every petal crosses the origin at nonzero speed, so no zero is repeated. |
| Montgomery pair correlation | Conjecture (1973) | Petals repel like eigenvalues of random matrices (GUE), so twin petals are rare. |
| Hilbert–Pólya idea | Open program | The petal heights are the energy levels of some self-adjoint operator. |
| Deninger's program | Open program | A dynamical system whose periodic orbits play the role of the primes. |
| Twin prime conjecture | Conjecture | Infinitely many primes p with p + 2 also prime. |
| Hardy–Littlewood prime-pair (k-tuple) conjectures | Conjecture | Predicted counts of twin primes and other prime patterns. Bogomolny and Keating used them in the mid-1990s to derive the fine structure of how petals pair up (a heuristic derivation). |

Two things that look like conjectures but are not:

- Gram's law (Gram crossings land on the positive side) is a rule of thumb. It is known to fail, more often as t grows.
- The Mandelbrot copy in the ζ(s) − c family is a numerical observation, and universality theory explains why copies like it appear.

## Fleurdelys

Fleurdelys is the name for the full 4D shape behind the flower: the graph of ζ over the critical strip, the pairs (s, ζ(s)) in ℂ². The flower is the shadow of one slice of it, the slice above Re(s) = ½, seen down the t-axis.

In this language, RH says two equivalent things:

- The surface meets the plane ζ = 0 only above the line Re(s) = ½.
- The flower never misses a petal: the petals counted through the origin always match N(T), the total number of zeros up to that height.

A zero off the line would come with a mirror partner. It would show up as two petals the flower should have grown but didn't.

These are restatements, not proofs. A proof needs a reason why the blooming can never skip a petal at any height, including near-misses like the Lehmer pair.

The full Fleurdelys imagined in these notes goes beyond what is drawn here. The next step is the observation that the journey has been building toward.

What comes next:

- [ ] Describe the core observation about the flower
- [ ] Check it numerically
- [ ] Compare it with the known results above
- [ ] Decide which seed (zero of ζ″) is canonical, or combine all of them
- [ ] Find what in the 4D picture singles out the line Re(s) = ½

## Code

Everything here can be reproduced locally from the fleurdelys repo (delivered as fleurdelys.zip). It needs Python 3.9+ with numpy, scipy, matplotlib and mpmath.

| File | What it does |
| --- | --- |
| web/flower3d.html | Standalone 3D viewer: σ slider, closed loop, t range up to ±200, Mandelbrot floor. Opens in any browser, offline. |
| zeta\_fast.py | Vectorized ζ (Euler–Maclaurin plus the functional equation). |
| newton.py | Newton iteration for ζ(s) − c, the default seed w and coloring. |
| flower.py | The flower for any t range. |
| newton\_plane.py | Newton on ζ, colored by which zero each start reaches. |
| mandelbrot\_copy.py | Zooms into the parameter plane at any center and radius. |
| find\_centers.py | Lists Mandelbrot-copy centers of a given period. |
| overlay.py | The flower on the parameter plane with centers marked. |
| near\_misses.py | Closest zero pairs and the Lehmer pair. |
| CLAUDE.md | Context for continuing this work in a coding session. |
