# Security News Framework

A framework for tracking, scoring, and summarizing cybersecurity information on a daily basis — vulnerability advisories, security news, threat intelligence research, and open source security projects.

## Structure

```
security-news/
├── README.md                    — this file
├── METHODOLOGY.md                — how sources are scored (read this first)
├── PROCESS.md                    — how the daily digest actually gets built
├── sources/
│   ├── catalog.md                — master index of every tracked source, sorted by score
│   ├── vulnerability-advisories.md
│   ├── news-analysis.md
│   ├── threat-intel-research.md
│   ├── open-source-projects.md
│   └── candidates.md             — sources discovered but not yet scored/promoted
└── daily/
    ├── TEMPLATE.md                — template for new daily digests
    └── YYYY-MM-DD.md              — one file per day
```

## How it works

1. **Sources are catalogued and scored.** Every source in `sources/` is rated on five criteria (reliability, timeliness, signal-to-noise, technical depth, independence) per `METHODOLOGY.md`, producing an overall score and a tier (1 = essential, 2 = valuable, 3 = supplementary). `sources/catalog.md` is the master index; the category files hold full rationale for every score.

2. **The daily digest is built by following `PROCESS.md`.** Each run fetches the current content of every Tier 1/2 source, filters to what's new since the last run, extracts factual details (dates, CVE IDs, direct links), and writes a categorized digest to `daily/YYYY-MM-DD.md`. Every claim in a digest links back to the specific page it came from — nothing is included without a traceable source.

3. **New sources get discovered, not just monitored.** When research turns up a credible source not yet in the catalog, it's logged in `sources/candidates.md` and scored against the same rubric before being promoted — the source list is expected to grow over time, not stay fixed.

4. **This runs on a schedule.** A recurring scheduled task triggers the daily process each morning; see the task list in this workspace (or ask to check/update it) for the current schedule.

## Where to start

- Want to see the current state of security news? Open the most recent file in `daily/`.
- Want to know why a source is or isn't trusted? Check its entry in the relevant `sources/*.md` file.
- Want to add a source? Score it against `METHODOLOGY.md`, add it to the right category file, then update `sources/catalog.md`.
- Want to change how the daily digest is built? Edit `PROCESS.md` — the scheduled task prompt points at this file directly, so changes take effect on the next run.
