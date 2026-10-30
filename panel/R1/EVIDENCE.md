# R1 evidence: CodingRoadmap transit-map redesign

Site: `H:/UBM/_cr/site` (8 pages: index, fundamentals, frontend, backend, devops, ml, about, 404).
Screenshots: `H:/UBM/_cr/panel/shots/<page>-<1440|390>-<light|dark>.png`. Measurements are in `panel/shots/measure.json`.

Measured after the last edit (32 runs, 8 pages x 2 widths x 2 schemes):
- Horizontal overflow: none.
- Text contrast below WCAG AA: none.
- Targets under 24 px: 'Fundamentals', 'GitHub', 'Angular'. All three are inline links inside sentences, which WCAG 2.5.8 exempts.
- Map: a label/track overlap test on the SVG returned [].

Concept: the roadmap drawn as a transit map. Fundamentals is a trunk line, and four branch lines leave it at a "Change here" hub in parallel 45-degree runs (Beck style). Each line has its own page, with a vertical route, a station per stage and topic chips linked to official docs. Nav items are line bullets. About keeps the original ASCII diagram verbatim.

Fix already applied before the panel: in dark mode the Fundamentals line was near-black on near-black. It now uses an ink variable that flips.

Inline premortem: (1) the map is unreadable on phones, so it scrolls sideways inside a focusable region, and the line cards below repeat its content as plain links; (2) the colour-only line identity is backed by a letter bullet and a text name everywhere; (3) the transit metaphor overpromises a fixed order, so About says lines are directions, not a sequence.
BREAK move: no hero image and no marketing copy. The map *is* the hero, and the whole roadmap is one glance.
