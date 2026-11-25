"""Build index.html (the follow-along journey as a web page) from JOURNEY.md.

JOURNEY.md stays the source; this script turns it into a styled page with the gallery pictures,
Proven / Open / Observed tags, a contents rail on wide screens, and a drawing of the flower
ζ(1/2 + it) in the header (computed here with zeta_fast).

    python make_journey_html.py                       # index.html at the repo root (for GitHub Pages)
    python make_journey_html.py --fragment --links text --out page.html
        # body-only page with repository links shown as plain names (for hosts that add their own
        # <html> skeleton and do not serve the repository files)
"""
import argparse
import html
import re
import unicodedata

import markdown
import numpy as np

from zeta_fast import zeta

TITLE = "Fleurdelys Journey"
DESC = ("A follow-along journey around the Riemann zeta function in 26 pictures. "
        "Not a proof of RH: every claim is tagged proven, open or observed.")
FONTS = ("https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@500;600;700"
         "&family=STIX+Two+Text:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap")

CSS = """
/* Layout: one reading column (about 68ch) with a sticky contents rail on wide screens;
   figures break out wider than the text. Petal orange and line blue come from the figures. */
:root {
  --paper: #f5f6f9; --surface: #ffffff; --ink: #1b2230; --muted: #586275; --rule: #d8dde7;
  --petal: #cf5428; --line: #2563b8;
  --proven: #1d7f54; --open: #a8681a; --observed: #2563b8;
  --proven-bg: #e3f3ea; --open-bg: #f8ecd9; --observed-bg: #e3edfa;
  --font-display: "Instrument Sans", "Helvetica Neue", Arial, sans-serif;
  --font-body: "STIX Two Text", "Cambria Math", Cambria, Georgia, serif;
  --font-mono: "IBM Plex Mono", ui-monospace, "SFMono-Regular", Menlo, monospace;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --paper: #10141c; --surface: #171d28; --ink: #e3e7ef; --muted: #9aa4b5; --rule: #29313f;
    --petal: #f0804f; --line: #73a9ee;
    --proven: #5fcf98; --open: #e6b25c; --observed: #73a9ee;
    --proven-bg: #173226; --open-bg: #3a2c15; --observed-bg: #18294a;
    color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --paper: #10141c; --surface: #171d28; --ink: #e3e7ef; --muted: #9aa4b5; --rule: #29313f;
  --petal: #f0804f; --line: #73a9ee;
  --proven: #5fcf98; --open: #e6b25c; --observed: #73a9ee;
  --proven-bg: #173226; --open-bg: #3a2c15; --observed-bg: #18294a;
  color-scheme: dark;
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--paper); color: var(--ink);
  font-family: var(--font-body); font-size: 1.125rem; line-height: 1.62;
  padding-left: max(16px, env(safe-area-inset-left, 0px));
  padding-right: max(16px, env(safe-area-inset-right, 0px));
}
a { color: var(--line); text-underline-offset: 0.18em; }
a:focus-visible, summary:focus-visible { outline: 2px solid var(--petal); outline-offset: 2px; border-radius: 2px; }
.shell { display: grid; grid-template-columns: minmax(0, 1fr); max-width: 1180px; margin: 0 auto; gap: 3rem; }
@media (min-width: 1100px) { .shell { grid-template-columns: 220px minmax(0, 1fr); } }
.rail { display: none; }
@media (min-width: 1100px) {
  .rail { display: block; position: sticky; top: calc(env(safe-area-inset-top, 0px) + 1.5rem); align-self: start;
          padding-block: 2rem; font-family: var(--font-display); font-size: 0.86rem; }
  .rail ol { list-style: none; margin: 0; padding: 0; display: grid; gap: 0.35rem; }
  .rail a { color: var(--muted); text-decoration: none; display: grid; grid-template-columns: 1.8rem 1fr; }
  .rail a:hover, .rail a.here { color: var(--ink); }
  .rail a.here .n { color: var(--petal); }
  .rail .n { font-family: var(--font-mono); font-size: 0.78rem; padding-top: 0.1rem; color: var(--muted); }
  .rail .label { font-size: 0.72rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); margin-bottom: 0.8rem; }
}
main { min-width: 0; max-width: 46rem; padding-block: 1rem 5rem; }
header.hero { display: grid; grid-template-columns: minmax(0, 1fr); gap: 1.5rem; align-items: center;
              padding-block: 3rem 2rem; border-bottom: 1px solid var(--rule); margin-bottom: 2rem; }
@media (min-width: 720px) { header.hero { grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); } }
.eyebrow { font-family: var(--font-display); font-size: 0.78rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--petal); margin: 0 0 0.6rem; }
.hero h1 { font-family: var(--font-display); font-weight: 700; font-size: clamp(2.6rem, 7vw, 4rem); line-height: 1; margin: 0 0 0.8rem; letter-spacing: -0.02em; }
.hero .sub { font-size: 1.3rem; margin: 0 0 1rem; color: var(--ink); text-wrap: balance; }
.hero .meta { font-family: var(--font-mono); font-size: 0.8rem; color: var(--muted); margin: 0; }
.flower { margin: 0; }
.flower svg { width: 100%; max-width: 360px; height: auto; display: block; margin-inline: auto; }
.flower figcaption { font-family: var(--font-display); font-size: 0.8rem; color: var(--muted); text-align: center; margin-top: 0.4rem; }
main h1:not(.title) { display: none; }
h2, h3 { font-family: var(--font-display); line-height: 1.2; text-wrap: balance; }
h2 { font-size: 1.75rem; font-weight: 700; margin: 3.5rem 0 1rem; padding-top: 1.2rem; border-top: 1px solid var(--rule); scroll-margin-top: 1.5rem; }
h2 .num { color: var(--petal); font-family: var(--font-mono); font-weight: 500; font-size: 1.1rem; margin-right: 0.6rem; vertical-align: 0.15em; }
h3 { font-size: 1.2rem; font-weight: 600; margin: 2rem 0 0.6rem; scroll-margin-top: 1.5rem; }
p, li { max-width: 68ch; }
ul, ol { padding-left: 1.3rem; }
li { margin-block: 0.3rem; }
li::marker { color: var(--muted); }
hr { display: none; }  /* section headings carry their own rule */
@media (min-width: 1100px) { #contents, #contents + ol { display: none; } }  /* the rail replaces the inline contents */
strong { font-weight: 600; }
code { font-family: var(--font-mono); font-size: 0.86em; background: var(--surface); border: 1px solid var(--rule); border-radius: 4px; padding: 0.05em 0.3em; }
pre { overflow-x: auto; background: var(--surface); border: 1px solid var(--rule); border-radius: 6px; padding: 1rem; font-size: 0.9rem; }
pre code { border: 0; padding: 0; background: none; }
figure.fig { margin: 2rem 0; }
@media (min-width: 900px) { figure.fig { margin-inline: -4rem; } }
figure.fig img { display: block; width: 100%; max-width: 100%; height: auto; border: 1px solid var(--rule); border-radius: 6px; background: #fff; }
figure.fig figcaption { font-family: var(--font-display); font-size: 0.86rem; color: var(--muted); margin-top: 0.5rem; max-width: 68ch; }
@media (min-width: 900px) { figure.fig figcaption { margin-inline: 4rem; } }
.tag { display: inline-block; font-family: var(--font-display); font-size: 0.72em; font-weight: 600; letter-spacing: 0.04em;
       text-transform: uppercase; padding: 0.08em 0.5em; border-radius: 999px; vertical-align: 0.1em; line-height: 1.5; }
.tag-proven { color: var(--proven); background: var(--proven-bg); }
.tag-open { color: var(--open); background: var(--open-bg); }
.tag-observed { color: var(--observed); background: var(--observed-bg); }
.table-wrap { overflow-x: auto; margin: 1.5rem 0; }
table { border-collapse: collapse; width: 100%; font-size: 0.95rem; }
th, td { text-align: left; vertical-align: top; padding: 0.55rem 0.8rem 0.55rem 0; border-bottom: 1px solid var(--rule); }
th { font-family: var(--font-display); font-size: 0.78rem; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); font-weight: 600; }
.repo-file { font-family: var(--font-mono); font-size: 0.86em; }
footer { font-family: var(--font-display); font-size: 0.85rem; color: var(--muted); border-top: 1px solid var(--rule); padding-top: 1.2rem; margin-top: 3rem; }
@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
@media (prefers-reduced-motion: no-preference) { html { scroll-behavior: smooth; } }
"""

SCRIPT = """
<script>
(function () {
  var links = Array.prototype.slice.call(document.querySelectorAll('.rail a'));
  if (!links.length || !('IntersectionObserver' in window)) return;
  var byId = {};
  links.forEach(function (a) { byId[decodeURIComponent(a.getAttribute('href').slice(1))] = a; });
  var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting && byId[e.target.id]) {
        links.forEach(function (a) { a.classList.remove('here'); });
        byId[e.target.id].classList.add('here');
      }
    });
  }, { rootMargin: '0px 0px -55% 0px' });
  document.querySelectorAll('main h2[id]').forEach(function (h) { obs.observe(h); });
})();
</script>
"""


def github_slug(text):
    """GitHub-style heading anchor: lowercase, drop punctuation (keep letters in any script), spaces -> hyphens."""
    text = html.unescape(re.sub(r"<[^>]+>", "", text)).strip().lower()
    out = []
    for ch in text:
        cat = unicodedata.category(ch)
        if ch in " -" or cat[0] in "LN" or ch == "_":
            out.append("-" if ch == " " else ch)
    return "".join(out)


def flower_svg(tmax=50.0, n=2400):
    t = np.linspace(0.0, tmax, n)
    z = zeta(0.5 + 1j * t, N=40)
    x, y = z.real, -z.imag                   # SVG y points down; flip so the picture matches the plots
    pad = 0.25
    x0, x1, y0, y1 = x.min() - pad, x.max() + pad, y.min() - pad, y.max() + pad
    pts = " ".join(f"{a:.3f},{b:.3f}" for a, b in zip(x, y))
    return (f'<svg viewBox="{x0:.2f} {y0:.2f} {x1 - x0:.2f} {y1 - y0:.2f}" role="img" '
            f'aria-label="The flower: the curve traced by zeta(1/2 + it) for t from 0 to {tmax:g}">'
            f'<line x1="{x0:.2f}" y1="0" x2="{x1:.2f}" y2="0" stroke="var(--rule)" stroke-width="0.02"/>'
            f'<line x1="0" y1="{y0:.2f}" x2="0" y2="{y1:.2f}" stroke="var(--rule)" stroke-width="0.02"/>'
            f'<polyline points="{pts}" fill="none" stroke="var(--petal)" stroke-width="0.028" stroke-linejoin="round"/>'
            f'<circle cx="0" cy="0" r="0.07" fill="var(--ink)"/></svg>')


def social_card(path="images/social_card.png", tmax=50.0):
    """1200 x 630 preview picture for link cards (X, Bluesky, Mastodon, Slack...)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    t = np.linspace(0.0, tmax, 4000)
    z = zeta(0.5 + 1j * t, N=40)
    fig = plt.figure(figsize=(12, 6.3), dpi=100)
    fig.patch.set_facecolor("#10141c")
    ax = fig.add_axes([0.52, 0.06, 0.46, 0.88])
    ax.set_facecolor("#10141c")
    ax.axhline(0, color="#29313f", lw=1)
    ax.axvline(0, color="#29313f", lw=1)
    ax.plot(z.real, z.imag, color="#f0804f", lw=1.6)
    ax.plot([0], [0], "o", color="#e3e7ef", ms=7)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.text(0.06, 0.70, "Fleurdelys", color="#e3e7ef", fontsize=58, fontweight="bold")
    fig.text(0.06, 0.55, "The Riemann zeta function,\ndrawn as a flower", color="#e3e7ef", fontsize=24, va="top", linespacing=1.3)
    fig.text(0.06, 0.30, "A follow-along journey in 26 pictures.\nEvery claim tagged proven, open or observed.",
             color="#9aa4b5", fontsize=16, va="top", linespacing=1.4)
    fig.text(0.06, 0.08, "ζ(½ + it), 0 ≤ t ≤ 50: each pass through the dot is a zero", color="#9aa4b5", fontsize=12)
    fig.savefig(path, facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


def tagify(s):
    names = "Proven|Open|Observed"
    s = re.sub(rf"<strong>({names}):?</strong>:?", lambda m: f'<span class="tag tag-{m.group(1).lower()}">{m.group(1)}</span>', s)
    s = re.sub(rf"\((?:<strong>)?({names})(?:</strong>)?", lambda m: f'(<span class="tag tag-{m.group(1).lower()}">{m.group(1)}</span>', s)
    s = re.sub(rf"<td>({names})\b", lambda m: f'<td><span class="tag tag-{m.group(1).lower()}">{m.group(1)}</span>', s)
    return s


def build(md_text, links):
    body = markdown.markdown(md_text, extensions=["tables", "fenced_code", "sane_lists"])
    # headings get GitHub-style ids; numbered chapter headings get a styled number
    toc = []

    def head(m):
        level, inner = m.group(1), m.group(2)
        hid = github_slug(inner)
        if level == "2":
            num = re.match(r"(\d+)\.\s+(.*)", inner)
            if num:
                toc.append((hid, num.group(1), num.group(2)))
                inner = f'<span class="num">{num.group(1)}</span>{num.group(2)}'
        return f'<h{level} id="{hid}">{inner}</h{level}>'
    body = re.sub(r"<h([23])>(.*?)</h\1>", head, body)
    # images become figures with the alt text as caption, linking to the full picture
    body = re.sub(r'<p><img alt="([^"]*)" src="([^"]+)" ?/?></p>',
                  lambda m: (f'<figure class="fig"><a href="{m.group(2)}"><img src="{m.group(2)}" alt="{m.group(1)}" loading="lazy"></a>'
                             f'<figcaption>{m.group(1)}</figcaption></figure>'), body)
    body = re.sub(r"<table>", '<div class="table-wrap"><table>', body).replace("</table>", "</table></div>")
    body = tagify(body)
    if links == "text":
        def relink(m):
            href, text = m.group(1), m.group(2)
            if href.startswith(("#", "http", "images/")):
                return m.group(0)
            return f'<span class="repo-file" title="in the project repository">{text}</span>'
        body = re.sub(r'<a href="([^"]+)">(.*?)</a>', relink, body)
    # drop the markdown title and intro line: the hero replaces them
    body = re.sub(r"^<h1>.*?</h1>\s*<p><em>.*?</em></p>", "", body, flags=re.S)
    rail = "".join(f'<li><a href="#{h}"><span class="n">{n}</span><span>{html.escape(html.unescape(t))}</span></a></li>' for h, n, t in toc)
    hero = (f'<header class="hero"><div><p class="eyebrow">An exploration in pictures · November 2026</p>'
            f'<h1 class="title">Fleurdelys</h1>'
            f'<p class="sub">A follow-along journey around the Riemann zeta function, one picture at a time.</p>'
            f'<p class="meta">{len(toc)} sections · {body.count("<figure")} pictures · every claim tagged '
            f'<span class="tag tag-proven">Proven</span> <span class="tag tag-open">Open</span> '
            f'<span class="tag tag-observed">Observed</span></p></div>'
            f'<figure class="flower">{flower_svg()}<figcaption>The flower, ζ(½ + it) for 0 ≤ t ≤ 50. '
            f'Each pass through the dot is a zero; there are 10.</figcaption></figure></header>')
    page = (f'<div class="shell"><nav class="rail" aria-label="Contents"><div class="label">Contents</div><ol>{rail}</ol></nav>'
            f'<main>{hero}{body}<footer>Built from JOURNEY.md in the project repository. Pictures are reduced copies; '
            f'each names the script that draws it at full size.</footer></main></div>')
    return page


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="JOURNEY.md")
    ap.add_argument("--out", default="index.html")
    ap.add_argument("--links", choices=["repo", "text"], default="repo",
                    help="repo: keep links to repository files; text: show them as plain names")
    ap.add_argument("--fragment", action="store_true", help="omit <!doctype>, <html>, <head> and <body>")
    ap.add_argument("--site", default="https://shadowalzazel.github.io/fleurdelys-math/",
                    help="public address of the page, for link previews (must end with /)")
    a = ap.parse_args()
    social_card()
    page = build(open(a.src, encoding="utf-8").read(), a.links)
    head = (f'<title>{TITLE}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            f'<meta name="description" content="{DESC}">\n'
            f'<meta property="og:type" content="article">\n<meta property="og:title" content="Fleurdelys: the Riemann zeta function as a flower">\n'
            f'<meta property="og:description" content="{DESC}">\n<meta property="og:url" content="{a.site}">\n'
            f'<meta property="og:image" content="{a.site}images/social_card.png">\n'
            f'<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
            f'<meta property="og:image:alt" content="The flower traced by the Riemann zeta function on the critical line">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="twitter:title" content="Fleurdelys: the Riemann zeta function as a flower">\n'
            f'<meta name="twitter:description" content="{DESC}">\n'
            f'<meta name="twitter:image" content="{a.site}images/social_card.png">\n'
            f'<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            f'<link rel="stylesheet" href="{FONTS}">\n<style>{CSS}</style>\n')
    if a.fragment:
        doc = head + page + SCRIPT
    else:
        doc = (f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
               f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
               f'{head}</head>\n<body>\n{page}\n{SCRIPT}</body>\n</html>\n')
    open(a.out, "w", encoding="utf-8").write(doc)
    print(f"wrote {a.out}: {len(doc) / 1024:.0f} KB, {page.count('<figure class=\"fig\"')} figures, "
          f"{page.count('class=\"tag ')} tags, links = {a.links}")
