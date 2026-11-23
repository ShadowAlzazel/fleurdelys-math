# What your observation needs: a checklist before sharing

Nov 23, 2026 · @ShadowAlzazel

To be a step toward RH, an observation has to prove one of four statements (targets A–D below) for every height, and somewhere it has to use the primes. This checklist turns that into nine checks you can run while you tweak the idea. Checks 1–4 decide whether it is precise, new and not circular. Checks 5–9 decide whether it could become a proof. A tweak that makes the claim weaker but provable is still worth having.

## The four targets

Each is proven equivalent to RH. Proving any one of them for ζ, at every height, proves RH.

| Target | In flower language |
| --- | --- |
| A. Counting | For every height T, the petals through the origin up to T number exactly N(T). |
| B. Off-line slices miss 0 | For every σ between ½ and 1, the curve t ↦ ζ(σ + it) never passes through 0. |
| C. No folds | ζ′ has no zeros in 0 < Re s < ½ (Speiser 1934). |
| D. A valley along the line | \|ξ(σ + it)\| strictly increases as σ moves away from ½ (Sondow–Dumitrescu 2010). Equivalently, every Newton step for ξ right of the line moves left (from Lagarias 1999). |

## The nine checks

1. **Write it as one sentence with every word pinned down.** Template: "For every [range], [object] has [property]." Name the function (ζ, ξ, Z, the flower curve, the Newton map for which c and which seed), the region (which σ, which t), and the quantifier: every, infinitely many, most, or up to height T.
   - Good: "For every t > 0 and every σ in (½, 1), |ξ(σ + it)| > |ξ(½ + it)|."
   - Too loose to check: "the petals always bloom in order."
2. **Say what kind of claim it is.** (a) Seen in pictures up to some height. (b) Believed for every height, a conjecture. (c) A step you think you can prove. Each needs different evidence, and mixing them is the most common way a good idea gets dismissed.
3. **Check it is not already a known equivalent of RH.** If it is, it is a reformulation: worth recording, but it needs a new reason to be true before it counts as progress. Besides A–D, known equivalents include:
   - Littlewood (1912): the Mertens function grows no faster than x^(½ + ε).
   - Riesz (1916): a growth condition on a series built from the Möbius function.
   - Nyman (1950) and Beurling (1955): an approximation problem in function spaces.
   - Weil (1952): positivity in the explicit formula.
   - Bagchi (1981): ζ approximates its own shifts.
   - Robin (1984): σ(n) < e^γ · n · log log n for every n > 5040.
   - Li (1997): a sequence of numbers built from the zeros is positive.
   - Lagarias (2002): a version of Robin's inequality using harmonic numbers.
   - De Bruijn–Newman: Λ ≤ 0. Rodgers–Tao proved Λ ≥ 0.
4. **Look for circularity.** Does any step quietly assume RH? Red flags:
   - counting petals as zeros of Z(t), which only sees zeros on the line;
   - Gram's law, which fails infinitely often;
   - "the flower never misses a petal" used as an input;
   - a numerical range treated as if it were every height;
   - assuming every zero is simple.
5. **Run the look-alike test, both ways.**
   - It must **fail** for the Davenport–Heilbronn function: same kind of functional equation, zeros off the line, no Euler product.
   - It should **hold** for a Dirichlet L-function with an Euler product, such as L(s, χ₄). If it fails there, it is probably special to ζ for a reason unrelated to RH, or wrong.
   - Run `lookalikes.py`. Target D shows the right pattern: it holds for ζ and L(s, χ₄) and fails for Davenport–Heilbronn at 13 of 130 points near its off-line zero.
6. **Check it does not need slack.** Does it rely on a margin: a fixed distance from 0, a minimum gap, a positive lower bound? Three proven facts break margin arguments:
   - Bohr: off-line curves come arbitrarily close to 0.
   - Rodgers–Tao: if RH holds, the zeros are only barely real.
   - The Lehmer pair at t ≈ 7005 reaches only 0.004 from the origin.

   An exact inequality that can be tight may survive; a uniform margin will not.
7. **Test every height you can, and say how it continues.** Check up to 10⁴ with `zeros.py`, near the closest pairs (#363–#364, the Lehmer pair), and where Gram's law fails. Then say why it should keep holding past what any computer can check.
8. **Name the step where the primes enter.** The Euler product, the explicit formula, or Landau's spectrum (the petals' spike of height log p at every prime power). If no step uses them, check 5 will fail.
9. **Compare with known results.** Look through the "What is proven" table and the "Results that came up in session 2" table in the notes. I will also search the literature when you share it.

## Weaker targets that are still real results

If the full claim does not survive, a weaker version often can. Each of these is a recognized kind of result:

| Weaker target | What is known now |
| --- | --- |
| A positive share of zeros on the line | At least 40% (Conrey 1989) |
| A zero-free region near Re s = 1 | Proven since 1896; wider regions are active research |
| Few zeros far from the line (zero-density) | Many theorems; recent improvements by Guth and Maynard (2024) |
| A new equivalent form of RH with a clean picture | Worth writing up even without a proof |
| A numerical phenomenon checked to a stated height | Worth sharing if it is precise and reproducible |

## What to bring when you share it

1. The one-sentence statement from check 1.
2. Its kind from check 2.
3. One picture, and the range of t you checked.
4. Which target (A–D) it aims at, or which weaker target.
5. The step where the primes enter.

What I will do with it: draw it for ζ, L(s, χ₄) and Davenport–Heilbronn side by side, check it against known equivalent forms, search for earlier work, and tell you plainly what holds and what breaks.
