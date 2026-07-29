# Scheduled Task Configuration

This documents the automation that drives the daily digest, so it can be reproduced anywhere this project folder lives — a fresh machine, a new Cowork session, or after this task is accidentally deleted.

**Why this is a separate file from `PROCESS.md`:** `PROCESS.md` defines *what* the daily job does — that part lives in this repo and travels with it. The scheduling trigger itself is registered in Cowork's own scheduled-tasks system, stored at `~/Claude/Scheduled/<taskId>/SKILL.md` on whichever machine created it — that file does *not* live in this repo and will not travel with a `git clone`. This file is the bridge: it's a versioned record of exactly how to re-register the trigger.

## Current registration

- **Task ID:** `security-news-daily-digest`
- **Schedule:** `0 7 * * *` (daily, 7:00 AM local time — Cowork applies a few minutes of jitter at dispatch)
- **Registered on:** whichever machine last ran the `create_scheduled_task` call — check `mcp__scheduled-tasks__list_scheduled_tasks` for the live state (enabled/disabled, next run time) rather than trusting this file for current status
- **Notifies on completion:** yes (default)

## Exact prompt used to register it

The task's prompt is intentionally thin — it delegates almost everything to this repo's own files (`PROCESS.md`, `sources/catalog.md`, `daily/TEMPLATE.md`) so that editing the *content* of the process never requires touching the scheduled task itself:

```
You are maintaining a cybersecurity news tracking framework in the user's connected "security-news" project folder. This is a recurring daily job — you have no memory of previous runs, so follow this prompt exactly and read the project's own files for full context before doing anything else.

Steps:

1. Read `PROCESS.md` at the root of the security-news folder — it defines exactly how this daily digest gets built (why it uses WebFetch/WebSearch instead of raw feed parsing, the categorization scheme, the high-priority flagging rules, and the "never fabricate" rule). Follow it precisely.

2. Read `sources/catalog.md` for the full list of tracked sources (each links to its category file in `sources/` which has the actual URL and fetch method for that source).

3. Determine the lookback window: find the most recent file in `daily/` (filenames are `YYYY-MM-DD.md`), and use the day after that file's date through today as the lookback window. If no prior daily file exists, use the last 3 days.

4. For each Tier 1 source (and Tier 2 sources not silent for multiple consecutive runs), use WebFetch on its listing/homepage URL (from the category file). If a fetch returns empty or clearly JS-rendered content, fall back to WebSearch scoped to that domain. Extract only items published within the lookback window.

5. For each item found, capture: title, exact publish date, direct article/advisory URL, source name + tier, a factual 2-3 sentence summary written only from what was actually read, and any CVE IDs / CVSS scores / named threat actors present.

6. Categorize items into: Critical Vulnerabilities & Advisories, Active Threats & Incidents, Threat Intelligence & Research, Open Source & Supply Chain, Other Notable. Flag high-priority items (Tier 1 source + active exploitation, CVSS >= 9.0, a KEV addition, or a major named incident) in an "At a glance" section at the top.

7. Write the digest to a new file `daily/YYYY-MM-DD.md` (today's date) using the structure in `daily/TEMPLATE.md`. Every item must carry its source link. If a Tier 1 source couldn't be fetched, say so explicitly rather than omitting it silently. If a source had no new items, say "no new items" rather than skipping it or padding the digest.

8. If you encounter a credible source not already in `sources/catalog.md` (cited by multiple existing sources, original technical content, identifiable ownership), add one line about it to `sources/candidates.md` with the URL and why it was flagged. Do not score or promote it in this run — that's a deliberate separate step, per `METHODOLOGY.md`.

9. Do not fabricate content. Every claim in the digest must trace back to a specific page you actually fetched or searched this run.

After writing the file, give a short summary (a few sentences) of the highest-priority items from today's digest — not a full recap of every item, just what matters most.
```

## How to reproduce this on a new machine/session

1. Make sure this project folder is connected/mounted in Cowork.
2. Call `mcp__scheduled-tasks__create_scheduled_task` with `taskId: "security-news-daily-digest"`, `cronExpression: "0 7 * * *"`, `description: "Daily cybersecurity news digest for the security-news project"`, and the exact prompt above.
3. Run it once manually ("Run now" in the Scheduled sidebar) to pre-approve WebFetch/WebSearch tool usage — otherwise the first unattended run may pause on a permission prompt.

## If you change the process

Edit `PROCESS.md`, not this file or the live task prompt — the prompt above just tells each run to go read `PROCESS.md`, so changes there take effect on the next scheduled run automatically. Only touch this file (and re-register the task) if you want to change *when* it runs, or the top-level delegation logic itself (e.g., which files it reads).
