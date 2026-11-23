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
