# SEA Boom Series

**Where do Southeast Asia's digital-economy booms come from, and what comes next?**

A connected series of studies on the digital economy in all 11 Southeast Asian countries. Each study builds on the one
before, uses simple, standard econometrics, and is planned in advance (pre-registered) with a review after each phase.

## The series

| # | Question | Status |
|---|---|---|
| **Q0** | What have SEA's digital-economy booms been, and when and where did each take off? | 📝 design drafted: [RESEARCH_DESIGN.md](q0_boom_catalogue/RESEARCH_DESIGN.md) |
| **Q1** | Which regions lead SEA booms: the US, China, India, other emerging markets, or none? | planned |
| **Q2** | How reliable and how fast is that lead? | planned |
| **Q3** | What is likely to boom next, and what is fading? | planned |
| **Q4** | What would change the forecast? | planned |
| **Q5** | Tracking and scoring the forecasts | planned |

## Q0 status

| Phase | Status |
|---|---|
| P0 · Literature and data audit | ⏳ next |
| P1 · Pre-registration | — |
| P2 · Panel | — |
| P3 · Blind coding check | — |
| P4 · Catalogue and tests | — |
| P5 · Write-up | — |

## Layout

```
series/                 shared code (config, data fetchers, boom rules), added in Q0-P0
q0_boom_catalogue/      design, pre-registration, notebooks, reports
data/public/            public data (raw downloads are re-fetchable and not committed)
data/licensed/          UCL-licensed extracts (Euromonitor Passport, Orbis): git-ignored, never shared
```

## Run

```bash
pip install -r requirements.txt
git config core.hooksPath .githooks         # blocks accidental commits of licensed data
./build_notebooks.sh q0_boom_catalogue      # rebuild and execute Q0's notebooks
```

## Data and licences

Public sources: IMF Financial Access Survey, World Bank, e-Conomy SEA reports. Euromonitor Passport and Orbis are
used under a UCL licence. Their data are not included in this repository, and notebooks that use them are published
without outputs.
