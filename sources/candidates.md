# Candidate Sources — Under Review

Sources spotted during daily research that aren't yet in the catalog. Each gets scored against `../METHODOLOGY.md` before promotion into a category file. Nothing here is used in the daily digest yet.

Format per entry: name, URL, why it was flagged, date flagged, status.

---

### Eclypsium InfraTrust
- **URL:** referenced via https://www.bleepingcomputer.com/news/security/new-infratrust-report-reveals-infrastructure-flaws-admins-should-patch-first/
- **Why flagged:** New infrastructure/firmware/edge-device vulnerability knowledge base plus a monthly "InfraTrust Pulse" prioritization report from Eclypsium, surfaced in daily research on 2026-07-28. Firmware/infrastructure vulnerabilities are a gap in the current catalog (existing sources skew OS/application/cloud).
- **Date flagged:** 2026-07-28
- **Status:** Not yet scored — needs its own review against `../METHODOLOGY.md` (independence is a real question, since Eclypsium is a commercial vendor selling into this exact space) before promotion to a category file.

### Risky Business News (news.risky.biz)
- **URL:** https://news.risky.biz/
- **Why flagged:** Cited repeatedly as a primary source in Daily DefSec Brief's show notes (e.g. the July 27 episode's lead item on a Fastjson RCE bug). Risky Business is a long-running, well-regarded independent security news operation (podcast + newsletter), not currently in the catalog — likely a real gap rather than noise, since it's being cited by a source we already trust.
- **Date flagged:** 2026-07-28
- **Status:** Not yet scored — needs a proper pass against `../METHODOLOGY.md` (check update cadence, fetch method, and independence/ownership) before promotion to `news-analysis.md`.

### Sysdig Threat Research Blog
- **URL:** https://www.sysdig.com/blog
- **Why flagged:** Published the original disclosure of JadePuffer, described as the first fully agentic/LLM-driven ransomware operation (surfaced 2026-07-28), and was independently cited as the primary source by BleepingComputer, Dark Reading, SecurityWeek, and The Hacker News rather than just republished — a strong signal of original technical research, not aggregation.
- **Date flagged:** 2026-07-28
- **Status:** Not yet scored — needs a pass against `../METHODOLOGY.md` (Sysdig is a commercial cloud/runtime-security vendor, so independence is a real question, similar to the existing Talos/Unit42/Mandiant vendor-research entries) before promotion to `threat-intel-research.md`.
