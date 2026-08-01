# Category: News & Analysis Sites

General-interest security journalism — breaches, incidents, investigations, industry news. Scored per `../METHODOLOGY.md`. Last reviewed: 2026-07-28.

---

### KrebsOnSecurity
- **URL:** https://krebsonsecurity.com/ · Feed: https://krebsonsecurity.com/feed/
- **Type:** Independent investigative journalism
- **Update cadence:** Several posts per week, irregular
- **Fetch method:** WebFetch the homepage (confirmed working — returns full post text with dates and permalinks)
- **Scores:** Reliability 5 / Timeliness 4 / Signal-to-noise 5 / Technical depth 4 / Independence 5 → **Overall 4.6 — Tier 1**
- **Rationale:** Brian Krebs has broken major stories (source of many original breach disclosures) with a long, well-corrected track record. Lower volume than aggregators but almost everything published is substantive. The highest-rated source in this catalog.

### BleepingComputer
- **URL:** https://www.bleepingcomputer.com/ · Feed: https://www.bleepingcomputer.com/feed/ (feed has returned HTTP 403 for some fetchers — prefer WebFetch on the site directly)
- **Type:** News aggregator with original reporting
- **Update cadence:** Multiple posts daily
- **Fetch method:** WebFetch the homepage/news listing
- **Scores:** Reliability 4 / Timeliness 5 / Signal-to-noise 4 / Technical depth 3 / Independence 4 → **Overall 4.0 — Tier 1**
- **Rationale:** Fast, high-volume, generally accurate reporting on breaches, ransomware, and malware; often first to cover ransomware gang activity and forum leaks. Depth is moderate — good summaries, not deep technical dives.

### The Hacker News
- **URL:** https://thehackernews.com/ · Feed: http://feeds.feedburner.com/TheHackersNews
- **Type:** News aggregator
- **Update cadence:** Multiple posts daily
- **Fetch method:** WebFetch the homepage
- **Scores:** Reliability 4 / Timeliness 5 / Signal-to-noise 3 / Technical depth 3 / Independence 3 → **Overall 3.6 — Tier 2**
- **Rationale:** Extremely fast and high-volume, useful as a broad radar, but higher noise (heavy syndication, some sponsored-content blending) and shallower analysis than Krebs or BleepingComputer.

### Dark Reading
- **URL:** https://www.darkreading.com/ · Feed: https://www.darkreading.com/rss.xml
- **Type:** Trade press / industry analysis
- **Update cadence:** Multiple posts daily
- **Fetch method:** WebSearch scoped to `darkreading.com` — **the site returns `HTTP 403 Forbidden` to WebFetch** as of 2026-07-31, on both the homepage and article URLs. This is a per-site block, not an environment problem (see `../PROCESS.md` step 2). Because search summaries can't supply a publish date off the page itself, items from this source need the dedicated date-targeted query described in `../PROCESS.md` step 4 before inclusion.
- **Scores:** Reliability 4 / Timeliness 3 / Signal-to-noise 4 / Technical depth 4 / Independence 4 → **Overall 3.8 — Tier 2**
- **Rationale:** Stronger on analysis and enterprise-security context than breaking news speed; good corroborating source for why an event matters, not usually first to report it.

### SANS Internet Storm Center (ISC) Handler's Diary
- **URL:** https://isc.sans.edu/ · Full-text feed: https://isc.sans.edu/rssfeed_full.xml
- **Type:** Independent/practitioner (volunteer handlers, SANS-affiliated)
- **Update cadence:** Daily
- **Fetch method:** WebFetch the diary listing page
- **Scores:** Reliability 5 / Timeliness 4 / Signal-to-noise 4 / Technical depth 4 / Independence 5 → **Overall 4.4 — Tier 1**
- **Rationale:** Practitioner-written daily diary with a strong reputation for hands-on technical accuracy (scanning trends, live analysis of new threats); low commercial bias.

### Daily DefSec Brief (podcast/YouTube)
- **URL:** Official page: https://defsecbrief.riverside.com/ (JS-rendered — confirms legitimacy/subscribe links but has no fetchable episode content) · YouTube channel: https://www.youtube.com/@DefensivePodcasts · Parent site: https://defensivesecurity.org/ (see separate "Defensive Security Podcast" entry below — same host, confirms this is a real, established person's project, not an anonymous channel)
- **Type:** Independent daily audio/video briefing
- **Update cadence:** Daily (with occasional gaps — not every calendar day)
- **Fetch method:** WebFetch the episode listing at https://rephonic.com/podcasts/daily-defsec-brief — it mirrors each episode's show notes as plain HTML, which list the day's topics with direct links to the underlying primary source for each item (CISA, BleepingComputer, The Hacker News, Risky Business News, etc.). This is a third-party mirror, used only because the official page (`defsecbrief.riverside.com`) is a JS-rendered app that returns no episode content through WebFetch. **Do not** try to fetch the show's own RSS/XML feed or a YouTube watch page directly — both were tested and returned unusable content (binary/empty — the same JS-rendering and XML-parsing limits documented in `PROCESS.md`). If rephonic hasn't indexed the newest episode yet, fall back to WebSearch for `"Daily DefSec Brief" cyber security news [date]`.
- **Scores:** Reliability 4 / Timeliness 4 / Signal-to-noise 5 / Technical depth 3 / Independence 4 → **Overall 4.0 — Tier 1**
- **Rationale:** Hosted by Jerry Bell, confirmed via `defensivesecurity.org` as the same person behind the 12-year-running Defensive Security Podcast (see below) — this is an established, identifiable host's side project, not an anonymous new channel. Every item in the (3–5 minute) daily briefing cites its primary source directly in the show notes, which makes it easy to verify and means it functions as a curated pointer/index to same-day coverage rather than a standalone claim. Very tight signal-to-noise. Docked on technical depth (headline-and-link format, not original analysis) and reliability is a provisional 4 rather than 5 because, as of 2026-07-28, the show itself is brand new (~17 episodes, launched roughly three weeks prior) with no long independent track record of its own yet — **flag for early re-review around 2026-10-28** (about three months) rather than waiting for the standard six-month cycle, to confirm consistency holds up.

### Defensive Security Podcast
- **URL:** https://defensivesecurity.org/ · RSS: https://defensivesecurity.org/feed/podcast/
- **Type:** Independent weekly audio briefing with commentary
- **Update cadence:** Weekly
- **Fetch method:** WebFetch the homepage directly — confirmed working well. It renders full plain-text episode posts including the episode number, publish date, and a dated list of that week's story links (BleepingComputer, The Hacker News, Dark Reading, Krebs, SecurityWeek, The Register, and others), no JS-rendering issues encountered.
- **Scores:** Reliability 5 / Timeliness 3 / Signal-to-noise 5 / Technical depth 3 / Independence 5 → **Overall 4.2 — Tier 1**
- **Rationale:** Co-hosted by Jerry Bell and Andrew Kalat since 2014 (354 episodes as of 2026-07-28) — one of the longer-running independent security podcasts, listener-supported (Patreon) rather than vendor-backed. Each episode's story list is a clean, dated, well-curated set of links, easy to verify and cross-reference. Timeliness is capped at 3 because it's weekly, so items are up to a week old by the time they're covered — this is a good corroborating/context source, not a same-day feed. Technical depth reflects the text show notes specifically (a link list); the audio commentary likely adds more analysis than this framework captures, since the daily process is text-only (see `PROCESS.md`).
