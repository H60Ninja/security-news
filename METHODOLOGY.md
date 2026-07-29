# Source Scoring Methodology

This document defines how every entry in `sources/` is scored. It exists so that scores are reproducible and arguable — anyone (including a future session of this assistant) should be able to look at a source, apply this rubric, and land on roughly the same number.

## The five criteria

Each source is rated 1–5 on five independent criteria. A score is not a vibe; it should be justified in one sentence in the source's catalog entry.

**Reliability** — Track record of factual accuracy. Does the source issue corrections when wrong? Has it been caught fabricating or badly misattributing claims? Vendor blogs lose points here only if they've historically overstated severity for marketing purposes; independent researchers with a long public track record score highest.

**Timeliness** — How quickly the source publishes relative to when something becomes known (disclosure, patch release, active exploitation). A source that reliably breaks or reports news same-day scores 5; a source with multi-day lag (e.g., NVD's historical CVE enrichment backlog) scores lower even if it's otherwise excellent.

**Signal-to-noise** — Proportion of substantive security content versus filler, advertising, syndicated reposts, or clickbait. A tight, low-volume feed where every post matters scores higher than a high-volume aggregator that reposts the same story ten times.

**Technical depth** — Does the source provide actionable detail: CVE IDs, CVSS scores, IOCs, TTPs (ATT&CK mapping), affected version ranges, PoC/exploit code? Or is it surface-level "there was a hack" reporting? Both have value, but depth is scored separately from reliability so a well-written summary source isn't penalized for being a summary source.

**Independence** — Editorial independence and transparency about conflicts of interest. Government/standards bodies and independent researchers score highest. Vendor blogs (Microsoft, Cisco Talos, Mandiant, Unit 42) are still valuable and often best-in-class technically, but they score a notch lower here because they have an incentive to frame findings favorably toward their own products.

## Overall score and tiers

Overall score = simple average of the five criteria, rounded to one decimal.

| Tier | Score range | Meaning | Cadence in daily digest |
|---|---|---|---|
| **Tier 1 — Essential** | 4.0–5.0 | Authoritative or best-in-class; a material security event will almost always surface here first or most accurately | Checked every run, always represented |
| **Tier 2 — Valuable** | 3.0–3.9 | Solid, worth regular monitoring, but has a real gap (noise, lag, or narrower scope) | Checked every run, included when it has new material |
| **Tier 3 — Supplementary** | 2.0–2.9 | Useful for specific topics or corroboration, not a primary feed | Checked periodically or spot-checked by topic |
| Not tracked | below 2.0 | Not currently worth the review overhead | Not polled |

## Source metadata (recorded per entry)

Beyond the five scores, every catalog entry records:

- **Type** — primary reporting, vendor/threat-intel research, government/standards authority, or aggregator
- **Update cadence** — real-time, daily, weekly, or irregular
- **Fetch method** — how the daily process actually retrieves content (see `PROCESS.md`), since some official feeds have been retired (CISA killed its RSS feeds in May 2025) and some endpoints are JS-rendered and require search rather than direct fetch
- **Rationale** — one to two sentences justifying the scores, so a disagreement can be resolved by re-reading the rationale rather than re-litigating the number

## Review cadence

Scores are not permanent. Re-review a source's score when: it changes ownership/editorial staff, it has a public accuracy failure, its fetch method breaks (e.g., a feed is retired) and needs a new rationale, or six months have passed since the last review. Each catalog entry has a "Last reviewed" date.

## Discovering new sources

Part of this framework's job is to widen the net over time, not just monitor a fixed list. Any time the daily research process encounters a source that isn't yet in the catalog and looks credible (cited by multiple Tier 1/2 sources, publishes original technical content, has identifiable authorship/ownership), it gets logged in `sources/candidates.md` with a one-line reason it was flagged. Candidates are scored using this same rubric before being promoted into a category file — nothing gets added to the daily rotation without going through the rubric first.
