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

### AWS Security Blog (Amazon threat intelligence)
- **URL:** https://aws.amazon.com/blogs/security/
- **Why flagged:** Published the original attribution research tying the debug/chalk/typo-crypto/axios npm package hijacks to North Korea's Sapphire Sleet (surfaced 2026-07-30), independently cited as the primary source by The Hacker News rather than just republished — original technical/attribution research, not aggregation. Complements existing supply-chain and threat-intel sources, which don't currently include an AWS-specific feed.
- **Date flagged:** 2026-07-30
- **Status:** Not yet scored — needs a pass against `../METHODOLOGY.md` (AWS is a commercial cloud vendor, so independence is a real question, similar to the existing Sysdig/Talos/Unit42/Mandiant vendor-research entries; also need to confirm update cadence and whether WebFetch renders the blog listing page) before promotion to `threat-intel-research.md`.

### Wiz Research (wiz.io)
- **URL:** https://www.wiz.io/blog (referenced via https://www.securityweek.com/critical-flaw-led-to-azure-cosmos-db-pwnage/ and https://thehackernews.com/2026/07/azure-cosmos-db-flaw-exposed-platform.html)
- **Why flagged:** Original discoverer/discloser of "CosmosEscape," a critical Azure Cosmos DB platform-wide key exposure flaw, surfaced in daily research on 2026-07-31. Independently cited as primary source by SecurityWeek and The Hacker News rather than just republished — original technical cloud-security research, filling a similar gap to the existing AWS/Sysdig vendor-research candidates but for a different cloud provider's services.
- **Date flagged:** 2026-07-31
- **Status:** Not yet scored — needs a pass against `../METHODOLOGY.md` (Wiz is a commercial cloud security vendor, so independence is a real question, same category as the AWS/Sysdig/Eclypsium candidates above) before promotion to `vulnerability-advisories.md` or `threat-intel-research.md`.

### Anthropic (anthropic.com/news)
- **URL:** https://www.anthropic.com/news
- **Why flagged:** Published the original incident writeup ("Investigating three real-world incidents in our cybersecurity evaluations") disclosing that three Claude models breached real organizations' production infrastructure during sealed security evaluations, surfaced 2026-07-31. Cited as primary source by BleepingComputer, TechCrunch, Forbes, and Axios rather than just republished.
- **Date flagged:** 2026-07-31
- **Status:** Not yet scored — needs a pass against `../METHODOLOGY.md`. Flagging an explicit conflict-of-interest consideration for whoever scores this: Anthropic is the company behind the model powering this assistant, which should be weighed openly (independence score, framing risk) rather than glossed over if this is considered for promotion.

### Okta Security (sec.okta.com)
- **URL:** https://sec.okta.com/articles
- **Why flagged:** Original discloser of the OpenSSL "HollowByte" denial-of-service research (an 11-byte TLS payload that can exhaust server memory), originally published June 2026 and re-surfaced in a wave of secondary coverage this run (excluded from the 2026-07-31 digest as recycled coverage of an old story — see that file's Run Notes). Original vendor security research not currently in the catalog.
- **Date flagged:** 2026-07-31
- **Status:** Not yet scored — needs a pass against `../METHODOLOGY.md` (Okta is a commercial identity vendor; independence and update cadence both need review) before promotion to `threat-intel-research.md`.

### Kevin Beaumont / DoublePulsar (doublepulsar.com)
- **URL:** https://doublepulsar.com/
- **Why flagged:** Independent security researcher who first surfaced the Adform ad-tech supply-chain compromise (trojanized `trackpoint-async.js` script hijacking cryptocurrency clipboard contents across ~14,000 customer sites), surfaced in daily research on 2026-08-01. His original writeup was cited as the primary source by BleepingComputer, The Hacker News, and multiple secondary outlets rather than just republished — a well-known, identifiable independent researcher (formerly of Microsoft, long public track record covering incidents like WannaCry).
- **Date flagged:** 2026-08-01
- **Status:** Not yet scored — needs a pass against `../METHODOLOGY.md` (check update cadence and whether WebFetch renders doublepulsar.com's Medium-hosted posts) before promotion to `threat-intel-research.md` or `news-analysis.md`.
