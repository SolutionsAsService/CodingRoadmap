# Coding Roadmap

Full-stack development drawn as a transit map. Everyone starts on the **Fundamentals** line; at its end you can change onto **Frontend**, **Backend**, **DevOps and infrastructure** or **Machine learning and AI**. Each line has its own page with its stations (stages) in order, and every tool on it links to its official documentation.

## Layout

```
_src/
  data/roadmap.json   # every line, station, note and link: edit this
  layout.html         # shared header and footer
  build.py            # writes site/ (standard-library Python, no dependencies)
site/                 # the deployable static site (committed)
  css/site.css
  favicon.svg
docs/original-roadmap.txt   # the original ASCII roadmap, kept as it was written
index.html            # redirects to site/
vercel.json           # static deploy config (root and site/)
```

## Editing the roadmap

1. Change `_src/data/roadmap.json`. Each track has an `id`, `name`, `color` and `stages`; each stage has a `name`, a one-line `note` and `topics` as `[name, url]` pairs. Leave the url empty for a topic with no single official page.
2. Rebuild:

```bash
python _src/build.py
```

The build writes one page per line plus the home map, About and 404, and stops with an error if any local link is dead. Commit the rebuilt `site/` with your change.

## Deploying

The repo deploys as a plain static site on Vercel or Shadw with no build step: `vercel.json` serves `site/` whether the project's root directory is blank or set to `site`. There is deliberately no `package.json` or framework config at the root.

## Contributing and licence

See [CONTRIBUTING.md](CONTRIBUTING.md). MIT licensed; see [LICENSE](LICENSE).
