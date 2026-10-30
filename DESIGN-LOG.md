# Design log: Coding Roadmap redesign (DADA-lite, Adaptive)

The previous version is kept on the branch `legacy-2026-10-29`: a single ASCII diagram in a file called `Roadmap`.

## Brief
Turn a one-file ASCII roadmap into a site that a newcomer can read at a glance and use as a reading list. It is multi-page: one page per line, plus home, About and 404.

## Anchors
- **Harry Beck's London Underground diagram.** Topology over geography, 45-degree diagonals, parallel lines that never cross, and stations as ticks.
- **Massimo Vignelli's NYC subway signage.** Coloured line bullets with a short identifier serve as the navigation.
- **Edward Tufte's data-ink ratio.** The map is the hero. There is no illustration and no marketing copy.

## Concept
Fundamentals is the trunk. At a "Change here" hub, Frontend, Backend, DevOps and Machine learning branch off in parallel. Each stage is a station. On a line page the route runs down the left edge, and every tool is a chip linked to its official documentation. About keeps the original ASCII diagram verbatim.

## Premortem (inline)
1. **The map would be unreadable on phones.** It scrolls sideways, opens at the interchange and says so, and the line cards below repeat it as plain links.
2. **Colour alone identifies the lines.** Every line also has a numbered bullet (0–4) and a written name.
3. **The metaphor implies a fixed order.** About says the lines are directions to specialise in, not a sequence.

## BREAK move
There is no hero image: the network map is the first thing under the title, and the whole roadmap fits in one glance at 1440.

## Panel R1 (Debord, Shklovsky, Beck/Garland, Krug, Cairo)
All five critics said "ship with fixes"; the full text is in `panel/R1/panel.md`. Must-fixes and how each was resolved:

| Must-fix | Resolution |
|---|---|
| Fundamentals and Frontend both used the bullet "F" | Explicit `bullet` per line in `roadmap.json`: 0 for the trunk, then 1–4 |
| Line names were in line colours, which failed in dark mode | Names are in ink and sit above the track, just after each bend; colour stays on the track |
| Map labels rendered at about 9 px | Station names are 19 viewBox units, the map runs wider than the text column (max 1680 px), and labels measure about 15.6 px on screen at 1440 |
| The phone map showed empty track | On narrow screens the map opens scrolled to the interchange, with a sideways-swipe hint and an edge fade |

"Should" items that were also done:
- The phone nav is one scrolling row.
- Duplicate station names are renamed ("Server code", "DB operations").
- The five line cards sit in one row at 1440.

The panel converged, so there was no R2. Before the panel, the dark-mode Fundamentals line (near-black on near-black) was fixed by using an ink variable that flips with the colour scheme.

## Measured after the last edit
- **Pages:** 8 pages × 2 widths × 2 colour schemes.
- **Horizontal overflow:** none.
- **AA contrast failures:** none.
- **Map label/track/stop overlap test:** `[]`.
- **Targets under 24 px:** only three inline text links inside sentences (Fundamentals, GitHub, Angular), which WCAG 2.5.8 exempts.
- **Doc links:** checked with curl. MySQL and Adobe XD refuse automated requests but are the official URLs.

## Open items
- The map's SVG text is not covered by the automated contrast check. Line names were moved to ink partly for that reason.
- Topics with no single official page (design systems, prototyping, 2FA, SSO) are shown as dashed, unlinked chips.
