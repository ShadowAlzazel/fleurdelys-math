"""Test a property on zeta, on a sibling with an Euler product, and on a look-alike.

Before sharing an observation about the flower, run it here:

    zeta       the Riemann zeta function                      zeros on the line (RH: all of them)
    L4         L(s, chi_4), chi_4 the character mod 4        Euler product; zeros on the line (GRH,
                                                              checked numerically far beyond our range)
    DH         the Davenport-Heilbronn function (mod 5)      same kind of functional equation,
                                                              NO Euler product, zeros OFF the line

A property that could lead to RH should hold for zeta and L4 and FAIL for DH.
If it also holds for DH, it does not use the primes, so it cannot imply RH.
If it fails for L4, it is probably special to zeta for a reason unrelated to RH, or wrong.

Each function comes with:
    value(s)        the function itself
    completed(s)    the completed function (xi for zeta), symmetric about the line
    logderiv(s)     completed'(s) / completed(s)

Write a property as a Python function prop(F, sigma, t) -> True / False, then

    python lookalikes.py                     # runs the built-in example (target D)

or from your own script:

    from lookalikes import FUNCS, run
    run(my_prop, sigmas=[0.6, 0.7, 0.8], ts=numpy.linspace(84, 88, 41))
"""
import mpmath as mp
import numpy as np

mp.mp.dps = 20


class Func:
    def __init__(self, name, value, completed_factor_logderiv, completed_factor):
        self.name = name
        self._value = value
        self._fl = completed_factor_logderiv
        self._f = completed_factor

    def value(self, s):
        return self._value(mp.mpc(s))

    def completed(self, s):
        s = mp.mpc(s)
        return self._f(s) * self._value(s)

    def logderiv(self, s):
        s = mp.mpc(s)
        return self._fl(s) + mp.diff(self._value, s) / self._value(s)


# zeta: xi(s) = s(s-1)/2 * pi^(-s/2) Gamma(s/2) zeta(s)
ZETA = Func(
    "zeta",
    mp.zeta,
    lambda s: 1 / s + 1 / (s - 1) - mp.log(mp.pi) / 2 + mp.digamma(s / 2) / 2,
    lambda s: s * (s - 1) / 2 * mp.pi ** (-s / 2) * mp.gamma(s / 2),
)

# L(s, chi_4): odd character mod 4, Lambda(s) = (4/pi)^((s+1)/2) Gamma((s+1)/2) L(s)
_CHI4 = [0, 1, 0, -1]
L4 = Func(
    "L4",
    lambda s: mp.dirichlet(s, _CHI4),
    lambda s: mp.log(4 / mp.pi) / 2 + mp.digamma((s + 1) / 2) / 2,
    lambda s: (4 / mp.pi) ** ((s + 1) / 2) * mp.gamma((s + 1) / 2),
)

# Davenport-Heilbronn: two odd characters mod 5, Lambda(s) = (5/pi)^((s+1)/2) Gamma((s+1)/2) f(s)
_R5 = mp.sqrt(5)
_K = (mp.sqrt(10 - 2 * _R5) - 2) / (_R5 - 1)
_CHI = [0, 1, 1j, -1j, -1]
_CHIB = [0, 1, -1j, 1j, -1]
DH = Func(
    "DH",
    lambda s: (1 - 1j * _K) / 2 * mp.dirichlet(s, _CHI) + (1 + 1j * _K) / 2 * mp.dirichlet(s, _CHIB),
    lambda s: mp.log(5 / mp.pi) / 2 + mp.digamma((s + 1) / 2) / 2,
    lambda s: (5 / mp.pi) ** ((s + 1) / 2) * mp.gamma((s + 1) / 2),
)

FUNCS = [ZETA, L4, DH]


def run(prop, sigmas, ts, funcs=FUNCS, label="property"):
    """Evaluate prop(F, sigma, t) on the grid for each function; print and return pass rates."""
    out = {}
    print(f"{label}: sigma in {list(sigmas)}, t from {ts[0]:g} to {ts[-1]:g} ({len(ts)} values)")
    for F in funcs:
        ok = [bool(prop(F, s, t)) for s in sigmas for t in ts]
        out[F.name] = np.mean(ok)
        verdict = "holds everywhere" if all(ok) else f"FAILS at {ok.count(False)} of {len(ok)} points"
        print(f"   {F.name:5s}: {verdict}")
    return out


def newton_moves_toward_line(F, sigma, t):
    """Target D: one Newton step for the completed function, started right of the line, moves left."""
    return float(mp.re(1 / F.logderiv(mp.mpc(sigma, t)))) > 0


if __name__ == "__main__":
    # Example: target D near the Davenport-Heilbronn off-line zero 0.80852 + 85.69935i
    run(newton_moves_toward_line, sigmas=[0.55, 0.65, 0.75, 0.85, 0.95], ts=np.linspace(84.5, 87, 26),
        label="Newton step for the completed function moves toward the line (target D)")
