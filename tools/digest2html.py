#!/usr/bin/env python3
"""Render a daily digest markdown file to a standalone HTML page.

Usage:
    python3 tools/digest2html.py daily/2026-07-31.md
    python3 tools/digest2html.py daily/2026-07-31.md -o /tmp/digest.html
    python3 tools/digest2html.py --latest

Design notes
------------
Standard library only, deliberately. The repo has no dependency manifest and
`PROCESS.md` explains why the *research* half of this framework can't be a
script (it depends on the assistant's own fetch tools). Rendering is a different
problem: it's a pure local transform with no network access, so a plain script
is the right shape for it.

This is not a general markdown renderer. It parses the specific structure that
`daily/TEMPLATE.md` defines, which lets the output carry meaning the markdown
can only imply — severity stripes, provenance callouts, source-tier ledgers.
Feeding it arbitrary markdown will produce something, but the structural parts
degrade to plain paragraphs.

Severity
--------
Each item gets a severity used for the left stripe and pill. It is taken from an
optional `**Severity:**` field in the item's metadata line when present:

    **Source:** ... · **Published:** ... · **Severity:** exploited

Valid values: exploited, critical, elevated, info, carried.

When the field is absent the severity is *inferred* from the item's text (KEV
mentions, CVSS values, provenance notes, and so on). The inference is a
convenience, not an authority — it reads wording, so it will occasionally
misjudge. Set the field explicitly on anything where the stripe matters.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SEVERITIES = ("exploited", "critical", "elevated", "info", "carried")

SEV_LABELS = {
    "exploited": "Exploited",
    "critical": "Critical",
    "elevated": "Elevated",
    "info": "Informational",
    "carried": "Carried over",
}

# Sections rendered as a two-column ledger rather than as item records.
LEDGER_SECTIONS = ("sources with no new items", "new source candidates")


# --------------------------------------------------------------------------
# model
# --------------------------------------------------------------------------


@dataclass
class Item:
    title: str = ""
    meta: str = ""
    severity: str = "info"
    blocks: list[tuple[str, object]] = field(default_factory=list)


@dataclass
class Section:
    heading: str = ""
    slug: str = ""
    items: list[Item] = field(default_factory=list)
    ledger: list[tuple[str, str]] = field(default_factory=list)
    blocks: list[tuple[str, object]] = field(default_factory=list)
    subsections: list[tuple[str, list]] = field(default_factory=list)

    @property
    def is_ledger(self) -> bool:
        low = self.heading.lower()
        return any(low.startswith(p) for p in LEDGER_SECTIONS)

    @property
    def count(self) -> int:
        return len(self.ledger) if self.is_ledger else len(self.items)


# --------------------------------------------------------------------------
# inline markdown
# --------------------------------------------------------------------------

# Matches only links whose label contains no brackets, so `render_links` can work
# innermost-first and handle nesting (see below).
LINK_RE = re.compile(r"\[([^\[\]]+)\]\(([^)\s]+)\)")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*", re.S)
CODE_RE = re.compile(r"`([^`]+)`")
# Case-insensitive: `infer_severity` matches against lowercased text.
CVE_RE = re.compile(r"CVE-\d{4}-\d+", re.I)

_nested_warned: set[str] = set()


def render_links(text: str) -> str:
    """Convert markdown links, resolving nested ones innermost-first.

    The digests contain genuinely nested links, e.g.

        [[CVE-2025-68686](nvd-url) (Fortinet FortiOS)](cisa-alert-url)

    which no HTML can express directly — anchors cannot nest. Both targets carry
    real information (`PROCESS.md` requires every CVE to link to NVD, and the
    outer URL is the item's evidence), so neither is dropped: the inner link
    stays inline and the outer target is hung off a trailing reference marker.
    A warning goes to stderr, since the source markdown is better off rewritten.
    """

    def one(m: re.Match) -> str:
        label, href = m.group(1), m.group(2)
        if "<a " in label:
            key = href[:80]
            if key not in _nested_warned:
                _nested_warned.add(key)
                print(
                    f"warning: nested markdown link, outer target rendered as a "
                    f"trailing reference: {href[:70]}",
                    file=sys.stderr,
                )
            return (
                f'{label} <a class="ref" href="{href}" '
                f'aria-label="source for the preceding item">↗</a>'
            )
        bare = re.sub(r"</?code>", "", label)
        cls = ' class="cve"' if CVE_RE.fullmatch(bare) else ""
        return f'<a{cls} href="{href}">{label}</a>'

    prev = None
    while prev != text:
        prev = text
        text = LINK_RE.sub(one, text)
    return text


def inline(text: str) -> str:
    """Escape, then apply the inline markdown subset the digests actually use."""
    out = html.escape(text, quote=True)
    out = CODE_RE.sub(lambda m: f"<code>{m.group(1)}</code>", out)
    out = render_links(out)
    out = BOLD_RE.sub(lambda m: f"<strong>{m.group(1)}</strong>", out)
    return out


def format_meta(text: str) -> str:
    """Render a `**Key:** value · **Key:** value` strip as keyed spans."""
    parts = [p.strip() for p in text.split("·")]
    cells = []
    for part in parts:
        m = re.match(r"\*\*(.+?):\*\*\s*(.*)", part, re.S)
        if m:
            cells.append(
                f'<span class="k">{html.escape(m.group(1))}</span> '
                f'<span class="v">{inline(m.group(2))}</span>'
            )
        elif part:
            cells.append(f'<span class="v">{inline(part)}</span>')
    return '<span class="sep">│</span>'.join(cells)


def slugify(heading: str) -> str:
    s = heading.lower().replace("&", "")
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    return re.sub(r"\s+", "-", s.strip())


def short_label(heading: str) -> str:
    """Condense a section heading for the sidebar nav."""
    trims = {
        "critical vulnerabilities & advisories": "Vulnerabilities",
        "active threats & incidents": "Threats & incidents",
        "threat intelligence & research": "Threat intel",
        "open source & supply chain": "Supply chain",
        "sources with no new items this run": "No new items",
        "new source candidates logged today": "Candidates",
    }
    return trims.get(heading.lower(), heading)


# --------------------------------------------------------------------------
# severity
# --------------------------------------------------------------------------

SEV_FIELD_RE = re.compile(r"\*\*Severity:\*\*\s*([a-z]+)", re.I)
CVSS_RE = re.compile(r"CVSS[:\s*]*([0-9]+(?:\.[0-9])?)", re.I)


def strip_severity_field(meta: str) -> str:
    """Remove the `**Severity:**` cell so it isn't printed in the meta strip."""
    cells = [c.strip() for c in meta.split("·")]
    kept = [c for c in cells if not SEV_FIELD_RE.match(c)]
    return " · ".join(kept)


def infer_severity(item: Item, body: str) -> str:
    declared = SEV_FIELD_RE.search(item.meta)
    if declared:
        value = declared.group(1).lower()
        if value in SEVERITIES:
            return value
        print(
            f"warning: unknown severity {value!r} on {item.title[:50]!r}, inferring",
            file=sys.stderr,
        )

    hay = f"{item.title}\n{item.meta}\n{body}".lower()

    if "provenance note" in hay or "carried over" in hay:
        return "carried"
    # \bkev\b, not a substring: "KEV catalog" yes, "Kevin"/"kevlar" no.
    if re.search(r"\bkev\b", hay) or any(
        k in hay
        for k in ("actively exploited", "active exploitation", "zero-day", "exploited as a")
    ):
        return "exploited"
    scores = [float(s) for s in CVSS_RE.findall(hay)]
    if any(s >= 9.0 for s in scores):
        return "critical"
    if "critical" in hay:
        return "critical"
    if CVE_RE.search(hay) or "actor/malware" in hay or "**actor" in hay:
        return "elevated"
    return "info"


def severity_badge(sev: str, item: Item) -> str:
    """Prefer a concrete label (CVSS 9.8, KEV) over the generic severity word."""
    hay = f"{item.title} {item.meta}".lower()
    if sev == "exploited":
        if re.search(r"\bkev\b", hay):
            label = "KEV"
        elif "zero-day" in hay:
            label = "Zero-day"
        else:
            label = "Exploited"
    elif sev == "critical":
        scores = [float(s) for s in CVSS_RE.findall(f"{item.title} {item.meta}")]
        top = max(scores) if scores else None
        label = f"CVSS {top:g}" if top and top >= 9.0 else "Critical"
    else:
        label = SEV_LABELS[sev]
    return f'<span class="pill" data-sev="{sev}">{html.escape(label)}</span>'


# --------------------------------------------------------------------------
# parsing
# --------------------------------------------------------------------------


def parse(text: str) -> tuple[str, list[tuple[str, object]], list[Section]]:
    title = ""
    preamble: list[tuple[str, object]] = []
    sections: list[Section] = []
    current: Section | None = None
    item: Item | None = None
    sub: tuple[str, list] | None = None
    para: list[str] = []
    bullets: list[str] = []

    def sink() -> list:
        if current is None:
            # Content between the title and the first section — in real digests
            # this is the incident-mode run notice, which PROCESS.md requires
            # at the very top of the file. It must survive rendering.
            return preamble
        if sub is not None:
            return sub[1]
        if item is not None:
            return item.blocks
        return current.blocks

    def flush() -> None:
        nonlocal para, bullets
        if para:
            joined = " ".join(para).strip()
            if joined:
                kind = "provenance" if joined.lstrip().startswith("**Provenance") else "p"
                sink().append((kind, joined))
            para = []
        if bullets:
            sink().append(("ul", list(bullets)))
            bullets = []

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()
        stripped = line.strip()

        if stripped.startswith("<!--"):
            while i < len(lines) and "-->" not in lines[i]:
                i += 1
            i += 1
            continue

        if line.startswith("# "):
            flush()
            title = line[2:].strip()
            i += 1
            continue

        if line.startswith("## "):
            flush()
            item, sub = None, None
            heading = line[3:].strip()
            if heading.lower().startswith("table of contents"):
                # Skipped: the nav is regenerated from the parsed structure.
                i += 1
                while i < len(lines) and not lines[i].startswith("## "):
                    i += 1
                continue
            current = Section(heading=heading, slug=slugify(heading))
            sections.append(current)
            i += 1
            continue

        if line.startswith("### ") and current is not None:
            flush()
            heading = line[4:].strip()
            if current.heading.lower().startswith("run notes"):
                sub = (heading, [])
                current.subsections.append(sub)
                item = None
            else:
                sub = None
                item = Item(title=heading)
                current.items.append(item)
                # The metadata strip, when present, is the next non-blank line.
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines) and lines[j].lstrip().startswith("**Source:**"):
                    item.meta = lines[j].strip()
                    i = j
            i += 1
            continue

        if current is not None and current.is_ledger and stripped.startswith("- "):
            flush()
            body = stripped[2:]
            m = re.match(r"\*\*(.+?)\*\*\s*[—-]\s*(.*)", body, re.S) or re.match(
                r"(.+?)\s+[—]\s+(.*)", body, re.S
            )
            if m:
                current.ledger.append((m.group(1).strip(), m.group(2).strip()))
            else:
                current.ledger.append(("", body))
            i += 1
            continue

        if stripped.startswith("- "):
            if para:
                flush()
            bullets.append(stripped[2:])
            i += 1
            continue

        if not stripped:
            flush()
            i += 1
            continue

        if bullets:
            flush()
        para.append(stripped)
        i += 1

    flush()

    for section in sections:
        for it in section.items:
            body = " ".join(
                str(b) for kind, b in it.blocks if kind in ("p", "provenance")
            )
            it.severity = infer_severity(it, body)
            it.meta = strip_severity_field(it.meta)

    return title, preamble, sections


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------


def render_blocks(blocks: list[tuple[str, object]]) -> str:
    out = []
    for kind, payload in blocks:
        if kind == "p":
            out.append(f"<p>{inline(str(payload))}</p>")
        elif kind == "provenance":
            out.append(f'<p class="provenance">{inline(str(payload))}</p>')
        elif kind == "ul":
            lis = "".join(f"<li>{inline(b)}</li>" for b in payload)  # type: ignore[union-attr]
            out.append(f"<ul>{lis}</ul>")
    return "\n".join(out)


def render_item(item: Item) -> str:
    parts = [f'<article class="item" data-sev="{item.severity}">']
    badge = severity_badge(item.severity, item) if item.severity != "info" else ""
    parts.append(f"<h3>{inline(item.title)} {badge}</h3>")
    if item.meta:
        parts.append(f'<p class="meta">{format_meta(item.meta)}</p>')
    parts.append(render_blocks(item.blocks))
    parts.append("</article>")
    return "\n".join(p for p in parts if p)


def render_section(section: Section) -> str:
    noun = "sources" if section.is_ledger else "items"
    count = f'<span class="cat-count">{section.count} {noun}</span>' if section.count else ""
    head = (
        f'<div class="cat-head"><h2>{inline(section.heading)}</h2>{count}</div>'
    )
    body = [render_blocks(section.blocks)]

    if section.is_ledger:
        rows = "".join(
            f'<li><span class="who">{inline(who)}</span><span>{inline(what)}</span></li>'
            for who, what in section.ledger
        )
        body.append(f'<ul class="ledger">{rows}</ul>')
    else:
        body.extend(render_item(it) for it in section.items)

    for heading, blocks in section.subsections:
        body.append(f"<h3>{inline(heading)}</h3>")
        body.append(render_blocks(blocks))

    cls = "cat notes" if section.heading.lower().startswith("run notes") else "cat"
    inner = "\n".join(b for b in body if b)
    if cls.endswith("notes"):
        inner = f'<div class="notes-inner">{inner}</div>'
    return f'<section class="{cls}" id="{section.slug}">\n{head}\n{inner}\n</section>'


def render_nav(sections: list[Section]) -> str:
    rows = []
    for s in sections:
        n = s.count or "—"
        rows.append(
            f'<li><a href="#{s.slug}">{html.escape(short_label(s.heading))}'
            f'<span class="n">{n}</span></a></li>'
        )
    return (
        '<nav class="rail" aria-label="Sections"><p class="rail-title">Contents</p>'
        f'<ol>{"".join(rows)}</ol></nav>'
    )


CSS = """
:root{--ground:#F7F8FA;--sunk:#EFF1F5;--panel:#FFF;--ink:#171B24;--soft:#4A5361;
--faint:#737D8C;--rule:#DFE3EA;--rule2:#E9ECF1;--accent:#1B5A66;--accent2:#E4EEF0;
--exploited:#B3302A;--critical:#C0741A;--elevated:#8A6A2F;--info:#5B6577;--carried:#6B5B8A;
--serif:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
--mono:ui-monospace,"SF Mono",SFMono-Regular,Menlo,Consolas,monospace}
@media(prefers-color-scheme:dark){:root{--ground:#10131A;--sunk:#0B0E14;--panel:#171B24;
--ink:#E4E7EE;--soft:#A8B0BE;--faint:#7A8494;--rule:#262C38;--rule2:#1E242E;
--accent:#6FB3BF;--accent2:#173034;--exploited:#E8756C;--critical:#E3A059;
--elevated:#C4A76A;--info:#8B95A6;--carried:#A895C4}}
:root[data-theme=dark]{--ground:#10131A;--sunk:#0B0E14;--panel:#171B24;--ink:#E4E7EE;
--soft:#A8B0BE;--faint:#7A8494;--rule:#262C38;--rule2:#1E242E;--accent:#6FB3BF;
--accent2:#173034;--exploited:#E8756C;--critical:#E3A059;--elevated:#C4A76A;
--info:#8B95A6;--carried:#A895C4}
:root[data-theme=light]{--ground:#F7F8FA;--sunk:#EFF1F5;--panel:#FFF;--ink:#171B24;
--soft:#4A5361;--faint:#737D8C;--rule:#DFE3EA;--rule2:#E9ECF1;--accent:#1B5A66;
--accent2:#E4EEF0;--exploited:#B3302A;--critical:#C0741A;--elevated:#8A6A2F;
--info:#5B6577;--carried:#6B5B8A}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--sans);
font-size:16px;line-height:1.65;-webkit-font-smoothing:antialiased}
.shell{max-width:1180px;margin:0 auto;padding:0 clamp(20px,4vw,48px) 96px;
display:grid;grid-template-columns:1fr;gap:0 56px}
@media(min-width:1000px){.shell{grid-template-columns:210px minmax(0,1fr)}
.masthead{grid-column:1/-1}.rail{display:block!important;grid-column:1;align-self:start;
position:sticky;top:32px;padding-top:44px}.flow{grid-column:2}}
.masthead{padding:clamp(40px,7vw,80px) 0 32px;border-bottom:2px solid var(--ink)}
.eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.16em;
text-transform:uppercase;color:var(--accent);margin:0 0 18px}
.masthead h1{font-family:var(--serif);font-size:clamp(2.6rem,7vw,4.4rem);line-height:1.02;
font-weight:400;letter-spacing:-.015em;margin:0;text-wrap:balance}
.masthead h1 .date{font-family:var(--mono);font-size:clamp(1.5rem,4vw,2.4rem);display:block;
color:var(--soft);margin-top:8px;font-variant-numeric:tabular-nums}
.runbar{margin-top:28px;display:flex;flex-wrap:wrap;gap:10px 28px;font-family:var(--mono);
font-size:11.5px;color:var(--faint)}
.runbar b{color:var(--ink);font-weight:600;font-variant-numeric:tabular-nums}
.rail{display:none}
.rail-title{font-family:var(--mono);font-size:10px;letter-spacing:.16em;
text-transform:uppercase;color:var(--faint);margin:0 0 14px}
.rail ol{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:2px}
.rail a{display:flex;justify-content:space-between;align-items:baseline;gap:8px;padding:5px 0;
font-size:13px;line-height:1.35;color:var(--soft);text-decoration:none;
border-bottom:1px solid var(--rule2)}
.rail a:hover,.rail a:focus-visible{color:var(--accent)}
.rail .n{font-family:var(--mono);font-size:10.5px;color:var(--faint);
font-variant-numeric:tabular-nums}
.flow{grid-column:1;min-width:0}
.preamble{margin:44px 0 0;max-width:68ch;font-size:15px;color:var(--soft)}
.preamble p{margin:0 0 12px}
.preamble p:last-child{margin:0}
.preamble strong{color:var(--ink)}
.preamble.notice{max-width:none;background:var(--panel);border:1px solid var(--rule);
border-left:3px solid var(--exploited);padding:16px 20px;font-size:14.5px;line-height:1.6}
section.cat{margin-top:72px}
.cat-head{display:flex;align-items:baseline;gap:14px;padding-bottom:12px;
border-bottom:1px solid var(--ink)}
.cat-head h2{font-family:var(--serif);font-size:clamp(1.5rem,3.2vw,2rem);font-weight:400;
letter-spacing:-.015em;margin:0;text-wrap:balance;flex:1}
.cat-count{font-family:var(--mono);font-size:11px;color:var(--faint);letter-spacing:.08em;
font-variant-numeric:tabular-nums;white-space:nowrap}
article.item{padding:30px 0 30px 20px;border-left:3px solid var(--info);
border-bottom:1px solid var(--rule2)}
article.item[data-sev=exploited]{border-left-color:var(--exploited)}
article.item[data-sev=critical]{border-left-color:var(--critical)}
article.item[data-sev=elevated]{border-left-color:var(--elevated)}
article.item[data-sev=carried]{border-left-color:var(--carried)}
article.item[data-sev=info]{border-left-color:var(--rule)}
article.item:last-child{border-bottom:0}
article.item h3{font-family:var(--serif);font-size:1.28rem;line-height:1.28;font-weight:600;
letter-spacing:-.008em;margin:0 0 12px;text-wrap:balance;display:flex;flex-wrap:wrap;
align-items:baseline;gap:10px}
.pill{display:inline-block;font-family:var(--mono);font-size:9.5px;letter-spacing:.11em;
text-transform:uppercase;padding:3px 7px 2px;border:1px solid currentColor;border-radius:2px;
vertical-align:2px;white-space:nowrap;color:var(--info);flex:none}
.pill[data-sev=exploited]{color:var(--exploited)}
.pill[data-sev=critical]{color:var(--critical)}
.pill[data-sev=elevated]{color:var(--elevated)}
.pill[data-sev=carried]{color:var(--carried)}
.meta{font-family:var(--mono);font-size:11.5px;line-height:1.7;color:var(--faint);
margin:0 0 14px;padding:9px 12px;background:var(--sunk);border-radius:2px;overflow-x:auto}
.meta .k{text-transform:uppercase;letter-spacing:.08em;font-size:9.5px;color:var(--faint)}
.meta .v{color:var(--ink)}
.meta .sep{color:var(--rule);padding:0 4px}
article.item>p,article.item>ul{margin:0 0 14px;max-width:68ch}
article.item>ul{padding-left:18px}
article.item>ul li{margin-bottom:8px;font-size:15px}
.provenance{max-width:68ch;margin:0 0 14px;padding:11px 14px;background:var(--accent2);
border-left:2px solid var(--carried);font-size:14px;line-height:1.55;color:var(--soft)}
.provenance strong{color:var(--ink)}
a{color:var(--accent);text-decoration:none;
border-bottom:1px solid color-mix(in srgb,var(--accent) 35%,transparent)}
a:hover,a:focus-visible{border-bottom-color:var(--accent)}
a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
code,.cve{font-family:var(--mono);font-size:.88em;font-variant-numeric:tabular-nums}
a.cve{white-space:nowrap}
a.ref{font-size:.8em;padding:0 2px;border-bottom:0;vertical-align:1px}
a.ref:hover,a.ref:focus-visible{border-bottom:0;text-decoration:underline}
.ledger{list-style:none;margin:0;padding:0;display:flex;flex-direction:column}
.ledger li{display:grid;grid-template-columns:minmax(0,1fr);gap:2px 18px;padding:13px 0;
border-bottom:1px solid var(--rule2);font-size:14.5px;line-height:1.55;color:var(--soft)}
@media(min-width:680px){.ledger li{grid-template-columns:232px minmax(0,1fr)}}
.ledger .who{font-family:var(--mono);font-size:11.5px;color:var(--ink);padding-top:3px}
section.notes .notes-inner{background:var(--panel);border:1px solid var(--rule);
padding:clamp(22px,3.5vw,34px);margin-top:26px}
section.notes h3{font-family:var(--mono);font-size:11px;letter-spacing:.14em;
text-transform:uppercase;color:var(--accent);margin:30px 0 12px}
section.notes .notes-inner>h3:first-child{margin-top:0}
section.notes p{margin:0 0 14px;max-width:68ch;font-size:14.5px;line-height:1.62;
color:var(--soft)}
section.notes p strong,section.notes li strong{color:var(--ink)}
section.notes ul{max-width:68ch;font-size:14.5px;color:var(--soft)}
.legend{display:flex;flex-wrap:wrap;gap:10px 20px;margin:30px 0 0;padding-top:22px;
border-top:1px solid var(--rule);font-family:var(--mono);font-size:10.5px;color:var(--faint);
letter-spacing:.04em}
.legend span{display:flex;align-items:center;gap:7px}
.legend i{width:18px;height:3px;display:block;background:var(--info)}
.legend span[data-sev=exploited] i{background:var(--exploited)}
.legend span[data-sev=critical] i{background:var(--critical)}
.legend span[data-sev=elevated] i{background:var(--elevated)}
.legend span[data-sev=carried] i{background:var(--carried)}
.colophon{margin-top:44px;padding-top:22px;border-top:1px solid var(--rule);
font-family:var(--mono);font-size:11px;line-height:1.7;color:var(--faint)}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

LEGEND = (
    '<div class="legend">'
    '<span data-sev="exploited"><i></i> Active exploitation / KEV</span>'
    '<span data-sev="critical"><i></i> Critical severity</span>'
    '<span data-sev="elevated"><i></i> Elevated</span>'
    '<span data-sev="info"><i></i> Informational</span>'
    '<span data-sev="carried"><i></i> Carried over, not re-verified</span>'
    "</div>"
)


def render_preamble(preamble: list[tuple[str, object]]) -> str:
    """Render pre-section content. A run notice gets warning treatment."""
    if not preamble:
        return ""
    first = str(preamble[0][1]).lstrip().lower()
    cls = "preamble notice" if first.startswith("**run notice") else "preamble"
    return f'<div class="{cls}">{render_blocks(preamble)}</div>'


def build(
    title: str,
    preamble: list[tuple[str, object]],
    sections: list[Section],
    source_name: str,
) -> str:
    date = ""
    m = re.search(r"(\d{4}-\d{2}-\d{2})", title)
    if m:
        date = m.group(1)
    label = title.replace(f"— {date}", "").strip(" —") if date else title

    tally = {s: 0 for s in SEVERITIES}
    for section in sections:
        for it in section.items:
            tally[it.severity] += 1

    chips = "".join(
        f"<span>{SEV_LABELS[s]} <b>{tally[s]}</b></span>"
        for s in ("exploited", "critical", "elevated", "info", "carried")
        if tally[s]
    )

    body = "\n".join(render_section(s) for s in sections)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{CSS}</style>
</head>
<body>
<div class="shell">
<header class="masthead">
<p class="eyebrow">Security News Framework · Daily Digest</p>
<h1>{html.escape(label)}<span class="date">{html.escape(date)}</span></h1>
<div class="runbar">{chips}</div>
</header>
{render_nav(sections)}
<main class="flow">
{render_preamble(preamble)}
{body}
{LEGEND}
<p class="colophon">
Generated from <code>{html.escape(source_name)}</code> by <code>tools/digest2html.py</code><br>
Every claim links to the page it came from. Nothing is included without a traceable source.
</p>
</main>
</div>
</body>
</html>
"""


def latest_digest(root: Path) -> Path:
    files = sorted(
        p for p in (root / "daily").glob("*.md") if re.fullmatch(r"\d{4}-\d{2}-\d{2}", p.stem)
    )
    if not files:
        sys.exit("no daily/YYYY-MM-DD.md files found")
    return files[-1]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("source", nargs="?", type=Path, help="path to a daily/YYYY-MM-DD.md file")
    ap.add_argument("-o", "--out", type=Path, help="output path (default: alongside input, .html)")
    ap.add_argument("--latest", action="store_true", help="render the newest file in daily/")
    ap.add_argument("--stdout", action="store_true", help="write to stdout instead of a file")
    args = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    if args.latest:
        src = latest_digest(root)
    elif args.source:
        src = args.source
    else:
        ap.error("give a source file or --latest")

    if not src.is_file():
        sys.exit(f"not a file: {src}")

    title, preamble, sections = parse(src.read_text(encoding="utf-8"))
    if not sections:
        sys.exit(f"no '## ' sections parsed from {src} — is this a digest file?")

    page = build(title or src.stem, preamble, sections, src.name)

    if args.stdout:
        sys.stdout.write(page)
        return

    out = args.out or src.with_suffix(".html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")

    items = sum(len(s.items) for s in sections)
    print(f"{src} → {out}  ({len(sections)} sections, {items} items)")


if __name__ == "__main__":
    main()
