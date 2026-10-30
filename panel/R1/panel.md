# R1 critic panel: CodingRoadmap transit-map redesign

Judged on: EVIDENCE.md, shots index-1440-light, index-390-light, index-1440-dark, frontend-1440-light, fundamentals-390-dark, about-1440-light, 404-390-light, plus site/css/site.css and _src/build.py.

## Guy Debord (spectacle vs. use; détournement of the transit map)
Verdict: **ship with fixes**.
The détournement works: the Beck map is lifted from the commute and repurposed as a syllabus, and there is no hero image and no slogan. The map is the content. At 390 px the détourned image becomes pure spectacle, though. A phone visitor sees a black trunk, four coloured stripes running off the right edge, a clipped "Web" label, and about 200 px of empty beige below (index-390-light). It is a picture of a map, not a usable one. The line cards below save the page, but the map still takes a full screen to show nothing.
1. `.map-scroll` / `.net` below about 600 px: either draw a vertical (stacked) variant of the network or cap the visible height and show an explicit "scroll the map sideways" cue. Don't leave an empty stage. **must**
2. "The lines" grid strands Machine learning alone on a second row at 1440 (index-1440-*). The orphan makes ML look like an afterthought, which is an accident of auto-fill, not a statement. **should**

## Viktor Shklovsky (estrangement: alive or automatic?)
Verdict: **ship with fixes**.
The form is alive where the metaphor is carried through: "Change here", "Next line", "Wrong platform." on the 404, the numbered stations hanging off a thick vertical line (frontend-1440-light, fundamentals-390-dark). The "Next line → Frontend" panel is a nice estranging touch. The device goes automatic in the line cards: they are generic SaaS feature cards with a coloured top border, and the transit language stops there.
1. `.line-card`: make it read as a line, not a card. Draw the card's top rule as a track with the station count as small stop ticks, or label the meta "4 stations · terminus UX/UI". It need not be large, but the metaphor should not switch off. **could**
Nothing else serious.

## Harry Beck / Ken Garland (transit-diagram craft)
Verdict: **ship with fixes**.
The geometry is right: the trunk is horizontal, the branches leave in parallel 45-degree runs, the line spacing is consistent and the stations are evenly spaced. The craft errors are in the lettering and the identifiers.
1. **Bullet letters collide.** Fundamentals and Frontend are both "F" (index cards, nav-adjacent bullets, line-page heroes). `build.py` derives the bullet from `t["name"][:1]` in two places. A network can never have two lines with the same route letter. Give each line an explicit `bullet` key in roadmap.json (for example Fundamentals "0" or "C" for core, Frontend "F") and use it at both call sites. **must**
2. **Station lettering is too small.** `.net .st` is 14px in viewBox units, but the SVG is scaled down, so the labels render at roughly 9 px on screen at 1440 ("Web platform", "IaC", "Data eng." in index-1440-light). "CHANGE HERE" in `.hub-name` (12px, ink-2, uppercase) is smaller still. Raise `.st` to about 18-20px and `.hub-name` to about 15px in viewBox units (or shrink the viewBox), so the on-screen size is at least 12 px. **must**
3. Shared station names appear twice without being drawn as interchanges: "Databases" on both Backend and DevOps, "Languages" on both Fundamentals and Backend. Either rename them per line (for example "Data stores" or "Server languages") or draw them as linked interchange rings. **should**

## Steve Krug (can a newcomer use it without thinking?)
Verdict: **ship with fixes**.
The nav is clear, the line pages are scannable, the chips look clickable, the 404 has one obvious button, and About answers "do I have to do these in order?". Friction points:
1. At 390 the header nav takes three rows, about 200 px, before the H1 (index-390, fundamentals-390, 404-390). Collapse `.lines-nav` on narrow screens: show the bullets only with an accessible name, or put it in a horizontal-scroll strip on a single row. **should**
2. Nothing on the home cards says "this opens the line". The card is a link (`.line-card a`) but has no arrow or "Ride the line" cue, and hover is the only signal. Add a trailing "→" or "Open line" to `.lc-meta`. **could**
3. Same as Debord #1: a phone user is not told that the map scrolls. **must** (merged)

## Alberto Cairo (is the map truthful as an information graphic?)
Verdict: **ship with fixes**.
The encoding is honest. Every line keeps the same colour across the nav, the map, the cards and its page, the colour is backed by a name, the counts (5 lines, 26 stations, 79 topics) are stated as text, and About corrects the "fixed order" implication the metaphor carries. Two truth problems are visible:
1. **Dark-mode line names fail.** In index-1440-dark the "Backend" terminus label (`.ln-name`, filled with the raw line colour via `style="fill:{col(t)}"` in build.py line 64) is dark blue on #1c1d22 and nearly invisible. Frontend red and ML magenta are weak too. This contradicts the CSS header's own rule that text never sits in a line colour. The measured contrast check evidently did not cover SVG text. Fill `.ln-name` with `var(--ink)` and keep the colour in a small bullet or roundel next to it. If the colour is kept, use per-line dark-mode tints that reach 4.5:1. **must**
2. The equal x-spacing of the branches implies that each line has the same "length" and each station the same weight. That is acceptable as a schematic (Beck's own convention), and About now says so. No fix needed.

## Consensus

### Must-fix (deduplicated)
1. **Unique line bullets.** Stop deriving the bullet from `t["name"][:1]` in `_src/build.py` (line-page hero bullet and `.line-card .bullet.sm`). Add an explicit `bullet` per line so Fundamentals and Frontend no longer both show "F".
2. **Legible map line names in dark mode.** `.net .ln-name` gets `fill: var(--ink)` instead of the inline `style="fill:{col(t)}"` (build.py about line 64). Line colour then appears only on the track and on an optional roundel beside the name, or gets dark-mode tints that pass 4.5:1. Extend the contrast measurement to SVG `<text>`.
3. **Map lettering at least 12 px on screen.** Raise `.net .st` (14px to about 19px) and `.net .hub-name` (12px to about 15px) in viewBox units, or tighten the viewBox, re-run the label/track overlap test and widen the station pitch if needed.
4. **Phone map is empty and gives no cue.** Below about 600 px, either render a vertical stacked variant of `.net` from build.py, or give `.map-scroll` a visible "Swipe to see all lines →" caption plus an edge-fade affordance and trim the empty vertical space (crop the viewBox or reduce the height for narrow screens).

Should (not blocking): compact the 390 px `.lines-nav` to one row; resolve the duplicate "Databases"/"Languages" station names; fix the orphaned ML card (for example `grid-template-columns: repeat(5, 1fr)` at ≥1200 px, or a full-width Fundamentals card above four branches).
Could: an "open line →" cue on `.lc-meta`; carry transit language into the cards.

### Convergence
The five critics converge on the same four defects (bullet collision, dark-mode SVG text, tiny map lettering, unusable phone map). The rest is preference. A second round would only re-check these four fixes, so a screenshot re-measure after the fixes is enough. **Converged; no R2 needed.**
