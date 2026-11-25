"""Build images/: small copies of every journey picture, in journey order, plus images/README.md.

The full-size pictures live in output/ (git-ignored) and are redrawn by their scripts. This keeps a
light copy of each (about 150-300 KB) in the repository so the journey can be browsed on GitHub.

    python make_gallery.py            # after running the scripts that draw the pictures
"""
import argparse
import io
from pathlib import Path

from PIL import Image

# (picture in output/, script, part of the journey, one-line caption)
GALLERY = [
    ("flower", "flower.py", "The flower", "The flower: ζ(½ + it) for t up to ±50 and ±1000. Every petal that passes through 0 is a zero of ζ."),
    ("newton_plane", "newton_plane.py", "The flower", "Newton's method on ζ, colored by which zero each starting point reaches."),
    ("mandelbrot_copy", "mandelbrot_copy.py", "The flower", "A Mandelbrot set copy in the parameter plane of the Newton family for ζ(s) − c (McMullen: Mandelbrot copies are universal)."),
    ("overlay", "overlay.py", "The flower", "The flower drawn on that parameter plane, with the Mandelbrot copy centers marked."),
    ("dh_flower", "davenport_heilbronn.py", "What a proof of RH must do", "ζ's flower beside the Davenport–Heilbronn function: the same kind of flower, but it has zeros off the line (no Euler product)."),
    ("newton_xi", "davenport_heilbronn.py", "What a proof of RH must do", "Newton steps for the completed functions: for ζ they always move toward the critical line; for Davenport–Heilbronn they break near its off-line zeros."),
    ("zero_polar", "zero_polar.py", "The petals hear the primes", "The zeros in the prime-spiral layout. The angles γ·log x lean toward π exactly when x is a prime power (Landau 1912)."),
    ("collatz_negative", "collatz_negative.py", "Collatz", "Collatz on negative numbers: every start down to −10⁶ ends in one of three cycles."),
    ("collatz_complex", "collatz_complex.py", "Collatz", "The complex Collatz map f(z) = (2 + 7z − (2 + 5z)cos πz)/4, with zooms at 0, 1, −1, −5."),
    ("collatz_julia", "collatz_julia.py", "Collatz", "A filled Julia set of z² + c hiding next to the cycle (−1, −2): 99.4% of pixels match (Douady–Hubbard)."),
    ("collatz_structure", "collatz_structure.py", "Collatz", "Structure in the steps plot: doubling chains, and 8k + 4, 8k + 5 merging after 3 steps (Terras 1976)."),
    ("collatz_polar", "collatz_polar.py", "Collatz", "Collatz in the prime-spiral layout. The arms come from the layout (2π ≈ 44/7), not from Collatz."),
    ("collatz_julia_cycles", "collatz_julia_cycles.py", "Collatz", "Julia set copies next to −2, −14 and −34 (return maps of degree 2, 8 and 2048)."),
    ("zeta_julia", "zeta_julia.py", "Julia copies around the flower", "Where the flower crosses a Mandelbrot copy, with the basilica and the rabbit in the s-plane."),
    ("petal_spiral", "petal_spiral.py", "Spirals and spectra", "Primes, twin primes, petals and twin petals in the spiral layout, at two scales."),
    ("petal_spectrum", "petal_spectrum.py", "Spirals and spectra", "The petal spectrum from 35,673 zeros: a spike of height log p at every prime power up to 100."),
    ("strip_spiral", "strip_spiral.py", "Spirals and spectra", "The critical strip wrapped onto a spiral (top view) and unrolled with Z(t) (side view)."),
    ("pair_spacing", "pair_spacing.py", "Spirals and spectra", "Pair correlation of the zeros and its Fourier transform, against random-matrix theory (Montgomery)."),
    ("zeta_spectroscopy", "zeta_spectroscopy.py", "Spirals and spectra", "Spectrogram of Z(t), with one chirp per integer n; the prime wave over all primes, twin primes and a random control."),
    ("prime_subsets", "prime_subsets.py", "Spirals and spectra", "How strongly twin, cousin, sexy and isolated primes show in the zeros, against matched random primes."),
    ("green_tao", "green_tao.py", "Prime patterns", "The first prime progressions of length 3 to 12, and their counts against the Green–Tao–Ziegler formula."),
    ("star_rotation", "star_rotation.py", "Prime patterns", "The star shape of 199 + 210j: a fixed turn per step, like a Mandelbrot orbit on the main cardioid's edge."),
    ("sunflowers", "sunflowers.py", "Other flowers", "Sunflowers (Vogel's model) for the golden angle, 1 radian and step 210: arm counts come from continued fractions."),
    ("other_flowers", "other_flowers.py", "Other flowers", "Flowers of six functions: the hourglass shape is shared by every L-function with real coefficients."),
    ("feigenbaum_zeta", "feigenbaum_zeta.py", "Feigenbaum and Fourier", "A period-doubling cascade in ζ's Newton family; the gap ratios approach Feigenbaum's δ = 4.669."),
    ("prime_fourier", "prime_fourier.py", "Feigenbaum and Fourier", "Fourier spectra of the primes, twin primes and Collatz step counts: lines at fractions a/q."),
    ("fleurdelys_3d", "fleurdelys_3d.py", "Feigenbaum and Fourier", "The 3D curve (Re ζ, Im ζ, t) along the critical line: the 'hourglass'."),
    ("zeta_bounce", "zeta_bounce.py", "The flower as a bouncing ball", "|Z(t)| bounces at each zero: phase portrait, elasticity, Gram's law, and the colliding blocks that count π."),
    ("twin_circle", "twin_circle.py", "Twin primes", "'A circle that holds every twin prime' as a restatement, the 3-5-7 triple, and counts against Hardy–Littlewood up to 10⁸."),
    ("chaos_bridges", "chaos_bridges.py", "Chaos", "Escape regions, ζ's Euler-product floor, Lyapunov exponents, and zero spacings (GUE vs random)."),
    ("petal_ledger", "petal_ledger.py", "Testing the targets", "The petal ledger: all zeros against petals through 0. Davenport–Heilbronn's deficit jumps by 2 at each off-line zero."),
    ("xi_pull", "xi_pull.py", "Testing the targets", "How strongly the critical line pulls Newton steps. Only Davenport–Heilbronn has pockets pushed away."),
    ("euler_product", "euler_product.py", "Testing the targets", "The Euler product: partial products never reach 0, the 3-4-1 trick, and log-coefficients only on prime powers."),
    ("eigen_rh", "eigen_rh.py", "Eigenvalues", "The Redheffer matrix (determinant = Mertens function), its eigenvalues, and zero spacings against a random matrix."),
    ("hilbert_polya", "hilbert_polya.py", "Eigenvalues", "Hilbert–Pólya: w = 1 − 1/s turns the critical line into the unit circle; RH ⇔ every zero on it (Li's criterion)."),
    ("cycle_matrix", "cycle_matrix.py", "Eigenvalues", "The Collatz cycle matrix: polygon eigenvalues, Fourier eigenvectors, the cycle equation, and cycle-length bounds."),
    ("zeta_determinants", "zeta_determinants.py", "Eigenvalues", "Zeta functions as determinants. Where RH is a theorem (graphs, curves over finite fields) it says: eigenvalues on a circle."),
]

INTRO = """# Fleurdelys: picture gallery

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
"""


def shrink(src, dst_stem, width):
    im = Image.open(src).convert("RGB")
    s = min(1.0, width / im.size[0])
    im = im.resize((round(im.size[0] * s), round(im.size[1] * s)), Image.LANCZOS)
    png = io.BytesIO()
    im.quantize(256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(png, "PNG", optimize=True)
    if png.tell() <= 300 * 1024:
        data, ext = png.getvalue(), ".png"
    else:
        jpg = io.BytesIO()
        im.save(jpg, "JPEG", quality=82, optimize=True)
        data, ext = jpg.getvalue(), ".jpg"
    path = dst_stem.with_suffix(ext)
    path.write_bytes(data)
    return path


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="output")
    ap.add_argument("--dst", default="images")
    ap.add_argument("--width", type=int, default=1400)
    a = ap.parse_args()
    dst = Path(a.dst)
    dst.mkdir(exist_ok=True)
    lines = [INTRO]
    part = None
    total = 0
    for i, (name, script, section, caption) in enumerate(GALLERY, 1):
        src = Path(a.src) / f"{name}.png"
        if not src.exists():
            print(f"missing {src}: run {script} first")
            continue
        for old in dst.glob(f"{i:02d}_{name}.*"):
            old.unlink()
        path = shrink(src, dst / f"{i:02d}_{name}", a.width)
        total += path.stat().st_size
        if section != part:
            lines.append(f"\n## {section}\n")
            part = section
        lines.append(f"**{i}. {caption}** (`{script}`)\n\n![{caption}]({path.name})\n")
    lines.append("\n## The user's own figures\n\nTwo figures from the user's work on eigenspaces of Collatz cycles are kept at full size in "
                 "[`../cycle_kernels/`](../cycle_kernels/), with their own README.\n")
    lines.append("\n## Rebuilding\n\nRun the scripts (see the main README), then `python make_gallery.py`.\n")
    (dst / "README.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(GALLERY)} pictures, {total / 2**20:.1f} MB in {dst}/")
