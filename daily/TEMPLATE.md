<!--
Template for daily/YYYY-MM-DD.md. See ../PROCESS.md for how to fill this in.
Delete this comment block when creating a real daily file.

Structure notes:
- Table of Contents goes right after the title, before "At a glance."
- Run/process metadata (lookback window, sources checked, outages, incident notes) goes in
  "Run Notes" at the very bottom, not the top — readers want the news first, the plumbing last.
- Every CVE ID must be a markdown link to https://nvd.nist.gov/vuln/detail/CVE-XXXX-XXXXX,
  every time it appears (headings, "At a glance" bullets, metadata lines, and body text).
-->

# Security Digest — YYYY-MM-DD

## Table of Contents

- [At a glance](#at-a-glance)
- [Critical Vulnerabilities & Advisories](#critical-vulnerabilities--advisories)
- [Active Threats & Incidents](#active-threats--incidents)
- [Threat Intelligence & Research](#threat-intelligence--research)
- [Open Source & Supply Chain](#open-source--supply-chain)
- [Other Notable](#other-notable)
- [Sources with no new items this run](#sources-with-no-new-items-this-run)
- [New source candidates logged today](#new-source-candidates-logged-today)
- [Run Notes](#run-notes)

<!-- Adjust the TOC to match whichever sections actually appear in a given day's file — drop entries for sections you don't use, keep it in the same order as the headings below. -->

## At a glance

- [High-priority item 1 — one line, with inline source link. Any CVE ID here must be a link, e.g. [CVE-2026-16723](https://nvd.nist.gov/vuln/detail/CVE-2026-16723)]
- [High-priority item 2]

## Critical Vulnerabilities & Advisories

### [Title]
**Source:** [Name (Tier)](URL) · **Published:** [date] · **CVE:** [[CVE-XXXX-XXXXX](https://nvd.nist.gov/vuln/detail/CVE-XXXX-XXXXX) if applicable] · **CVSS:** [if applicable] · **Severity:** [optional — see below]

[2-3 sentence factual summary]

<!--
`**Severity:**` is optional and affects only the HTML view produced by tools/digest2html.py
(it is dropped from the rendered metadata line, so it never shows up as visible text).
Values: exploited | critical | elevated | info | carried
Omit it and the renderer infers a severity from wording; set it explicitly wherever the
distinction matters. Use `carried` for an item kept from a previous version of the same
file that could not be re-verified this run.
-->

## Active Threats & Incidents

### [Title]
**Source:** [Name (Tier)](URL) · **Published:** [date]

[2-3 sentence factual summary]

## Threat Intelligence & Research

### [Title]
**Source:** [Name (Tier)](URL) · **Published:** [date] · **Actor/malware:** [if named]

[2-3 sentence factual summary]

## Open Source & Supply Chain

### [Title]
**Source:** [Name (Tier)](URL) · **Published:** [date]

[2-3 sentence factual summary]

## Other Notable

### [Title]
**Source:** [Name (Tier)](URL) · **Published:** [date]

[2-3 sentence factual summary]

## Sources with no new items this run

- [Source name (Tier)] — [why: no new items found / outside window / couldn't fetch]

## New source candidates logged today

[None / list — see sources/candidates.md]

## Run Notes

<!-- Everything mechanical about the run itself lives here, at the bottom, not the top. -->

### Lookback window and sources checked

Lookback window: [start] to [end]. Sources checked: [N of M distinct catalog sources].

### Run notice

[Only include this subsection if something went wrong — a fetch outage, a source unreachable, an incident-mode fallback to WebSearch-only, etc. State plainly what happened, what was done to compensate (e.g. wider lookback window, dedicated per-item date verification), and what a human needs to do to fix it, if anything. Omit this subsection entirely on a clean run.]
