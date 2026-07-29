# Category: Open Source Security Projects

Projects, foundations, and databases tracking open source software security specifically — dependency vulnerabilities, supply-chain tooling, and OSS security governance. Scored per `../METHODOLOGY.md`. Last reviewed: 2026-07-28.

---

### OSV.dev
See full entry in `vulnerability-advisories.md` (cross-listed — it's both a vuln database and the primary open source dependency vulnerability tracker). **Overall 4.2 — Tier 1**

### GitHub Security Lab
- **URL:** https://github.blog/tag/github-security-lab/ · Feed: https://github.blog/security/feed/
- **Type:** Vendor/platform research
- **Update cadence:** Weekly to biweekly
- **Fetch method:** WebFetch the blog listing page
- **Scores:** Reliability 5 / Timeliness 3 / Signal-to-noise 4 / Technical depth 4 / Independence 4 → **Overall 4.0 — Tier 1**
- **Rationale:** Original vulnerability research in widely-used open source projects, plus CodeQL-based findings; GitHub's platform position gives it visibility into supply-chain issues (malicious packages, compromised maintainer accounts) other sources miss.

### OpenSSF (Open Source Security Foundation) Blog
- **URL:** https://openssf.org/blog/
- **Type:** Standards/foundation
- **Update cadence:** Weekly
- **Fetch method:** WebFetch the blog listing page
- **Scores:** Reliability 5 / Timeliness 3 / Signal-to-noise 4 / Technical depth 3 / Independence 4 → **Overall 3.8 — Tier 2**
- **Rationale:** Best source for OSS security governance/tooling news (Scorecard, SLSA, sigstore) rather than individual vulnerability disclosures; more strategic than tactical.

### GHSA / GitHub Advisory Database
- **URL:** https://github.com/advisories
- **Type:** Aggregator (platform-hosted)
- **Update cadence:** Continuous
- **Fetch method:** WebFetch/search by ecosystem or package name; feeds into OSV.dev as an upstream source
- **Scores:** Reliability 4 / Timeliness 4 / Signal-to-noise 4 / Technical depth 3 / Independence 3 → **Overall 3.6 — Tier 2**
- **Rationale:** High coverage of package-level advisories across ecosystems GitHub hosts, but overlaps heavily with OSV.dev — kept as Tier 2 to avoid double-counting the same disclosures as a Tier 1 duplicate.

### Community KEV mirrors (e.g., `cisagov/kev-data`, `CryptoGenNepal/CVE-KEV-RSS`)
- **URL:** https://github.com/cisagov/kev-data
- **Type:** Community mirror
- **Update cadence:** Daily sync of upstream CISA KEV data
- **Fetch method:** WebFetch/GitHub raw file
- **Scores:** Reliability 4 / Timeliness 4 / Signal-to-noise 3 / Technical depth 3 / Independence 3 → **Overall 3.4 — Tier 2**
- **Rationale:** Useful fallback now that CISA's own RSS feed is retired, but it's a mirror of a primary source, not original reporting — only consulted if the official KEV page/JSON is unreachable.

---

## Candidate discovery

New open source security projects worth evaluating surface constantly (package-manager-specific scanners, new OpenSSF working groups, ecosystem-specific advisory databases like RustSec or PyPA Advisory DB). Any such project encountered during daily research that isn't yet catalogued here should be logged in `candidates.md`, not silently skipped.
