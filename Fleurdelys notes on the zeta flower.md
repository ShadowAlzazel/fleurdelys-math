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
- In the window Re(c) from −2.2 to 4.2, Im(c) from −2.7 to 2.7: 10 period-2 centers and 76 period-3 centers. They lie along the fractal borders between basins, with no visible pattern relative to the petals or the origin.
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

## Session 2 (Nov 23, 2026)

Session 2 turned "what would a proof need?" into four precise targets and one test. It then took the same tools to a new field, the Collatz problem. This is still a journey through pictures, not a proof attempt. Everything above is kept as written; corrections are listed here.

**Correction.** The "76 period-3 centers" in the parameter-plane section came from one random-start search, which is not exhaustive. Repeated searches find at least 109 in that window (single runs find 71 to 101). The count of 10 period-2 centers is stable.

### Journey log, continued

| Step | Idea or question | What we found |
| --- | --- | --- |
| 15 | Run every script in the new environment | All run. The fast ζ matches mpmath to about 9 digits. Found the period-3 count correction above. |
| 16 | What must be proven geometrically? Inspired by Calcea Johnson and Ne'Kiya Jackson's high-school trigonometric proofs of Pythagoras | Four targets, each proven equivalent to RH. Two theorems say there is no slack. RH ⇔ every Newton step for ξ moves toward the critical line. |
| 17 | A flower that looks right but misses petals | The Davenport–Heilbronn function: same functional equation as ζ, zeros off the line, no Euler product. A proof must use the primes. |
| 18 | Collatz on negative and complex numbers | Negatives fall into three cycles, about a third each. In the complex extension, positive cycles attract and negative ones repel (multiplier 3ᵏ/2ᵐ). Each integer cycle has a nearby twin with flipped stability. |
| 19 | "The orange region looks like a Julia set" | Confirmed: it matches the filled Julia set of z² + 0.18719 on 99.4% of pixels, and −1 sits at its tip (Douady–Hubbard). |
| 20 | "The steps plot reminds me of the prime spiral" | The curves are doubling chains (log₂ curves). The dashes come from 8k + 4 and 8k + 5 always merging. Residue classes seen through a smooth coordinate. |
| 21 | Collatz in the prime-spiral layout | The arms come from the layout (2π ≈ 44/7). Which cycle a number reaches ignores its arm, but nearby numbers share a cycle more often than chance. |
| 22 | Fleurdelys in the prime-spiral layout | The petal spiral is featureless (Hlawka). Winding the petals by log x leans toward π exactly at prime powers (Landau): the zeros reproduce the primes. |
| 23 | Update all documents, append-only | This section. |

### What a geometric proof of RH must do

Each target below is proven equivalent to RH. Proving any one of them for ζ proves RH.

| Target | In flower language | Source |
| --- | --- | --- |
| A. Counting | For every height T, the petals through the origin up to T number exactly N(T). | Argument principle, Riemann–von Mangoldt; Turing's method checks it |
| B. Off-line slices miss 0 | For every σ between ½ and 1, the curve t ↦ ζ(σ + it) never passes through 0. | Restatement of RH |
| C. No folds | ζ′ has no zeros in 0 < Re s < ½: the 4D surface does not fold left of the line. | Speiser 1934; Levinson–Montgomery 1974 |
| D. A valley along the line | \|ξ(σ + it)\| strictly increases as σ moves away from ½. Equivalently Re(ξ′/ξ) > 0 right of the line. | Sondow–Dumitrescu 2010; Lagarias 1999 |

Target D links to our Newton thread. One Newton step for ξ moves s by −ξ/ξ′, which points left exactly when Re(ξ′/ξ) > 0. So RH holds if and only if every Newton step for ξ right of the line moves left, and by symmetry every step left of it moves right. This follows from Lagarias in one line, so it is an equivalence, not progress. Numerically, 0 of 3,240 grid points right of the line move right for t between 82 and 90.

There is no slack, and both facts are proven:

- Rodgers and Tao (2020): if RH holds, the de Bruijn–Newman constant is exactly 0. The zeros are only barely real.
- Bohr: for ½ < σ < 1 the curve ζ(σ + it) comes arbitrarily close to 0. No "safe distance" argument can work.

### The Davenport–Heilbronn test

The Davenport–Heilbronn function combines two Dirichlet L-functions mod 5:

```latex
f(s) = \tfrac{1 - i\kappa}{2}\, L(s,\chi) + \tfrac{1 + i\kappa}{2}\, L(s,\bar\chi), \qquad \kappa = \frac{\sqrt{10 - 2\sqrt5} - 2}{\sqrt5 - 1}
```

Here χ is the character mod 5 with χ(2) = i. It satisfies a functional equation of the same shape as ζ's, so its flower looks similar. But it has zeros off the line, for example 0.80852 + 85.69935i and 0.65083 + 114.16334i (checked to 25 digits).

- Between t = 82 and 90 its turning predicts about 5.4 petals. Only 3 pass through the origin; the off-line zero and its mirror are the missing 2. The curve bends toward 0 near (−0.35, 0.1) and turns back.
- Its Newton field breaks around the off-line pair: 50 grid points right of the line move right.
- It has no Euler product. That is the difference from ζ.

Consequence: any argument that uses only the functional equation, symmetry, petal shape, growth or general Newton/Mandelbrot dynamics would also "prove" something false about f. A proof of RH has to use the primes somewhere. The model of a geometric argument that does is the inequality 3 + 4cos φ + cos 2φ ≥ 0, applied prime by prime, which shows ζ has no zeros on Re s = 1.

The test for any proposed property P:

1. ζ provably has P at every height.
2. P implies one of the targets A–D.
3. The Davenport–Heilbronn function does not have P.

&#91;image: ζ's flower next to the Davenport–Heilbronn flower for t from 82 to 90, and the Davenport–Heilbronn curve at σ = 0.8085 passing through 0. Script: davenport_heilbronn.py.\]

&#91;image: Horizontal direction of one Newton step for ξ and for the completed Davenport–Heilbronn function. Red moves left, blue moves right. Script: davenport_heilbronn.py.\]

### The petals hear the primes

We drew the zeros the way the prime spiral draws primes: each zero ½ + iγ at radius γ and angle γ. A new script finds all 10,142 zeros up to height 10,000. The count matches mpmath exactly and the values agree to about 10⁻⁷.

- **Petal spiral, angle γ:** featureless. Hlawka (1975) proved that aγ is evenly distributed mod 1 for every a ≠ 0, so no arms are expected.
- **Angle γ·log x:** the angles lean toward π exactly when x is a power of a prime (Landau, 1912). For x = 2 the average of e^(iγ log 2) is −0.0768, and Landau's formula predicts −0.0769. For x = 6 and x = 10 it is 0.
- **The spectrum:** adding up the winding for every x gives a spike of height log p at every prime power up to 32 (2: 0.68 against 0.69; 3: 1.09 against 1.10), and about 0 everywhere else.

This is known: it is Landau's formula and the explicit formula behind it. It is still the clearest picture so far of the petals carrying the primes. It is also exactly what the Davenport–Heilbronn function lacks.

&#91;image: Left: the petal spiral. Middle: angles γ·log 2 and γ·log 6. Right: the spectrum, with a spike of height log p at each prime power. Script: zero_polar.py.\]

### Collatz: a new field

There is no known connection between Collatz and RH. We used the same tools: extend, measure stability, find the look-alike, separate what we see from what is true.

**Negative numbers.** On negatives, 3n + 1 is the same as 3n − 1 on positives. Down to −1,000,000 every start falls into one of three cycles:

| Cycle | Share of starts |
| --- | --- |
| −1 → −2 | 32.8% |
| −5 → −14 → −7 → −20 → −10 | 32.3% |
| 18 steps, starting at −17 | 34.9% |

That there are no others is a conjecture.

**The complex extension.** The entire function f(z) = (2 + 7z − (2 + 5z)·cos πz)/4 gives n/2 at even integers and 3n + 1 at odd ones (Letherman, Schleicher and Wood, 1999). Its slope at an integer is ½ (even) or 3 (odd). So a cycle with k odd and m even steps has multiplier 3ᵏ/2ᵐ, which equals 1/∏(1 + 1/3n) over its odd members. That product is the classical cycle equation (Steiner, 1977). For positive numbers each factor is above 1, so the cycle attracts. For negative numbers each is below 1, so it repels.

**Twins (observed in our code).** Next to every integer cycle sits a non-integer cycle with stability flipped. Its multiplier is about 2 minus the integer cycle's.

| Integer cycle | Multiplier | Twin starts at | Distance | Twin's multiplier |
| --- | --- | --- | --- | --- |
| 1 → 4 → 2 | 0.75 | 1.00147 | 0.0015 | 1.28 (repelling) |
| −1 → −2 | 1.5 | −0.99427 | 0.0057 | 0.50 (attracting) |
| −5 → … | 1.125 | −4.99994 | 0.000065 | 0.88 (attracting) |
| −17 → … | 1.068 | −16.9999996 | 0.00000044 | 0.94 (attracting) |

This is expected from complex dynamics when two fixed points sit close together. The twins depend on the chosen extension; the integer multipliers do not. The 1 → 4 → 2 basin in the complex plane is tiny (radius about 0.01) because its repelling twin bounds it.

**The Julia set next to −1 (your observation, confirmed).** Next to every even integer n the map has a critical point at about n − 2/(π²(2 + 5n)), for example −1.97401 next to −2. It is captured by the nearby attracting cycle, so two steps of the map act like a quadratic near the twin (Douady–Hubbard). The orange basin matches the filled Julia set of z² + c, with c = 0.18719 taken from the twin's multiplier, on 99.4% of pixels after only shifting, scaling and mirroring. The integer −1 sits exactly at the tip, where the β fixed point of the Julia set is: 2β = 1.501 against the cycle's multiplier 3/2. This is the same mechanism as the Mandelbrot copy in the ζ(s) − c family.

**The steps plot (your prime-spiral observation).** The structure is arithmetic, not a rendering artifact.

- Curves: steps(2n) = steps(n) + 1, with no exceptions up to 100,000. Doubling chains climb one step per doubling, which traces log₂ curves.
- Dashes: 8k + 4 and 8k + 5 always merge after three steps, for every integer k. In general the first m moves depend only on n mod 2ᵐ (Terras, 1976).
- The mod-8 statistics are nearly the same for positive and negative numbers (46.0% and 46.6% of neighbours have equal step counts).

**The prime-spiral layout.** The arms come from the layout itself, because 2π ≈ 44/7. Which cycle a negative number reaches is nearly independent of its arm (29–37% per class mod 44). Nearby numbers share a cycle more often than chance, and the effect fades smoothly with distance, with no extra jump at 44, 710 or 1024:

| Distance | Same cycle |
| --- | --- |
| 1 | 60.6% |
| 44 | 38.5% |
| 1000 | 33.7% |
| chance | 33.4% |

The likely reason is that nearby orbits merge, as 8k + 4 and 8k + 5 do. That is not yet proven.

**The look-alike lesson again.** The negative integers follow the same rule as the positive ones but have extra cycles. So a proof that every positive start reaches 1 must use something that fails for negatives. The sign inside ∏(1 + 1/3n) is one place it shows up.

&#91;image: Every integer from −20000 to 20000 by the cycle it falls into. Script: collatz_negative.py.\]

&#91;image: Collatz on the complex plane, with zooms at 0, 1, −1 and −5. Script: collatz_complex.py.\]

&#91;image: The basin next to −1 and the filled Julia set of z² + 0.1872. Script: collatz_julia.py.\]

&#91;image: Doubling chains and the 8k + 4, 8k + 5 merge. Script: collatz_structure.py.\]

&#91;image: Primes, positive n by steps, and negative n by cycle in the prime-spiral layout. Script: collatz_polar.py.\]

### Results that came up in session 2

| Result | Who, when | Status | What it says here |
| --- | --- | --- | --- |
| Davenport–Heilbronn function | Davenport and Heilbronn, 1936 | Proven | A flower with the same functional equation as ζ but zeros off the line. |
| Zero-free line Re s = 1 via 3 + 4cos φ + cos 2φ ≥ 0 | Hadamard, de la Vallée Poussin (1896); Mertens (1898) | Proven | The model of a geometric argument that uses the primes. |
| Landau's formula | Landau, 1912 | Proven | Winding the petals by log x leans toward π exactly at prime powers. |
| Zeros of ζ′ and off-line zeros | Levinson and Montgomery, 1974 | Proven | Behind target C. |
| aγ is evenly distributed mod 1 | Hlawka, 1975 | Proven | The petal spiral has no arms. |
| Re(ξ′/ξ) > 0 right of the line ⇔ RH | Lagarias, 1999 | Proven equivalence | Target D; Newton for ξ moves toward the line. |
| \|ξ\| increases away from the line ⇔ RH | Sondow and Dumitrescu, 2010 | Proven equivalence | Target D. |
| De Bruijn–Newman constant is at least 0 | Rodgers and Tao, 2020 | Proven | No slack on the line. |
| Generalized Collatz problems can be undecidable | Conway, 1972 | Proven | Collatz-like rules can be as hard as any problem. |
| First m moves depend only on n mod 2ᵐ | Terras, 1976 | Proven | The dashes in the steps plot. |
| Cycle equation and cycle-length bounds | Steiner, 1977, and later work | Proven | The multiplier 3ᵏ/2ᵐ = 1/∏(1 + 1/3n). |
| Collatz on the 2-adic integers is conjugate to a shift | Lagarias, 1985 | Proven | The 2-adic view of Collatz. |
| Entire extension of Collatz | Letherman, Schleicher and Wood, 1999 | Studied | Our complex pictures. |
| Almost all orbits reach almost bounded values | Tao, 2019 | Proven | The strongest partial result on Collatz. |
| Trigonometric proofs of Pythagoras | Calcea Johnson and Ne'Kiya Jackson, 2023–2024 | Published | The inspiration for step 16. |
| Every positive start reaches 1 | Collatz conjecture | Open | |
| Only three cycles on the negatives | Conjecture | Open | |

### Open threads after session 2

- [ ] The core observation about the flower (not yet revealed)
- [ ] The Collatz patterns you found for negative and complex numbers (not yet revealed)
- [ ] Julia copies next to the 18-cycle at −17, where the twin is only 4·10⁻⁷ away
- [ ] Why nearby numbers share a cycle: check whether orbit merging explains the whole curve
- [ ] Is "Newton for ξ moves toward the line" stated in this form in the literature?
- [ ] Draw the zero spectrum for the Davenport–Heilbronn function (expect no clean prime spikes)
- [ ] Carried over: which zero of ζ″ is the canonical seed; what in the 4D picture singles out Re(s) = ½

### Code added in session 2

| File | What it does |
| --- | --- |
| davenport\_heilbronn.py | ζ's flower next to the Davenport–Heilbronn flower, and the Newton step direction for both completed functions. |
| zeros.py | All zeros up to a height (Riemann–Siegel with tabulated corrections, mpmath below 300), cached in output/. |
| zero\_polar.py | The petals in the prime-spiral layout, angles γ·log x, and the prime spectrum. |
| collatz\_negative.py | Every start in −N…N by the cycle it reaches. |
| collatz\_complex.py | The complex extension with zooms at 0, 1, −1, −5. |
| collatz\_twins.py | The twin cycle next to each integer cycle. |
| collatz\_julia.py | The basin next to −1 against the filled Julia set of z² + c. |
| collatz\_structure.py | Doubling chains and the 8k + 4, 8k + 5 merge. |
| collatz\_polar.py | Collatz in the prime-spiral layout. |

## Session 2, continued: Julia copies and the observation checklist (Nov 23, 2026)

### Journey log, continued

| Step | Idea or question | What we found |
| --- | --- | --- |
| 24 | Look for Julia copies next to the −17 cycle | Every even member of a negative cycle puts one critical point into its twin's basin, so the hidden map has degree 2ᵐ (m = number of halvings): 2 for −1, 8 for −5, 2048 for −17. The −17 copy is a round blob with many bumps. |
| 25 | Look for Julia copies around the zeta flower | The flower passes through Mandelbrot copies in the Newton parameter plane. Inside the copy it crosses at t = 24.108, the s-plane shows a basilica and a rabbit, as Douady–Hubbard predict. |
| 26 | Update what the observation needs, to tweak it before sharing | A nine-check list (`Observation checklist.md`) and a test harness (`lookalikes.py`) that runs any property on ζ, L(s, χ₄) and Davenport–Heilbronn. |

### Julia copies next to the negative Collatz cycles

Next to every even member n of a cycle sits a critical point of f, at about n − 2/(π²(2 + 5n)). Odd members have one too, farther out, at about n + 12/(π²(2 + 5n)). In our code, for every negative cycle, each even member's critical point is joined to the twin cycle by a path that stays inside the basin, and no odd member's is. So the return map on a basin component has degree 2ᵐ, where m is the number of halvings in the cycle. This is a numerical observation; the count is a lower bound if other critical points hide in the components.

| Cycle | Halvings m | Return-map degree | Twin multiplier | Component next to an even member |
| --- | --- | --- | --- | --- |
| −1 → −2 | 1 | 2 | 0.4987 | next to −2, about 0.05 across: the quadratic copy matched before (z² + 0.18719) |
| −5 → … (5 steps) | 3 | 8 | 0.8829 | next to −14, about 0.006 across, two lobes |
| −17 → … (18 steps) | 11 | 2048 | 0.9356 | next to −34, about 0.0024 across, a round blob with many bumps |
| 1 → 4 → 2 (attracting itself) | 2 | 4 | 0.75 | |

Each blob is the filled Julia set of the hidden map. All its critical points are pulled into one attracting fixed point, and for such maps the boundary is a single closed curve (a quasicircle): the narrow necks in the pictures never close completely. The higher the degree, the more bumps it has at each scale. The integer itself sits on the edge of the blob, as −1 did.

&#91;image: Basin components next to −2, −14 and −34: degree 2, 8 and 2048. Script: collatz_julia_cycles.py.\]

**Correction.** The table above says the −5 component has two lobes. With the full window drawn, it has four, about 0.009 across and 0.009 tall.

### Julia copies around the zeta flower

The flower t ↦ ζ(½ + it) lives in the parameter plane of Newton's method for ζ(s) − c, and it passes through Mandelbrot copies there. Over t from −200 to 200 it crosses three of them:

| Copy centered at | Flower crossings (t) |
| --- | --- |
| 0.836 − 0.592i | 24.11, 66.33, 156.78, 196.36, −186.45 |
| −0.032 − 0.393i | 37.38, 101.19, 195.13, −53.13, −131.25 |
| 1.310 + 0.852i | 177.14, −162.59 |

Inside the copy at 0.836 − 0.592i, each parameter plays the role of a point of the Mandelbrot set, and the s-plane around the seed shows the matching Julia set:

| Parameter c | Role in the copy | What the s-plane shows near the seed |
| --- | --- | --- |
| 0.83605 − 0.59158i (period 2) | center (c′ = 0) | a disk-like blob |
| 0.852809 − 0.604099i (period 4) | basilica (c′ = −1) | a basilica |
| 0.829974 − 0.608302i (period 6) | rabbit | a rabbit |
| ζ(½ + 24.108i) = 0.83629 − 0.59853i | the flower's crossing, c′ ≈ −0.21 + 0.26i (main body) | a disk-like blob; this map also has the root ½ + 24.108i on the critical line |

This is the Douady–Hubbard mechanism again, so it is expected. What is new for us is the meeting: at the flower's crossing, one Newton map has both a root on the critical line and a Julia copy around the seed. Nothing here singles out Re(s) = ½ yet. The crossing happens because the flower's values pass through the copy, not because of the line.

&#91;image: The Mandelbrot copy the flower crosses, and the s-plane basilica and rabbit next to the true Julia sets. Script: zeta_julia.py.\]

### What the observation needs, updated

The full checklist is in `Observation checklist.md`. In short:

1. State it as one sentence with every word pinned down.
2. Say whether it is seen, believed or provable.
3. Check it is not already a known equivalent of RH.
4. Look for circularity.
5. Run the look-alike test both ways: it must fail for Davenport–Heilbronn and should hold for L(s, χ₄). `lookalikes.py` does this. Target D passes for ζ and L(s, χ₄) and fails for Davenport–Heilbronn at 13 of 130 points.
6. Make sure it does not need a margin.
7. Test every height you can, and say how it continues.
8. Name the step where the primes enter.
9. Compare with known results.

A weaker version that survives (a positive share of zeros, a zero-free region, a zero-density bound, a new equivalent form) is still a real result.

### Code added

| File | What it does |
| --- | --- |
| collatz\_julia\_cycles.py | Basin components next to −2, −14, −34 (degree 2, 8, 2048). |
| zeta\_julia.py | The Mandelbrot copy the flower crosses, and the basilica and rabbit in the s-plane. |
| lookalikes.py | Runs any property on ζ, L(s, χ₄) and Davenport–Heilbronn. |
| Observation checklist.md | The nine checks and the weaker targets. |

## Session 2, continued: the petals in every spiral view (Nov 23, 2026)

### Journey log, continued

| Step | Idea or question | What we found |
| --- | --- | --- |
| 27 | Run every Collatz-style view on the petals | Small and large spirals for primes, twin primes, petals colored by spacing, and twin petals. Primes and twin primes show arms; petals and twin petals do not. |
| 28 | Show only twin primes | At small scale the smaller twin and the larger twin each take one arm of their own. At large scale each avoids 2 of the 20 prime arms. |
| 29 | Extend "the petals hear the primes" | 35,673 zeros up to height 30,000 hear every prime power up to 100. Twin primes get the same spikes as other primes. |
| 30 | Overlay the critical strip, top and side views | In the spiral layout the critical line is the spiral r = θ itself. Wrapping the strip onto it puts every zero up to 120 on the middle line. |

### Twin primes in the spiral

All points in the prime-spiral layout sit on the Archimedean spiral r = θ; the arms come from sampling it at whole numbers (2π is close to 6 and to 44/7). Twin primes (p and p + 2 both prime) follow their own arm rules, which are proven and elementary:

| Scale | Primes use | Smaller twin p | Larger twin p + 2 | Why |
| --- | --- | --- | --- | --- |
| Small (mod 6) | 2 arms (1 and 5) | 1 arm: 5 mod 6 | 1 arm: 1 mod 6 | Past 3, one of p, p + 2 would otherwise be divisible by 3 |
| Large (mod 44) | 20 arms | 18 arms, avoiding 9 and 31 | 18 arms, avoiding 13 and 35 | On those arms the partner is divisible by 11 |

Counts leave out pairs below 13, which break the pattern.

### Petals and twin petals in the spiral

- Petals at radius γ and angle γ show no arms at either scale, as Hlawka's theorem (1975) predicts.
- Twin petals: pairs of consecutive zeros closer than 0.3 times the average spacing. There are 164 such pairs among the 10,142 zeros up to 10,000 (1.6%). They show no arms either.
- Consecutive gaps between zeros are anti-correlated, −0.369 in our data: a short gap tends to be followed by a long one. This is the opposite of Collatz, where nearby numbers tend to behave alike (60.6% share a cycle at distance 1). It is a numerical observation. Montgomery's pair-correlation conjecture says zeros repel like eigenvalues of random matrices, which is why twin petals are rare.

&#91;image: Primes, twin primes, petals colored by gap, and twin petals in the prime-spiral layout, at radius 1500 and 10000. Script: petal_spiral.py.\]

### The petals hear the primes, extended

With 35,673 zeros up to height 30,000 (matching mpmath's count exactly), the spectrum reaches x = 100:

- All 35 prime powers up to 100 have a spike within 0.075 of log p (mean difference −0.031).
- The 64 integers from 6 to 100 that are not prime powers all stay below 0.042.
- Twin primes get the same spikes as other primes. This one-number spectrum hears each prime by itself. Twin primes would show up in how pairs of zeros are spaced (Bogomolny–Keating's heuristic, from the Hardy–Littlewood conjectures), not here.

&#91;image: The zero spectrum up to x = 100, twin primes in orange, and the measured spike against log p for every prime power. Script: petal_spectrum.py.\]

### The critical strip, top view and side view

- **Top view:** the strip 0 ≤ σ ≤ 1 wrapped onto the spiral. The point σ + it sits at angle t and radius t + 4(σ − ½), so the critical line is the spiral r = θ, the same curve the prime spiral samples at whole numbers. Colors show ζ: hue is its direction, dark is small. All 38 zeros up to t = 120 appear as dark points on the middle line. The 30 primes up to 120 sit on the same curve, 19 of them twin primes.
- **Side view:** the same strip unrolled, with Z(t) below it. Each sign change of Z is a petal through the origin, and lines up with a zero on σ = ½.
- **Caveat:** putting whole numbers and zero heights on the same axis is a choice of layout, not a link. The real link between zeros and primes is the spectrum, where γ pairs with log p.

&#91;image: The critical strip wrapped onto the spiral (top view) and unrolled (side view), with Z(t). Script: strip_spiral.py.\]

### Code added

| File | What it does |
| --- | --- |
| petal\_spiral.py | Primes, twin primes, petals and twin petals in the spiral layout, two scales. |
| petal\_spectrum.py | The zero spectrum up to x = 100 with twin primes marked, and spike height against log p. |
| strip\_spiral.py | The critical strip wrapped onto the spiral, unrolled, and Z(t). |
| zeros.py (rerun) | 35,673 zeros up to height 30,000, cached. |

## Session 2, continued: pair spacing and spectroscopy (Nov 23, 2026)

### Journey log, continued

| Step | Idea or question | What we found |
| --- | --- | --- |
| 31 | Does the spacing between pairs of zeros hear twin primes? | Yes, collectively. The Fourier transform of the pair spacing bends at τ = 1 and goes flat, which is where prime pairs (p, p + h) enter, twin primes being h = 2. It cannot single out twin primes from the other gaps. |
| 32 | The side view looks like a wave: Fourier analysis (the user works with Fourier transforms) | The spectrogram of Z(t) shows one chirp line for every whole number n. Summing waves cos(t·log p) over the primes gives back peaks at the zeros. |
| 33 | The same analysis on twin primes only | Twin primes hear the zeros more strongly than random primes of the same count. So do cousin and sexy primes; isolated primes hear them upside down. It is about primes clustering, not twins alone. |

### Pair spacing hears prime pairs

The zeros are first rescaled to average spacing 1 (35,644 zeros between heights 100 and 30,000).

- **Pair correlation:** zeros repel at short distance. Only 705 pairs sit closer than 0.3 spacings, where independent points would give about 10,700 and random-matrix theory (GUE, Montgomery's conjecture) predicts about 980. The curve follows GUE closely. The small, significant deviations (χ² per bin about 4) are expected at finite height; Bogomolny, Bohigas, Leboeuf and Monastra (2006) explained them with prime corrections. We have not fitted their formula.
- **Form factor (its Fourier transform):** rises with slope 1.06 up to τ = 1, then flattens to 1.000 ± 0.021. If each prime only paired with itself, it would keep rising.
- **What this means:** heuristically, the flat part comes from pairs of primes (p, p + h) following the Hardy–Littlewood prime-pair statistics. Twin primes are the h = 2 term, but every even gap contributes. Montgomery (1973) proved the rising part assuming RH. Goldston and Montgomery (1987) tied the flat part to how primes spread in short intervals. Bogomolny and Keating (1996) derived the whole curve from the prime-pair conjecture. So the pair spacing hears all prime pairs together; at our heights it cannot single out twin primes.
- **Extra spikes, observed in our code:** a spike at τ = 1.000 matches Gram's law, since the rescaled zeros pile up halfway between whole numbers (the middle tenths hold about 4,400 zeros each, the edge tenths about 2,700). Spikes near τ = 1.09 and 1.23 survive changes in smoothing and bin size and drift slightly with height. They are not explained yet.

&#91;image: Pair correlation against GUE, and the form factor bending at τ = 1. Script: pair_spacing.py.\]

### Spectroscopy of the flower

**The side-view wave.** Riemann–Siegel writes Z(t) as a sum of waves cos(θ(t) − t·log n), one for every whole number n up to √(t/2π). Its spectrogram (short-time Fourier transform, t from 200 to 2600) shows exactly those chirp lines at angular frequency ½·log(t/2π) − log n, labelled n = 1 to 20. The lines are all integers, not only primes.

**From integers to primes.** The Dirichlet series of ζ has a term at every log n. Its logarithm keeps only prime powers: log ζ(s) = Σ Λ(n)/log n · n^(−s). In signal-processing language this is like a cepstrum, the spectrum of the log of a spectrum. It is an analogy, but an exact formula sits under it.

**Primes back to zeros.** The wave −Σ (log p)·p^(−1/2)·cos(t·log p) over prime powers up to 2,000,000 peaks at every zero up to t = 100, with a line strength of 3.10 standard deviations.

### Which primes hear the zeros

Line strength is the mean of the wave at the 29 zeros between 12 and 100, in standard deviations. Each subset is compared with random primes that have the same count in every range [2ʲ, 2ʲ⁺¹).

| Subset of primes up to 2,000,000 | Count | Line strength | Matched random | Difference |
| --- | --- | --- | --- | --- |
| twin (p ± 2 prime) | 29,741 | 2.12 | 1.76 ± 0.10 | +3.8 sd |
| cousin (p ± 4 prime) | 29,483 | 1.91 | 1.68 ± 0.09 | +2.5 sd |
| sexy (p ± 6 prime) | 53,931 | 2.43 | 2.18 ± 0.08 | +3.1 sd |
| isolated (no prime within 6) | 59,302 | −0.60 | 0.73 ± 0.18 | −7.6 sd |

This is an observation from our code, at one range of X and only 29 zeros. The heuristic reading, not proven: the zeros encode where primes are locally denser or sparser. Where they are denser, pairs are denser by roughly the square and isolated primes are rarer. So pairs amplify the zeros' signal and isolated primes invert it. This is about primes clustering, and twin primes are one case of it. We have not checked the literature for this exact experiment.

&#91;image: Spectrogram of Z(t), and the prime wave over all prime powers, twin primes and a matched random control. Script: zeta_spectroscopy.py.\]

&#91;image: Line strength for twin, cousin, sexy and isolated primes against matched random primes. Script: prime_subsets.py.\]

### Code added

| File | What it does |
| --- | --- |
| pair\_spacing.py | Pair correlation of the zeros and its Fourier transform (form factor), against GUE. |
| zeta\_spectroscopy.py | Spectrogram of Z(t); the prime wave over all primes, twin primes and a random control. |
| prime\_subsets.py | Line strength for twin, cousin, sexy and isolated primes against matched random primes. |

## Session 2, continued: Green–Tao, and twin primes versus RH (Nov 23, 2026)

### Journey log, continued

| Step | Idea or question | What we found |
| --- | --- | --- |
| 34 | If twin primes "appear on the petals" and that is infinite, does it prove the twin prime conjecture, with "all primes on the petals" still open? | Partly right. Twin primes and RH are independent as far as anyone knows. But a property of twin primes does not show there are infinitely many of them, and the petals already hear every prime (proven). RH is about zeros, not primes. |
| 35 | Explore the Green–Tao theorem | The first progression of k primes for k = 3 to 12, drawn in the spiral; counts of 3- and 4-term progressions approach the proven Green–Tao–Ziegler formula. |

### Twin primes and RH: what would follow from what

- **"Twin primes appear on the petals."** In the spiral layout every whole number lies on the curve r = θ, so being on it is a feature of the layout. In the spectrum sense, the petals hear every prime power; that is proven without RH (Landau 1912). Neither says anything new about twin primes.
- **"…and it is infinite."** Proving that every twin prime has some property, even one that infinitely many things have, does not show there are infinitely many twin primes. Every twin prime is odd and there are infinitely many odd numbers, but that proves nothing. Infinitely many twin primes is the twin prime conjecture itself.
- **Independence.** As far as anyone knows, the twin prime conjecture and RH are independent: neither is known to imply the other. Even assuming RH and its generalizations, twin primes stay out of reach because of the parity problem (Selberg), a known limit of sieve methods. A proof of twin primes would leave RH open, and the reverse.
- **Wording.** RH is "every nontrivial zero is on the critical line", not "every prime is on the petals".
- **What is proven about twin primes:** Chen (1973), infinitely many p with p + 2 prime or a product of two primes. Zhang (2013), infinitely many pairs of primes less than 70,000,000 apart. Maynard and Tao (2013–2014, independently) brought it to 600, and the Polymath project to 246.

### The Green–Tao theorem

Green and Tao (2004, published 2008) proved that the primes contain arithmetic progressions a, a + d, …, a + (k − 1)d of every length k. The proof does not use the zeros or RH. It combines Szemerédi's theorem (1975: any set of whole numbers with positive density has long progressions) with a transference principle: the primes are a dense part of a larger, well-mixed set of "almost primes", built with weights from Goldston and Yıldırım. Green, Tao and Ziegler (2010–2012) later proved how many k-term progressions there are up to N.

The first progression of each length, found by search:

| Length k | Progression | Last term |
| --- | --- | --- |
| 3 | 3 + 2j | 7 |
| 4 | 5 + 6j | 23 |
| 5 | 5 + 6j | 29 |
| 6 | 7 + 30j | 157 |
| 7 | 7 + 150j | 907 |
| 8, 9, 10 | 199 + 210j | 1669, 1879, 2089 |
| 11, 12 | 110437 + 13860j | 249037, 262897 |

The count of progressions of primes up to N, divided by the proven asymptotic C_k ∫∫ da dd / ∏ log(a + jd):

| N | 3-term count | ratio | 4-term count | ratio |
| --- | --- | --- | --- | --- |
| 10,000 | 59,504 | 0.946 | 10,257 | 0.915 |
| 100,000 | 2,856,331 | 0.969 | 389,606 | 0.960 |
| 200,000 | 9,428,344 | 0.970 | 1,207,788 | 0.964 |

The ratios approach 1 slowly, as prime counts usually do.

**Why 3-term progressions are proven and twin primes are not.** The constant for 3-term progressions, C₃ = 1.32032, is exactly twice the twin-prime constant 0.66016: the same prime-by-prime correction factors govern both patterns. Yet infinitely many 3-term progressions of primes were proven in 1939 (van der Corput), and progressions of every length in 2004. The difference is the number of free variables. A progression has two (the start a and the step d), and averaging over both lets Fourier-type methods count it. A twin prime pair has one (p, with the gap fixed at 2), and no current method can count it. Green and Tao call this "infinite complexity"; it is the same wall as the parity problem.

&#91;image: Prime progressions in the spiral layout, the first progression of each length, and the count ratio against the proven formula. Script: green_tao.py.\]

### Code added

| File | What it does |
| --- | --- |
| green\_tao.py | First progressions of primes for k = 3 to 12, drawn in the spiral; 3- and 4-term counts against the Green–Tao–Ziegler asymptotic. |

## Session 2, continued: the star shape (Nov 23, 2026)

### Journey log, continued

| Step | Idea or question | What we found |
| --- | --- | --- |
| 36 | The 10-prime progression 199 + 210j in the spiral layout draws a star, like the single-seed Mandelbrot orbits shown by 3Blue1Brown and Ben Sparks | Same geometry: both turn by a fixed angle at every step. The progression turns 0.4225 of a full turn per step; the orbit at c = −0.48 + 0.35i turns 0.4226. |

### Why they match

- **The progression.** In the spiral layout, a progression a + dj turns by d mod 2π at every step while its radius grows by d. For d = 210 that is 0.4225 of a full turn, between 2/5 (0.4) and 3/7 (0.4286). Joining the points in order draws a star.
- **The Mandelbrot orbit.** For c in the main cardioid, the orbit of 0 under z² + c settles onto a fixed point z*, and near it each step multiplies the distance to z* by λ = 1 − √(1 − 4c). So each step turns by the angle of λ and shrinks by |λ|. At c = −0.48 + 0.35i, the turn is 0.4226 of a full turn and |λ| = 0.854: a star spiraling inward.
- **The other screenshot.** At c = −0.52 + 0.57i the orbit is in the 2/5 bulb and settles on a cycle of 5 points, visited 2/5 of a turn apart: a five-pointed star.
- **The shared map.** The main cardioid is exactly the set of c whose fixed point turns by a given angle: c = λ/2 − λ²/4 with |λ| < 1. On its edge, the angle p/q is where the p/q bulb attaches (a standard fact of the Mandelbrot set). So every progression step d picks a point on the cardioid's edge, c(d) = e^(id)/2 − e^(2id)/4. Step 210 lands between the 2/5 and 3/7 bulbs, step 150 near 7/8, step 30 near 7/9.

This is shared geometry (rotation by a fixed angle), not number theory: the cardioid does not know which steps give primes. The match between 0.4225 and 0.4226 is a coincidence of the screenshot's c; any orbit or progression with the same turn draws the same star.

&#91;image: The progression 199 + 210j in the spiral layout, the orbit of z² + c at c = −0.48 + 0.35i, and where each step's turn angle sits on the main cardioid. Script: star_rotation.py.\]

| File | What it does |
| --- | --- |
| star\_rotation.py | The progression and the Mandelbrot orbit side by side, and each step's turn angle on the main cardioid's edge. |

## Session 2, continued: other flowers (Nov 23, 2026)

### Journey log, continued

| Step | Idea or question | What we found |
| --- | --- | --- |
| 37 | Shared geometry is a good sign: it means real mathematics is happening, not a one-off | Universality: Mandelbrot copies (McMullen), random-matrix spacing (zeros, heavy nuclei, Cuernavaca buses), Feigenbaum's constant, and rotation by a fixed angle (arms, stars, sunflowers). |
| 38 | Draw other flowers; so far the hourglass Fleurdelys appears only in RH | Sunflowers share the rotation mechanism. Other functions draw the same hourglass: every L-function with real coefficients does, including Davenport–Heilbronn. A complex character breaks the mirror. Off the line, ζ draws an hourglass that never touches 0. |

### Sunflowers

Point n at angle n × (turn) and radius √n (Vogel's model, 1979). The arms you see are the denominators of fractions close to the turn (its continued-fraction convergents):

| Turn | Fractions close to it | Arms you see |
| --- | --- | --- |
| Golden angle, 0.3820 of a turn | 1/3, 2/5, 3/8, 5/13, 8/21, 13/34 | 3, 5, 8, 13, 21 (Fibonacci) |
| 1 radian, 0.1592 of a turn (the prime-spiral layout) | 1/6, 3/19, 4/25, 7/44, 53/333, 113/710 | 6, 44, 710 at growing scale |
| Step 210, 0.4225 of a turn | 2/5, 3/7, 8/19, 11/26, 30/71 | 71 straight rays at the edge |

The golden angle is the hardest number to approximate by fractions, so sunflower seeds never line up into a few arms and pack evenly. This is the same mechanism as the prime-spiral arms and the star shapes.

&#91;image: Sunflowers for three turns, all points and primes only. Script: sunflowers.py.\]

### Other Fleurdelys flowers

The hourglass has two ingredients: mirror symmetry (real coefficients give F(s̄) = conj F(s), so t and −t are mirror images) and petals through 0 (each zero on the line). For t from −60 to 60:

| Function | Passes through 0 | Mirror-symmetric | Euler product |
| --- | --- | --- | --- |
| ζ(½ + it) | 26 | yes | yes |
| L(½ + it, χ₄), real character mod 4 | 50 | yes | yes |
| ζ·L(χ₄), the zeta function of the Gaussian integers | 76 = 26 + 50 | yes | yes |
| Davenport–Heilbronn f(½ + it) | 56 | yes | no |
| L(½ + it, χ), complex character mod 5 | 55 | no | yes |
| ζ(0.6 + it), off the line | 0 (closest 0.076) | yes | yes |

So the hourglass is not unique to ζ. It is the shape of a whole family, and the Davenport–Heilbronn flower has it too, even though it misses petals higher up (at t ≈ 85.7). The hourglass shape alone cannot tell RH apart from its failure; what matters is whether the petal count keeps up, which is target A.

&#91;image: Flowers of ζ, L(χ₄), the Gaussian-integer zeta, Davenport–Heilbronn, a complex character mod 5, and ζ at σ = 0.6. Script: other_flowers.py.\]

| File | What it does |
| --- | --- |
| sunflowers.py | Sunflowers (Vogel's model) for the golden angle, 1 radian and step 210; all points and primes only. |
| other\_flowers.py | Flowers of six functions, with passes through 0 and the mirror test. |

## Session 2, continued: Feigenbaum and Fourier, playing with the new tools (Nov 23, 2026)

### Journey log, continued

| Step | Idea or question | What we found |
| --- | --- | --- |
| 39 | Back to the 3D and 4D projections of the critical line: that is the hourglass shape | Drew (Re F, Im F, t) from the side for six functions and the σ-slices of ζ. Every real-coefficient function makes the hourglass; only σ = ½ touches the axis. |
| 40 | Map the Feigenbaum constant | ζ's own Newton family has a period-doubling cascade 3 → 6 → 12 → … → 384 on the real line, and its gap ratios approach 4.6692. |
| 41 | Fourier analysis of primes, twin primes and Collatz | The spectrum of the primes has lines exactly at fractions a/q with q square-free, heights 1/φ(q). Twin primes have lines at the same places with different heights (full height at 1/3 and 1/6). Collatz has lines only at a/2ᵐ, the opposite. |

### Feigenbaum's constant inside ζ's Newton family

For real c, the Newton map for ζ(s) − c sends real numbers to real numbers, and w = −3.595771 (a real zero of ζ″) is its free critical point. That makes it a real one-parameter family, like the logistic map. In the window c ∈ [0.0199, 0.0205] the orbit of w has period 3, then 6, 12, 24, …: the real slice of a period-3 Mandelbrot copy. Its superstable parameters (w returns to itself after exactly P steps), found by bisection:

| Period P | c_P | Gap ratio |
| --- | --- | --- |
| 3 | 0.020425946526685 | |
| 6 | 0.020159477880976 | |
| 12 | 0.020083368584961 | 3.501 |
| 24 | 0.020066231465415 | 4.441 |
| 48 | 0.020062521338855 | 4.619 |
| 96 | 0.020061724922537 | 4.659 |
| 192 | 0.020061554262738 | 4.6667 |
| 384 | 0.020061517708154 | 4.6686 |

Gap ratio = (c at period P/4 − c at period P/2) / (c at period P/2 − c at period P), listed on the row of period P. The ratios approach Feigenbaum's δ = 4.6692016…, as his universality theorem (Feigenbaum 1978, proved by Lanford 1982) predicts for any smooth one-humped family. This is expected, not new, but it is a clean example of shared geometry: the same constant governs the logistic map, the real line of the Mandelbrot set, dripping faucets, and ζ's Newton family.

&#91;image: Bifurcation diagram of the Newton map for ζ(s) − c on the real line, and the gap ratios approaching δ. Script: feigenbaum_zeta.py.\]

### Fourier spectra of primes, twin primes and Collatz

Treat each as a signal on n = 1 … 720,720 and take its Fourier transform. 720,720 is divisible by every q ≤ 16, so every fraction a/q with q ≤ 16 is an exact frequency.

- **Primes (58,083):** lines exactly at a/q with q square-free, height |μ(q)|/φ(q): 1 at 1/2, 0.5 at 1/3 and 1/6, 0.25 at the fifths, nothing at 1/4, 1/8, 1/9, 1/12, 1/16. All 40 predicted heights for q ≤ 16 match within 0.002. This comes from primes spreading evenly over residue classes (Dirichlet, Siegel–Walfisz), the same input the circle method of Vinogradov and Green–Tao uses.
- **Twin primes (6,207 pairs, the smaller member):** lines at the same fractions, but heights set by the residues r where both r and r + 2 avoid q's factors (the Hardy–Littlewood prediction). Full height 1.0 at 1/3 and 1/6, because every smaller twin above 3 is 2 mod 3. 0.54 at 2/5 against 0.25 for primes; 0.08 at 2/7 against 0.17. All match within 0.016.
- **Collatz step counts:** lines only at fractions a/2ᵐ (1/2: 0.134, 1/4: 0.095, 3/8: 0.088, 1/16: 0.060), and essentially nothing at 1/3, 1/5 or 1/7. That follows from Terras: the first m moves depend only on n mod 2ᵐ.

So the primes have no lines at the powers of 2 beyond 1/2, and Collatz has lines only there. In Fourier terms, the two problems live on opposite sides of the spectrum.

&#91;image: Spectra of the primes, twin primes and Collatz step counts, with predicted line heights. Script: prime_fourier.py.\]

### Fleurdelys in 3D and 4D: the hourglass

The hourglass is the 3D curve t ↦ (Re F(½ + it), Im F(½ + it), t), seen from the side: loops narrow near t = 0 widen toward both ends, and the zeros are the points where the curve meets the vertical axis F = 0. Axis hits for t from −50 to 50, counted where the curve's direction flips by about half a turn (robust to the step size):

| Function | Axis hits | Hourglass mirrored top to bottom |
| --- | --- | --- |
| ζ(½ + it) | 20 | yes |
| L(½ + it, χ₄) | 40 | yes |
| ζ·L(χ₄), the Gaussian-integer zeta | 60 = 20 + 40 | yes |
| Davenport–Heilbronn | 42 | yes |
| L(½ + it, χ), complex character mod 5 | 43 | no |
| ζ(0.6 + it) | 0 | yes |

The 4D view draws ζ(σ + it) for σ = 0.3, 0.5 and 0.7 in one 3D frame. Only σ = ½ touches the axis (20 hits, closest 0.002); σ = 0.3 and 0.7 stay at least 0.172 and 0.147 away for t in ±50. Off the line they do come arbitrarily close at larger heights (Bohr), so this distance is not a margin.

&#91;image: The 3D hourglass for six functions, and ζ's σ = 0.3, 0.5, 0.7 slices. Script: fleurdelys_3d.py.\]

## Session 2, continued: the flower as a bouncing ball (Nov 23, 2026)

### Journey log, continued

| Step | Idea or question | What we found |
| --- | --- | --- |
| 42 | The side view looks like a bouncing ball (elasticity and phase). What can we measure, and how does it compare with the π from two colliding blocks? | Bounce heights, elasticity, phase portrait, phase lag S(t) and Gram phase locking all have clean numbers. The blocks count steps of a fixed angle that fit in π; the flower counts half-turns (≈ π each) that fit in θ(T), off by the phase lag. |

### The dictionary

| Bouncing ball | The flower's side view |
| --- | --- |
| height y(t), hitting the floor | \|Z(t)\| = \|ζ(½ + it)\|, touching 0 at every zero |
| phase portrait (y, p) | (Z, Z′/θ′), with local frequency θ′(t) ≈ ½·log(t/2π) |
| energy, falling by e² per bounce | squared amplitude of each petal |
| elasticity e = 0.8, constant | e_n = reach of petal n + 1 ÷ reach of petal n, fluctuating |

### What we measured (zeros up to 10,000)

- **Phase portrait:** each petal is a near-circle in (Z, Z′/θ′), like an elastic oscillator whose energy gets a random kick at every bounce.
- **Elasticity** (10,140 bounces): the median e_n is 0.990 and the average of log e_n is 0.0000. Half the bounces go higher (49.6%) and half lower, with a wide spread (standard deviation of log e_n 1.39). Consecutive values are anti-correlated (−0.41): a high bounce tends to follow a low one. The ball always loses energy; the flower neither gains nor loses on average.
- **The law of the bounce heights:** Selberg's central limit theorem (1946, proven) says log|ζ(½ + it)| is close to normal with variance ½·log log t. At 40,000 random t between 5,000 and 10,000, the measured variance is 1.71. Selberg's leading term gives 1.09; Keating and Snaith's random-matrix model (2000), ½(log N + γ + 1) with N = log(t/2π), gives 1.77. The measured distribution is also skewed, with a long left tail from near-zeros, as random matrices predict. The normal shape appears only at enormous heights.
- **Phase lag S(t) = N(t) − θ(t)/π − 1:** zeros counted minus the clock θ/π. Mean +0.0001, standard deviation 0.41, largest |S| 1.43 up to 10,000. Selberg's leading-order spread is √(log log t / 2π²); lower-order terms add more at these heights. Turing's method for checking RH numerically relies on S averaging to 0.
- **Phase locking (Gram's law):** Gram points are where θ(t) passes a multiple of π. Of 10,141 Gram intervals up to 10,000, 83.8% hold exactly one zero, 8.1% none, 8.0% two and 0.1% three. The first failure is the interval starting at t = 280.80, between Gram points 125 and 126, as Hutchinson found in 1925. Empty and double intervals balance, which is the phase lag averaging to 0.

### Colliding blocks and π

Two blocks with masses 1 and 100ᵏ, perfectly elastic, against a wall, collide 3, 31, 314, 3141, 31415, 314159 times (our simulation, k = 0 to 5). Galperin (2003) explained why: in the coordinates (√m₁·v₁, √m₂·v₂), energy conservation is a circle, and each collision turns the state by the same angle 2·arctan(√(m₁/m₂)). The collisions stop once the turns add up to π, so the count is about π ÷ arctan(√(m₁/m₂)).

The comparison with the flower:

| | Blocks | Flower |
| --- | --- | --- |
| Phase space | a circle (energy conserved, elastic) | near-circles of changing size (energy kicked at each bounce) |
| Turn per step | exactly 2·arctan(√(m₁/m₂)) | about π per petal, on average |
| What is counted | collisions ≈ π ÷ (turn per step) | petals ≈ θ(T) ÷ π |
| Error in the count | none (the turn is exactly constant) | the phase lag S(T), which stays small but is never 0 for long |

It is the same mechanism as the spiral arms and the star shapes: rotation by a fixed angle, counted against a full or half turn. The inelastic ball is the third case: its energy shrinks, so its phase portrait spirals inward. RH's counting target A says the flower's count must keep up exactly: every half-turn of the clock is paid for by a zero on the line, up to the bounded phase lag.

&#91;image: The flower as a bouncing ball: \|Z(t)\| bounces, phase portrait, elasticity histogram, phase lag S(t), the law of log\|ζ\|, and the colliding blocks on their energy circle. Script: zeta_bounce.py.\]

| File | What it does |
| --- | --- |
| zeta\_bounce.py | Bounces, phase portrait, elasticity, phase lag, Selberg's law and the colliding blocks. |

## Session 2, continued: the assistant's note, and a circle around the twin primes (Nov 24, 2026)

### Journey log, continued

| Step | Idea or question | What we found |
| --- | --- | --- |
| 43 | The user's other assistant: the bloom rate gives N(T) = θ(T)/π + 1 + S(T), so all the difficulty sits in S(T), and the Euler product must force each half-turn to make a petal | Mostly right, three refinements. θ(t) also has a −t/2 term. S(T) counts all zeros and is small without RH; the quantity that decides RH is the petal deficit N(T) − N₀(T) = 2 × (zeros right of the line). One petal per half-turn is Gram's law, which fails for ζ itself (16% of half-turns up to 10⁴). |
| 44 | In the spiral layout, is "a circle of radius K containing all twin primes" the property if the twin prime conjecture is false? | Yes, exactly, but it is a restatement (finite = bounded). The arms can prove such a circle for inadmissible patterns (p, p + 2, p + 4: only 3, 5, 7), never for twin primes. Counts below 10⁸ follow Hardy–Littlewood to ratio 0.9999. |

### Refinements to the assistant's note

1. θ(t) = (t/2)·log(t/2π) − t/2 − π/8 + O(1/t). The −t/2 term is the same size as the count, so N(T) ≈ (T/2π)·log(T/2π) − T/2π + 7/8.
2. N(T) = θ(T)/π + 1 + S(T) counts all zeros in the strip, on or off the line, whether or not RH holds. S(T) is proven to grow at most like log T without RH, and the Davenport–Heilbronn function also has a small S while skipping petals. The quantity that decides RH is the petal deficit N(T) − N₀(T) = 2 × (number of zeros with real part above ½, up to height T), where N₀(T) counts the petals through 0 (sign changes of Z). Following the phase along the line counts petals; following it around the strip gives S(T); the two differ exactly by the off-line zeros. For Davenport–Heilbronn the deficit jumps by 2 at t ≈ 85.70 and again at 114.16.
3. One petal per half-turn is Gram's law. Up to 10⁴, 8.1% of half-turns hold no petal and 8.0% hold two (first failure at t = 280.80). The block version (Rosser's rule) is also known to fail eventually. RH needs only the running total N₀(T) to equal N(T), not one petal per half-turn. Any argument using one-per-half-turn hits check 4 (circularity) of the checklist.

### A circle around the twin primes

In the spiral layout the radius is the number, so the twin prime conjecture is false exactly when some circle of radius K contains every twin prime. That is a correct equivalence, and a restatement: finite and bounded say the same thing.

The circle does separate patterns that residues can decide from those they cannot:

- **(p, p + 2, p + 4):** one of the three is always divisible by 3, so the only such triple of primes is 3, 5, 7. A circle of radius 7 traps them, provably (our search below 10⁶ finds only 3).
- **(p, p + 2):** for every prime q it uses only 2 of q's residues, so the arms always leave room. Residues alone can never trap twin primes in a circle, and whether something else does is the twin prime conjecture itself.
- **Proven:** pairs of primes at most 246 apart cannot be trapped by any circle (Zhang 2013; Maynard and Tao; Polymath). Brun (1919): the twin primes are sparse enough that the sum of their reciprocals converges (Brun's constant ≈ 1.902; our partial sum up to 10⁸ is 1.7588).

Counts of twin pairs below x against Hardy–Littlewood's prediction 2C₂ ∫₂ˣ dt / log²t:

| x | Twin pairs | Hardy–Littlewood | Ratio |
| --- | --- | --- | --- |
| 100 | 8 | 14 | 0.591 |
| 10,812 | 218 | 227 | 0.961 |
| 1,168,952 | 9,376 | 9,403 | 0.997 |
| 100,000,000 | 440,312 | 440,368 | 0.9999 |

&#91;image: Twin primes up to 3000 in the spiral layout with the circle through the last pair, the 3-5-7 triple in its radius-7 circle, and twin-pair counts against Hardy–Littlewood up to 10⁸. Script: twin_circle.py.\]

| File | What it does |
| --- | --- |
| twin\_circle.py | The circle restatement, the 3-5-7 triple, and twin-pair counts against Hardy–Littlewood up to 10⁸. |

## Session 2, continued: escape regions and chaos (Nov 24, 2026)

### Journey log, continued

| Step | Idea or question | What we found |
| --- | --- | --- |
| 45 | Is "the Mandelbrot set above radius 2 is never bounded" the right property? How can chaos extend to RH and twin primes with our tools? | Yes, as the escape criterion: past radius max(2, \|c\|) an orbit never returns (0 of 367,448 random orbits came back). The same "one term dominates" argument gives ζ no zeros for Re s > 1 (Euler product). The hard questions (the set's boundary, the critical strip, twin primes) live where no term dominates: the chaotic region. |

### The escape criterion

If |zₙ| > 2 and |zₙ| ≥ |c|, then |zₙ₊₁| ≥ |zₙ|² − |c| ≥ |zₙ|(|zₙ| − 1) > |zₙ|, and the growth factor keeps increasing, so the orbit runs to infinity. Hence the Mandelbrot set lies in |c| ≤ 2, with c = −2 its only point on that circle. Checked on 400,000 random orbits: 367,448 crossed the radius and none came back.

### One pattern, three problems

| Problem | Easy region: one term dominates | Hard region: no term dominates |
| --- | --- | --- |
| Mandelbrot | \|z\| > max(2, \|c\|): squaring wins, the orbit escapes | the boundary of the set: fractal, chaotic |
| Zeros of ζ | Re s > 1: the Euler product wins, \|ζ(s)\| ≥ ζ(2σ)/ζ(σ) > 0, no zeros (Re s < 0 by the functional equation) | the critical strip: values dense (Bohr), ζ imitates every nonvanishing function (Voronin) |
| Prime patterns | inadmissible patterns: residues force a factor, finitely many (only 3, 5, 7 for p, p + 2, p + 4) | admissible patterns such as twin primes: residues never decide; the parity problem |

### Measurements

- **ζ's floor for Re s > 1:** the minimum of |ζ(σ + it)| over t ∈ [1, 600] sits above the proven floor ζ(2σ)/ζ(σ) at every σ > 1 sampled (σ = 1.3: 0.466 against 0.332; σ = 2.5: 0.783 against 0.773). In the strip it drops toward 0 (σ = 0.55: 0.04; σ = 0.5: the zeros).
- **Davenport–Heilbronn right of 1 (a prediction of mine that failed):** I expected zeros with Re s > 1, since it has no Euler product. A search over t ≤ 3000 found none; its minimum stays above 0.19 (σ = 1.01: 0.196 at t ≈ 240.4). Without an Euler product there is no theorem keeping it away from 0 there, but at these heights it stays away anyway. Whether it has zeros right of 1 at all is a literature check, now an open thread.
- **Chaos in ζ's Newton family:** the Lyapunov exponent along the real cascade is strongly negative in the period-3 window (about −2), touches 0 at each doubling, and is positive (up to +0.17) on 17% of the window: order, the cascade, then chaos.
- **Quantum chaos:** the spacings between 35,643 neighbouring zeros follow the GUE curve, the signature of a chaotic quantum system without time reversal (Bohigas–Giannoni–Schmit 1984). Only 0.6% of spacings are below 0.2, against 18.1% for independent points (Poisson).

### Where chaos meets RH and twin primes (known bridges, none a proof)

- **Bagchi (1981):** RH holds exactly when ζ approximates its own shifts on the right half of the strip (strong recurrence). RH is equivalent to a recurrence property of a chaotic object.
- **Quantum chaos:** Berry and Keating (1999) proposed a chaotic system whose energy levels would be the zeros, with periodic orbits of length log p, matching the spectrum lines in `petal_spectrum.py`. Chaos explains the spacing statistics; it does not by itself make the zeros real, which is what RH needs.
- **Primes as chaos:** Sarnak's conjecture (2010) says the Möbius function does not correlate with any low-complexity (zero-entropy) dynamical system. Chowla's conjecture, about μ(n)μ(n + 2), is the Möbius cousin of the twin prime problem. Tao (2016) proved its logarithmically averaged two-point form using ideas from ergodic theory and entropy.

&#91;image: Mandelbrot escape criterion, ζ's Euler-product floor against Davenport–Heilbronn, the Lyapunov exponent along ζ's Newton cascade, and the zero spacings against GUE. Script: chaos_bridges.py.\]

| File | What it does |
| --- | --- |
| dh\_fast.py | Fast vectorized Dirichlet L-functions mod q and the Davenport–Heilbronn function (Euler–Maclaurin Hurwitz zeta), checked against mpmath. |
| chaos\_bridges.py | Escape criterion, ζ's floor, Lyapunov exponent, zero spacings. |

## Session 2, continued: the petal ledger, the pull of the line, the Euler product, and eigenvalues (Nov 24, 2026)

### Journey log, continued

| Step | Idea or question | What we found |
| --- | --- | --- |
| 46 | Build the petal ledger (item 1) | ζ and L(s, χ₄): deficit 0 at every height up to 200. Davenport–Heilbronn: deficit jumps by 2 at t ≈ 85.8, 114.2, 166.5, 176.8, its four off-line zeros. |
| 47 | Newton for ξ as a dynamical system (item 2) | For ζ and L(s, χ₄), every one of 398,000 grid points right of the line is pulled toward it. Davenport–Heilbronn has 498 points pushed away, in four pockets at exactly its off-line zeros. |
| 48 | The Euler product, the special part | Partial Euler products never reach 0; the 3-4-1 trick holds for ζ and fails for Davenport–Heilbronn; ζ's "cepstrum" lives only on prime powers. |
| 49 | Eigenvalues (where the user's journey started) | The Redheffer matrix: det = Mertens function, so RH is a statement about determinants of a 0/1 matrix. Its eigenvalues: two near ±√n, ⌊log₂ n⌋ − 1 small ones, and 1 repeated. The zeros space like eigenvalues of a random Hermitian matrix. |

### The petal ledger (`petal_ledger.py`)

N(T) comes from the argument principle on the completed function, along 2 → 2 + iT → ½ + iT; N₀(T) counts sign changes of the completed function on the line. Heights within 0.01 of a zero are skipped (two early versions of the grid landed on zeros and showed fake one-step blips).

| Function | N(200) | N₀(200) | Deficit | Deficit jumps |
| --- | --- | --- | --- | --- |
| ζ | 79 | 79 | 0 | none; N(T) equals the stored zero list at every T |
| L(s, χ₄) | 122 | 122 | 0 | none |
| Davenport–Heilbronn | 129 | 121 | 8 | +2 at t ≈ 85.8, 114.2, 166.5, 176.8 |

The four Davenport–Heilbronn jumps are its off-line zeros near 0.808 + 85.70i, 0.651 + 114.16i, and two more near t ≈ 166.5 and 176.8.

### The pull of the line (`xi_pull.py`)

On a grid of 398,000 points with ½ < σ ≤ 1.5 and t ≤ 200:

| Function | Points pushed away from the line | Weakest pull, min of Re(Λ′/Λ)/(σ − ½) |
| --- | --- | --- |
| ζ | 0 | +0.046 |
| L(s, χ₄) | 0 | +0.160 |
| Davenport–Heilbronn | 498, in pockets at t ≈ 85.5–86.0, 114.1–114.3, 166.5–166.6, 176.5–176.9 | −789 |

The pull breaks exactly where the ledger jumps: the two tests see the same off-line zeros, one by counting and one by dynamics. For ζ both are equivalent to RH (targets A and D) and both hold here.

### The Euler product (`euler_product.py`)

- **Partial products never reach 0.** Each factor (1 − p⁻ˢ)⁻¹ is nonzero, so ∏ over p ≤ P has no petals through the origin. For t from 10 to 60 the closest approaches are 0.215 (P = 10), 0.115 (P = 100), 0.056 (P = 1000), against 0.0001 for ζ. On the line the product does not converge; its flowers are tangled, and the clean hourglass belongs to ζ itself. The primes reach the zeros indirectly, through the continuation and the explicit formula.
- **The 3-4-1 trick** (Hadamard and de la Vallée Poussin 1896; Mertens 1898): for σ > 1, log|ζ(σ)³ζ(σ+it)⁴ζ(σ+2it)| ≥ 0, because prime by prime 3 + 4cos x + cos 2x = 2(1 + cos x)² ≥ 0. At σ = 1.05 and t ≤ 400: ζ never drops below +5.21; Davenport–Heilbronn goes down to −5.98 and is negative on 58% of t.
- **The cepstrum:** the coefficients of log F. For ζ they are Λ(n)/log n, nonzero only at prime powers (composite values below 10⁻¹⁵). For Davenport–Heilbronn they reach 4.25 at composite n (6, 10, 12, 14, 15, 18, …). An Euler product is exactly the property that log F lives on prime powers.

### Eigenvalues (`eigen_rh.py`)

- **The Redheffer matrix** Aₙ (Redheffer 1977): 1 where i divides j, or j = 1. Its determinant is the Mertens function M(n) = μ(1) + … + μ(n) (checked at n = 10, 50, 100, 200, 300). RH is equivalent to M(n) = O(n^(½+ε)) for every ε > 0 (Littlewood 1912). So RH is a statement about the determinants of simple 0/1 matrices.
- **Its eigenvalues** (n = 2000): two real ones at 48.49 and −40.70 (near ±√n = ±44.72, both shifted up), nine small ones (⌊log₂ n⌋ − 1 = 9, between about −0.14 and 0.95), and the eigenvalue 1 with multiplicity 1989 = n − ⌊log₂ n⌋ − 1 (Barrett, Forcade and Pollington 1988; Barrett and Jarvis 1992; Vaughan). The eigenvalue 1 is defective, so rounding spreads it into a small ring (radius up to 0.05) around 1.
- **M(n)/√n up to 10⁷** stays below 0.57 in size (largest at n = 199). The stronger guess |M(n)| < √n (Mertens' conjecture) is false (Odlyzko and te Riele 1985), even though no counterexample has been found by computation: no slack again.
- **Hilbert–Pólya:** if the zeros were eigenvalues of a self-adjoint operator they would be real, which is RH. No such operator is known, but the spacings of 35,643 zeros and of one random 2000 × 2000 Hermitian matrix follow the same GUE law.

&#91;image: The petal ledger for ζ, L(s, χ₄) and Davenport–Heilbronn. Script: petal_ledger.py.\]

&#91;image: Where a Newton step for the completed function moves toward or away from the line, and the weakest pull at each height. Script: xi_pull.py.\]

&#91;image: Partial Euler-product flowers, the 3-4-1 trick, and the cepstrum of ζ and Davenport–Heilbronn. Script: euler_product.py.\]

&#91;image: The Redheffer matrix, its eigenvalues, M(n)/√n up to 10⁷, and zero spacings against a random Hermitian matrix. Script: eigen_rh.py.\]

| File | What it does |
| --- | --- |
| petal\_ledger.py | N(T) and N₀(T) for ζ, L(s, χ₄), Davenport–Heilbronn, and the petal deficit. |
| xi\_pull.py | Direction and strength of the Newton pull toward the line for the three functions. |
| euler\_product.py | Partial Euler products, the 3-4-1 trick, and the log-coefficients. |
| eigen\_rh.py | Redheffer matrix, its eigenvalues, the Mertens function, and random-matrix spacings. |

## Session 2, continued: Hilbert–Pólya, the flower turned into a circle (Nov 24, 2026)

### Journey log, continued

| Step | Idea or question | What we found |
| --- | --- | --- |
| 50 | Hilbert–Pólya: transform the flower into "another flower" that forces the zeros onto the line | The map w = 1 − 1/s turns the critical line into the unit circle (right of the line → inside). RH ⇔ every zero lands on the circle ⇔ Li's λₙ ≥ 0 for all n (Li 1997; Bombieri–Lagarias 1999). ζ: all 35,673 zeros on the circle, λₙ positive and on the Keiper–Li curve. Davenport–Heilbronn: four pairs miss the circle by 3·10⁻⁶ to 4·10⁻⁵. |

### The transformed plane (`hilbert_polya.py`)

- **The map.** w = 1 − 1/s is a Möbius map. Each vertical line Re s = σ becomes a circle through w = 1: σ = ½ is the unit circle, σ = 0.7 a smaller circle inside it, σ = 0.3 a larger one outside, σ = 0 the vertical line Re w = 1. A zero ½ + iγ lands at angle about 1/γ, so all zeros crowd toward w = 1 (first zero at angle 0.071).
- **ζ:** all 35,673 zeros up to height 30,000 sit on the circle to rounding (max ||w| − 1| = 2.2·10⁻¹⁶). This is just the input (they were computed on the line), not a test.
- **Li's criterion** (proven equivalence). λₙ = Σ over zeros of [1 − (1 − 1/ρ)ⁿ]. RH ⇔ λₙ ≥ 0 for every n. From our zeros plus a tail estimate: λ₁ = 0.0230957, equal to the exact value 1 + γ/2 − ½ log 4π (γ = Euler's constant); λ₂ = 0.0923, λ₁₀ = 2.279, λ₁₀₀ = 118.60, λ₁₀₀₀ = 2326.1, λ₂₀₀₀ = 5351.8. The Keiper–Li size under RH is (n/2)(log n − 1 + γ − log 2π): 117.2, 2323.5, 5340.2. All positive in our sample (proven positive only for finitely many n; computed far beyond 2000 in the literature).
- **Davenport–Heilbronn on the circle.** Its four zeros right of the line (σ = 0.8085, 0.6508, 0.5744, 0.7243 at γ = 85.70, 114.16, 166.48, 176.70) land inside the circle, their mirrors outside, by |w| − 1 = ±4.2·10⁻⁵, ±1.16·10⁻⁵, ±2.7·10⁻⁶, ±7.2·10⁻⁶, matching (2σ − 1)/(2γ²). The circle squeezes height, so the miss is tiny but real.
- **No slack, again.** The mirror zero outside the circle contributes a term of size about 2(1 + δ)ⁿ. It passes the Keiper–Li size only at n ≈ 3.3·10⁵ (γ = 85.7), 1.3·10⁶, 2.2·10⁶, 6.3·10⁶. So Li's test sees an off-line zero only at very large n; it gets later the higher the zero. This is a crude envelope (the term oscillates, and DH has its own gamma factor), not a computed λₙ for DH.
- **The "other flower".** 100 eigenvalues of a random 100 × 100 unitary matrix (CUE) lie on a circle and repel: smallest gap 0.19 × mean, 1% of gaps below 0.2 × mean. 100 consecutive zeros after #20,000, unfolded and wrapped onto a circle: 0.12 × mean, 2%. 100 independent random points: 0.017 × mean, 15%. The zeros look like eigenvalues, not like random points.

### What this does and does not give (honest)

- **Known:** the circle picture is Li's criterion (Li 1997; Bombieri–Lagarias 1999) and the Hilbert–Pólya idea (Pólya, Hilbert, about 1914; Montgomery–Dyson 1973; Odlyzko's numerics; Katz–Sarnak for function fields, where it is a theorem: the zeros are eigenvalues of Frobenius, Deligne 1974).
- **The catch:** building a unitary matrix whose eigenvalues are the known zeros is trivial (put e^(iθ) on a diagonal). The whole difficulty is an operator built from the primes, not from the zeros, whose eigenvalues are provably the zeros. The explicit formula (zeros ↔ prime powers) has the shape of a trace formula, which is why people expect such an operator. Candidates: Berry–Keating (H = xp, 1999), Connes (adelic, 1999), Bender–Brody–Müller (2017; disputed). None is proven to work.
- **Look-alike test:** the circle by itself is a restatement. Any operator proposed must fail for Davenport–Heilbronn (its zeros are not on the circle), so it must use the Euler product.

&#91;image: The map w = 1 − 1/s, distance from the circle for ζ and Davenport–Heilbronn, Li's coefficients, and zeros against random unitary eigenvalues. Script: hilbert_polya.py.\]

| File | What it does |
| --- | --- |
| hilbert\_polya.py | The Li/Cayley map w = 1 − 1/s, zeros on the unit circle, Li's λₙ, Davenport–Heilbronn off the circle, CUE eigenvalues vs zeros. |

## Session 2, continued: the cycle matrix, eigenspaces of Collatz cycles (Nov 25, 2026)

### Journey log, continued

| Step | Idea or question | What we found |
| --- | --- | --- |
| 51 | The user's zip `Fleurdelys_Cycle_Kernel_Plots`: an eigenspace view of the Collatz cycles at −17 and 1 | Kept as delivered in `cycle_kernels/` and reproduced exactly. Its matrix B is a weighted cyclic shift. Eigenvalues: a regular polygon of radius μ^(1/p). Eigenvectors: Fourier modes times one profile that follows the cycle itself. The cycle is the resolvent q = (I − B)⁻¹e, the classical cycle equation. A new positive cycle would need a polygon just inside the unit circle, which gives the known length bounds (Eliahou's 17,087,915 comes out exactly). |

### What the zip contains (`cycle_kernels/`)

- **The matrix.** For a p-cycle q₀, …, q_(p−1) of the complex Collatz map f, put a_j = f′(q_j) and B[(j + 1) mod p, j] = a_j, zeros elsewhere. It acts on small perturbations of all cycle points at once. Bᵖ = μI with μ = a₀a₁⋯a_(p−1), the cycle's multiplier.
- **The figures.** Basins next to −17 (period 18) and 1 (period 3); the eigenvalues of B for the integer cycle and its twin; the phase of every eigenvector of the attracting cycle; twin primes in the radius n, angle n spiral.
- **Reproduced here** (`python cycle_kernels/plot_cycle_kernels.py`, 24 s): twin offsets 4.4303563429·10⁻⁷ and 0.0014721821280, basin shares 40.4% and 35.9%, the same as the delivered JSON. These match our own earlier table (offsets 4.4·10⁻⁷ and 1.5·10⁻³, twin multiplier 0.94 at −17).
- **Twin primes picture:** the counts are right (19 pairs up to 300, 205 up to 10⁴). It is the same view as our earlier `petal_spiral.py` twin panel.
- **Basins:** their −17 panel zooms on the basin piece at −17 itself; our `collatz_julia_cycles.py` zoomed on the piece at −34, the one that holds a critical point. Both belong to the same attracting twin, whose return map has degree 2¹¹ = 2048.
- One change: the script now writes to `output/cycle_kernels` by default and writes README/ZIP only with `--package`. Before, running it with `--out .` from the repository root would have overwritten the repository README. The change is recorded at the end of `cycle_kernels/README.md`.

### What B knows (`cycle_matrix.py`)

Each fact below has a short algebraic proof; the code checks each one numerically.

1. **Eigenvalues: a regular polygon.** The eigenvalues are the p-th roots of μ, a regular p-gon on the circle of radius μ^(1/p). For an integer cycle μ = 3ᵏ/2ᵐ (k odd steps, m even steps). The polygon is on the unit circle only if 3ᵏ = 2ᵐ, which never happens. Inside means attracting, outside means repelling.

| Cycle | p | k | m | μ | radius | twin μ | twin radius | 2ᵐ − 3ᵏ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 → 4 → 2 | 3 | 1 | 2 | 0.75 | 0.9086 | 1.2768 | 1.0849 | 1 |
| −1 → −2 | 2 | 1 | 1 | 1.5 | 1.2247 | 0.4987 | 0.7062 | −1 |
| −5 → … | 5 | 2 | 3 | 1.125 | 1.0238 | 0.8829 | 0.9754 | −1 |
| −17 → … | 18 | 7 | 11 | 1.0679 | 1.0037 | 0.9356 | 0.9963 | −139 |

   The integer cycle and its twin always sit on opposite sides of the unit circle (the multipliers add up to about 2: 2.027, 1.999, 2.008, 2.003).

2. **Eigenvectors: Fourier modes times one profile.** B = D(μ^(1/p)P)D⁻¹, where P is the plain cyclic shift and D is diagonal. So every eigenvector is v_j = |v_j|·e^(−2πijk/p): a discrete Fourier mode times one magnitude profile shared by all p eigenvectors. On the uploaded data, the phase panel equals the DFT matrix to 2.8·10⁻¹⁴, and the magnitudes agree across columns to 6·10⁻¹⁶. So the phase picture only knows p. The Collatz information is in the magnitudes, which the phase picture leaves out: the profile goes ×3 at odd steps and ÷2 at even steps, with the drift removed. It follows the cycle's own orbit |q_j|/μ^(j/p) (correlation of the logs: 0.9998 for −17, 0.994 for 1 → 4 → 2).

3. **The cycle is the resolvent of B at 1.** Along an integer cycle q_(j+1) = a_j q_j + ε_j, with ε_j = 1 at odd steps (3n + 1) and 0 at even steps (n/2). So q = Bq + e, and q = (I − B)⁻¹e. Also det(I − B) = 1 − μ = (2ᵐ − 3ᵏ)/2ᵐ, which is −139/2048 for −17. This is the classical cycle equation (Böhm–Sontacchi 1978) in matrix form, checked to 10⁻¹². Every parity pattern (a word of odd and even steps) gives exactly one rational cycle (Lagarias 1990, "rational cycles"). Of all 8,388,606 patterns up to length 22, 103 give integers, and they are exactly the 5 known cycles: 0, (1, 4, 2), (−1, −2), (−5, …), (−17, …). Large cycle numbers need μ close to 1, that is, a polygon vertex close to the point 1.

4. **A new positive cycle needs a polygon just inside the unit circle.** For a positive cycle ∏(1 + 1/(3n)) over its odd members equals 2ᵐ/3ᵏ. So if every odd member is at least N₀, then 0 < m log 2 − k log 3 ≤ k/(3N₀): m/k must approximate log₂ 3 from above, unusually well. Best approximations come from the continued fraction of log₂ 3. Results:

| Every odd member at least | needs at least |
| --- | --- |
| 1 | k = 1, m = 2 (the 1 → 4 → 2 cycle itself fits) |
| 1000 | k = 41, m = 65 |
| 10⁶ | k = 2966, m = 4701 |
| 2⁴⁰ | m = 17,087,915 halvings (k = 10,781,274) |
| 2⁶⁸ | m = 114,208,327,604 (k = 72,057,431,991; 186,265,759,595 steps in all) |

   The 2⁴⁰ row is exactly Eliahou's 1993 bound (cycle length counted in halvings, given that every n below 2⁴⁰ was checked to reach 1). The 2⁶⁸ row uses the computer check up to 2⁶⁸ (Barina). As far as I recall, 186,265,759,595 is also the bound in Hercher (2023); literature check to do. This is the Steiner (1977) / Eliahou method, drawn as how close the polygon may come to the unit circle.

### Connections to the rest of the journey

- **Hilbert–Pólya (step 50).** There, RH says the zeros sit exactly on a circle. Here a cycle's eigenvalues can never sit exactly on the unit circle (3ᵏ ≠ 2ᵐ), and a new positive cycle would have to come extremely close to it from inside. The integer cycle and its twin straddle the circle, a bit like a Davenport–Heilbronn off-line zero and its mirror. This is an analogy only: the Collatz pair comes from holomorphic dynamics (two nearby fixed points, multipliers adding to about 2), the Davenport–Heilbronn pair from the functional equation's symmetry.
- **Fourier.** B is a weighted circulant, and the Fourier transform diagonalizes every circulant. That is why the eigenvectors are DFT modes.
- **Redheffer (step 49).** Another simple matrix whose determinant holds the arithmetic: the Mertens function there, 2ᵐ − 3ᵏ here.
- **log₂ 3 and continued fractions** (an open thread): panel (d) is exactly that thread.

### Honest status

- Everything here is known or a short repackaging of known facts. B holds no information beyond the parity pattern: its spectrum knows only μ and p, its eigenvectors only the orbit, and its resolvent is the cycle equation.
- The one part that depends on the chosen complex extension is the twin's B (its μ, its basin). The integer B does not depend on the extension.
- Proven: facts 1–3 (algebra) and the inequality in 4. Computer-checked: the search over all patterns up to length 22, and the bounds above, which rest on published verifications up to 2⁴⁰ and 2⁶⁸.

&#91;image: Eigenvalue polygons of the cycle matrix B, eigenvectors as Fourier modes times one profile, the resolvent over all parity patterns, and how close a new cycle's polygon must come to the unit circle. Script: cycle_matrix.py.\]

| File | What it does |
| --- | --- |
| cycle\_kernels/ | The user's zip as delivered (README, script, data, two figures); `--out` default changed to output/cycle\_kernels. |
| cycle\_matrix.py | What the cycle matrix B knows: polygon eigenvalues, Fourier eigenvectors, the resolvent cycle equation over all parity patterns, cycle-length bounds from log₂ 3. |
