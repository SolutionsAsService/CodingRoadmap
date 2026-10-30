"""Build the Coding Roadmap site from _src/data/roadmap.json into site/.

    python _src/build.py

One page per line (track), a home page with the whole network drawn as a transit
map, an about page carrying the original ASCII roadmap, and a 404. Standard library
only; refuses to finish on a dead local link.
"""
import html
import json
import pathlib
import re

SRC = pathlib.Path(__file__).resolve().parent
ROOT = SRC.parent
SITE = ROOT / "site"
DATA = json.loads((SRC / "data" / "roadmap.json").read_text(encoding="utf-8"))
TRACKS = DATA["tracks"]
TRUNK = next(t for t in TRACKS if t.get("trunk"))
LINES = [t for t in TRACKS if not t.get("trunk")]
e = html.escape


def col(t):
    """The trunk is drawn in ink, so it flips with dark mode; other lines keep their colour."""
    return "var(--trunk)" if t.get("trunk") else t["color"]


def page(title, desc, body, current=None):
    out = (SRC / "layout.html").read_text(encoding="utf-8")
    nav = "".join(
        f'<li><a href="{t["id"]}.html" style="--c:{col(t)}"{" aria-current=\"page\"" if current == t["id"] else ""}><i aria-hidden="true"></i>{e(t["name"])}</a></li>'
        for t in TRACKS)
    out = out.replace("{{nav}}", nav).replace("{{title}}", e(title)).replace("{{description}}", e(desc)).replace("{{body}}", body)
    out = out.replace("{{cur:about}}", ' aria-current="page"' if current == "about" else "")
    assert "{{" not in out, title
    return out


def network_svg():
    """Fundamentals runs left to right; at its end each line branches off at 45 degrees, Beck-style."""
    gap, x0, y0, step = 135, 60, 84, 26
    trunk_end = x0 + gap * (len(TRUNK["stages"]) - 1)
    hub = trunk_end + 34 + step * len(LINES)
    rows = [y0 + 92 * (i + 1) for i in range(len(LINES))]
    # Line i leaves the trunk step*i to the left of the hub, so deeper lines run parallel
    # to the left of shallower ones and no line crosses another.
    starts = [hub - step * i for i in range(len(LINES))]
    bends = [sx + (y - y0) for sx, y in zip(starts, rows)]
    firsts = [bx + 84 for bx in bends]  # a short straight run, so first labels clear the deeper diagonals
    ends = [fx + gap * (len(t["stages"]) - 1) for fx, t in zip(firsts, LINES)]
    width = max(ends) + 80
    height = rows[-1] + 60
    s = [f'<svg class="net" viewBox="0 0 {width} {height}" role="img" aria-labelledby="net-t net-d">',
         f'<title id="net-t">The roadmap as a transit map</title>',
         f'<desc id="net-d">The Fundamentals line runs left to right through {len(TRUNK["stages"])} stations. At its end, '
         + ", ".join(f'{t["name"]} ({len(t["stages"])} stations)' for t in LINES) + ' branch off.</desc>']
    for t, y, sx, bx, x1, end in zip(LINES, rows, starts, bends, firsts, ends):
        s.append(f'<a href="{t["id"]}.html" class="ln"><path d="M{sx} {y0} L{bx} {y} H{end}" style="stroke:{col(t)}" class="track"/>')
        for i, st in enumerate(t["stages"]):
            x = x1 + gap * i
            s.append(f'<circle cx="{x}" cy="{y}" r="7" class="stop" style="stroke:{col(t)}"/>')
            s.append(f'<text x="{x}" y="{y + 32}" class="st" text-anchor="middle">{e(short(st["name"]))}</text>')
        s.append(f'<text x="{bx + 16}" y="{y - 16}" class="ln-name">{e(t["name"])}</text></a>')  # above the track, clear of the station names below
    s.append(f'<a href="{TRUNK["id"]}.html" class="ln"><path d="M{x0} {y0} H{hub}" style="stroke:{col(TRUNK)}" class="track trunk"/>')
    for i, st in enumerate(TRUNK["stages"]):
        x = x0 + gap * i
        s.append(f'<circle cx="{x}" cy="{y0}" r="7" class="stop" style="stroke:{col(TRUNK)}"/>')
        s.append(f'<text x="{x}" y="{y0 - 22}" class="st" text-anchor="middle">{e(short(st["name"]))}</text>')
    s.append(f'<rect x="{hub - 15}" y="{y0 - 15}" width="30" height="30" rx="15" class="hub"/></a>')
    s.append(f'<text x="{hub + 26}" y="{y0 - 22}" class="hub-name">Change here</text>')
    s.append("</svg>")
    return "\n".join(s)


def short(name):
    return {"Algorithms and data structures": "Algorithms", "Object-oriented programming": "OOP",
            "Server-side languages": "Server code", "Security and authentication": "Security",
            "Microservices and serverless": "Microservices", "CI/CD and deployment pipelines": "CI/CD",
            "Infrastructure as code": "IaC", "Monitoring and logs": "Monitoring", "Database management": "DB operations",
            "Python for machine learning": "Python ML", "Natural language processing": "NLP",
            "Frameworks and state": "Frameworks", "Languages and styling": "Styling", "UX and UI design": "UX/UI",
            "APIs and protocols": "APIs", "Cloud providers": "Cloud", "The web platform": "Web platform",
            "Model deployment": "Deployment", "Data engineering": "Data eng.", "Computer vision": "Vision",
            "First languages": "Languages", "Build and test": "Build & test"}.get(name, name)


def topic(name, url):
    return f'<li><a href="{e(url)}" rel="noopener">{e(name)}</a></li>' if url else f'<li><span>{e(name)}</span></li>'


def line_page(t, i):
    prev_t, next_t = TRACKS[i - 1] if i else None, TRACKS[i + 1] if i + 1 < len(TRACKS) else None
    stations = "".join(
        f'''<li class="station"><h2 id="s{n}"><span class="num" aria-hidden="true">{n + 1:02d}</span>{e(st["name"])}</h2>
  <p>{e(st["note"])}</p>{('<ul class="topics" aria-label="' + e(st["name"]) + ': tools and topics">' + "".join(topic(a, b) for a, b in st["topics"]) + "</ul>") if st["topics"] else ""}</li>'''
        for n, st in enumerate(t["stages"]))
    start = ("Start here." if t.get("trunk") else
             f'Change here from the end of <a href="{TRUNK["id"]}.html">{e(TRUNK["name"])}</a>.')
    pager = "".join(x for x in [
        f'<a class="pg prev" href="{prev_t["id"]}.html" style="--c:{col(prev_t)}"><small>Previous line</small>{e(prev_t["name"])}</a>' if prev_t else "",
        f'<a class="pg next" href="{next_t["id"]}.html" style="--c:{col(next_t)}"><small>Next line</small>{e(next_t["name"])}</a>' if next_t else ""])
    body = f'''<header class="line-head" style="--c:{col(t)}">
  <div class="wrap">
    <p class="bullet" aria-hidden="true">{e(t["bullet"])}</p>
    <h1>{e(t["name"])} <span class="sr-only">line</span></h1>
    <p class="lede">{e(t["summary"])}</p>
    <p class="meta">{len(t["stages"])} stations · {sum(len(s["topics"]) for s in t["stages"])} tools and topics · {start}</p>
  </div>
</header>
<div class="wrap">
  <ol class="route" style="--c:{col(t)}">{stations}</ol>
  <nav class="pager" aria-label="Other lines">{pager}</nav>
</div>'''
    return page(f'{t["name"]} · Coding Roadmap', f'{t["name"]}: {t["summary"]} {len(t["stages"])} stages, each with official documentation links.', body, t["id"])


def main():
    SITE.mkdir(exist_ok=True)
    written = []
    for i, t in enumerate(TRACKS):
        (SITE / f'{t["id"]}.html').write_text(line_page(t, i), encoding="utf-8", newline="\n")
        written.append(f'{t["id"]}.html')
    cards = "".join(
        f'''<li class="line-card" style="--c:{col(t)}"><a href="{t["id"]}.html"><span class="bullet sm" aria-hidden="true">{e(t["bullet"])}</span>
  <span class="lc-name">{e(t["name"])}</span><span class="lc-sum">{e(t["summary"])}</span><span class="lc-meta">{len(t["stages"])} stations</span></a></li>'''
        for t in TRACKS)
    n_topics = sum(len(s["topics"]) for t in TRACKS for s in t["stages"])
    home = f'''<header class="hero wrap">
  <h1>Coding Roadmap</h1>
  <p class="lede">{e(DATA["summary"])}</p>
</header>
<section class="map-wrap" aria-label="The network">
  <div class="map-pad"><div class="map-scroll" tabindex="0" aria-label="Transit map, scrolls sideways on small screens">{network_svg()}</div><p class="swipe" aria-hidden="true">Swipe sideways to see the whole map</p></div>
</section>
<script>/* on narrow screens, open the map at the interchange rather than on empty track */
(function () {{ var m = document.querySelector(".map-scroll"), h = m.querySelector(".hub"), s = m.querySelector(".net");
  if (m.scrollWidth > m.clientWidth) m.scrollLeft = (h.getBBox().x / s.viewBox.baseVal.width) * s.clientWidth - 60; }})();</script>
<section class="wrap lines" aria-labelledby="lines-h">
  <h2 id="lines-h">The lines</h2>
  <ul class="line-cards">{cards}</ul>
  <p class="foot-note">{len(TRACKS)} lines, {sum(len(t["stages"]) for t in TRACKS)} stations, {n_topics} tools and topics, each linked to its official documentation.</p>
</section>'''
    (SITE / "index.html").write_text(page("Coding Roadmap · Full-stack development as a transit map", DATA["summary"], home), encoding="utf-8", newline="\n")
    original = (ROOT / "docs" / "original-roadmap.txt").read_text(encoding="utf-8")
    about = f'''<header class="hero wrap small"><h1>About this map</h1>
  <p class="lede">The roadmap began as an ASCII diagram. This site draws the same routes as a transit map, with each tool linked to its own documentation.</p></header>
<div class="wrap about">
  <section><h2>How to read it</h2><ul class="plain">
    <li>Everyone starts on <a href="{TRUNK["id"]}.html">{e(TRUNK["name"])}</a>.</li>
    <li>At its end you can change to any other line. Lines are directions to specialise in, not a fixed order: most people ride more than one.</li>
    <li>Stations are in a sensible order within each line, but you don't have to finish one before visiting the next.</li></ul></section>
  <section><h2>The original</h2><p>The diagram this site is built from, exactly as it was first written (kept in <code>docs/original-roadmap.txt</code>).</p>
  <div class="ascii" tabindex="0" aria-label="Original ASCII roadmap, scrolls sideways"><pre>{e(original)}</pre></div>
  <p>Changes from the original: "Angular.js" is now <a href="https://angular.dev/" rel="noopener">Angular</a> (AngularJS is its retired predecessor), "(Most Popular)" was removed from React because the diagram gave no source for it, and tools that appeared in more than one box are listed where you'd first use them.</p></section>
  <section><h2>Contributing</h2><p>Every line, station and link lives in <code>_src/data/roadmap.json</code>. Edit it, run <code>python _src/build.py</code>, and open a pull request on <a href="https://github.com/SolutionsAsService/CodingRoadmap" rel="noopener">GitHub</a>.</p></section>
</div>'''
    (SITE / "about.html").write_text(page("About · Coding Roadmap", "How to read the Coding Roadmap transit map, the original ASCII roadmap, and how to contribute.", about, "about"), encoding="utf-8", newline="\n")
    nf = '<header class="hero wrap small"><h1>Wrong platform.</h1><p class="lede">That page isn\'t on this map.</p><p><a class="btn" href="index.html">Back to the map</a></p></header>'
    (SITE / "404.html").write_text(page("Not found · Coding Roadmap", "That page isn't on this map.", nf), encoding="utf-8", newline="\n")
    written += ["index.html", "about.html", "404.html"]
    dead = [f"{w}: {r}" for w in written for r in re.findall(r'(?:href|src)="([^"#?]+)', (SITE / w).read_text(encoding="utf-8"))
            if not re.match(r"[a-z]+:|//", r) and not (SITE / r).is_file()]
    assert not dead, dead
    print(f"built {len(written)} pages")


if __name__ == "__main__":
    main()
