# Daily Research Process

How the daily digest actually gets built. This is written so that any future run of this assistant — scheduled or manual — reproduces the same process.

## Why this isn't a standalone script

The obvious design would be a script that pulls each source's RSS feed on a cron job. That doesn't work here: this environment's shell has allowlisted network egress, and direct `curl`/`requests` calls to RSS/JSON endpoints (tested against CISA's KEV JSON, Krebs' feed, etc.) come back blocked. Fetching has to go through the assistant's own `WebFetch`/`WebSearch` tools instead of raw HTTP calls — and testing showed those tools handle HTML listing pages well (confirmed against krebsonsecurity.com, which returned full post text with dates and links) but not JSON or XML endpoints (the CISA KEV JSON URL returned empty content).

So the daily process is an agent run, not a cron script: each run, the assistant works through the catalog and fetches each source's human-readable page, not its raw feed.

## Steps

1. **Load the catalog.** Read `sources/catalog.md` for the full source list, and pull Tier 1 sources every run; pull Tier 2 sources every run as well unless they've been silent for several consecutive days (then check less frequently — use judgment, not a hard rule).

2. **Fetch each source.** Use `WebFetch` on the source's homepage/listing URL (recorded per-source in the category files under "Fetch method"). If a fetch returns empty or clearly JS-rendered content, fall back to `WebSearch` scoped to that domain (e.g., `site:cisa.gov known exploited vulnerabilities` with a recency term) rather than guessing at content.

   **Podcast/video sources are text-only in this framework.** We don't transcribe audio or watch video — we rely on written show notes/episode descriptions, which for a well-run news podcast already contain the substance (topic + link to the primary source per item). Raw podcast/YouTube RSS feeds return as unusable binary/XML through `WebFetch`, same as other XML feeds, and YouTube's own watch pages are JS-rendered and return empty — don't use either directly. Instead use whatever HTML mirror of the show notes actually renders (see Daily DefSec Brief's entry in `sources/news-analysis.md` for the current example: a third-party podcast tracker page, not the platform itself). If a source is added that has no such text mirror, note that explicitly rather than fabricating episode content from the title alone.

   **Prefer the official source over a third-party mirror whenever the official one actually renders.** Before settling on a third-party tracker/mirror as a source's fetch method, check whether the publisher's own site works through `WebFetch` — plenty of official pages are plain server-rendered HTML and work fine (e.g. `defensivesecurity.org`, a WordPress site, renders perfectly), while others are JS-rendered apps that return nothing (e.g. `defsecbrief.riverside.com`). Only fall back to a third party when the primary source genuinely doesn't render as text. When a mirror is used, say so explicitly in the source's catalog entry so it's clear the digest is one step removed from the publisher.

3. **Filter to the lookback window.** Default lookback is since the last successful daily run (roughly 24 hours; use 48–72 hours for the first run of a new week to catch anything missed over a weekend gap). Discard anything older even if it's still on the homepage.

4. **Extract per item:** title, exact publish date, direct URL (the actual article/advisory permalink, not just the homepage), source name + tier, and a 2–3 sentence factual summary written from what was actually read — never inferred or filled in from the headline alone. Pull out CVE IDs, CVSS scores, and named threat actors/malware when present, since these are what make items scannable and searchable later.

5. **Categorize** each item into one of:
   - Critical Vulnerabilities & Advisories (new CVEs, KEV additions, Patch Tuesday, actively-exploited flaws)
   - Active Threats & Incidents (breaches, ransomware, ongoing campaigns)
   - Threat Intelligence & Research (APT/malware analysis, TTP writeups)
   - Open Source & Supply Chain (OSS project vulnerabilities, dependency advisories, tooling)
   - Other Notable (anything credible that doesn't fit above but a security-focused reader would want to see)

6. **Flag high-priority items** — anything from a Tier 1 source involving: confirmed active exploitation, CVSS ≥ 9.0, a KEV catalog addition, or a major named incident (breach affecting a large population, critical infrastructure, or significant ransomware activity). These go in an "At a glance" section at the top of the digest.

7. **Write the digest** to `daily/YYYY-MM-DD.md` using `daily/TEMPLATE.md`. Every item must carry its source link — no unsourced claims. If a scheduled Tier 1 source couldn't be fetched this run, say so explicitly in the digest ("CISA advisories page unreachable this run") rather than silently omitting it.

   **Formatting rule:** keep the `**Source:** ... · **Published:** ...` metadata line to a single link and date. When an item covers multiple related dates/batches/links (e.g. several weeks of KEV additions under one heading), put the primary one in the metadata line and break the rest out as a bulleted list underneath — don't chain them together with semicolons in one line. Markdown renders a long single-line paragraph as one dense, hard-to-scan block regardless of how it's wrapped in the source file.

8. **Log new source candidates.** If research surfaces a source not in the catalog that looks credible (see `METHODOLOGY.md` → "Discovering new sources"), add one line to `sources/candidates.md` with the URL and why it was flagged. Don't score or promote it in the same run — that's a separate, deliberate step.

9. **Never fabricate.** If nothing new came from a source, say "no new items" rather than padding the digest. If a claim can't be traced to a specific fetched page, it doesn't go in the digest. This applies to URLs too: always copy a link verbatim from the page or search result you actually retrieved. Never hand-construct or shorten a URL from memory (e.g. guessing the path structure from other similar URLs seen in the same batch) — a plausible-looking URL that wasn't copied directly is exactly the kind of thing that quietly 404s.

## Scheduling

This process runs as a scheduled task (see `mcp__scheduled-tasks__create_scheduled_task`) rather than a shell cron job, since it depends on the assistant's own fetch tools. The task prompt should point at this file and `sources/catalog.md` directly so behavior stays in sync with any future edits to either.
