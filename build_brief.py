"""Build the sample brief page + PDF from the workflow output.

Usage:
  .venv/bin/python build_brief.py brief_data.json
brief_data.json = {"brief": "<markdown>", "data": {section: [items...]}, "generated": "YYYY-MM-DD"}
Items carry: date, claim, detail, actor, source_title, source_url, publisher, source_date, source_type, verdict, verify_note.
Global ids: S(section_index*100 + i + 1) with section order chronology, actors, indicators, scenarios.
"""
import json, re, sys, html, subprocess, os
import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "us-china-ai-chip-export-controls")
SECTION_ORDER = ["chronology", "actors", "indicators", "scenarios"]
SECTION_TITLES = {"chronology": "Chronology", "actors": "Actor positions", "indicators": "Trigger indicators", "scenarios": "Baseline and scenarios"}
TITLE = "U.S. export controls on advanced AI chips to China, 2022–2026"
SUBTITLE = "Chronology, actor positions, trigger indicators, scenarios — a public-source method sample"


def load(path):
    with open(path) as f:
        return json.load(f)


def build_index(data):
    """Return {sid: item} with global ids."""
    idx = {}
    for si, sec in enumerate(SECTION_ORDER):
        for i, it in enumerate(data.get(sec, [])):
            sid = f"S{si*100 + i + 1}"
            it = dict(it)
            it["sid"] = sid
            it["section"] = sec
            idx[sid] = it
    return idx


def cite_to_html(md, idx):
    """Replace [S12] or [S12, S13] with superscript links; append confidence tag of the first cite."""
    def repl(m):
        ids = [x.strip() for x in m.group(1).split(",")]
        parts = []
        for sid in ids:
            if sid in idx:
                parts.append(f'<a class="cite" href="#{sid}" title="{html.escape(idx[sid].get("source_title") or "")}">{sid}</a>')
            else:
                parts.append(f'<span class="cite">{html.escape(sid)}</span>')
        return " " + " ".join(parts)
    return re.sub(r"\s*\[((?:S\d+)(?:\s*,\s*S\d+)*)\]", repl, md)


def label_to_html(md):
    """Turn (confirmed)/(reported)/(inferred) markers into tags."""
    return re.sub(r"\((confirmed|reported|inferred)\)", lambda m: f'<span class="tag {m.group(1)}">{m.group(1)}</span>', md)


def render_brief_html(brief_md, idx):
    md = cite_to_html(brief_md, idx)
    md = label_to_html(md)
    body = markdown.markdown(md, extensions=["extra", "sane_lists"])
    return body


def render_sources(idx):
    rows = []
    for sec in SECTION_ORDER:
        items = [it for it in idx.values() if it["section"] == sec]
        if not items:
            continue
        rows.append(f"<h3>{SECTION_TITLES[sec]}</h3><ol class='src'>")
        for it in items:
            v = it.get("verdict", "reported")
            title = html.escape(it.get("source_title") or it.get("publisher") or it.get("source_url") or "")
            url = html.escape(it.get("source_url") or "")
            pub = html.escape(it.get("publisher") or "")
            sdate = html.escape(it.get("source_date") or "")
            claim = html.escape(it.get("claim") or "")
            date = html.escape(it.get("date") or "")
            link = f'<a href="{url}" rel="noopener">{title or url}</a>' if url and it.get("source_type") != "unsourced" else "<em>analyst judgment — no external source</em>"
            meta = " · ".join(x for x in [pub, sdate] if x)
            rows.append(f'<li id="{it["sid"]}"><strong>{it["sid"]}</strong> <span class="tag {v}">{v}</span> '
                        f'{("<time>"+date+"</time> — ") if date else ""}{claim}<br>{link}{(" <span class=meta>· "+meta+"</span>") if meta else ""}</li>')
        rows.append("</ol>")
    return "\n".join(rows)


def page(brief_html, sources_html, generated, counts):
    legend = ('<div class="legend"><span><span class="tag confirmed">confirmed</span> primary source directly supports the claim</span>'
              '<span><span class="tag reported">reported</span> reputable secondary source</span>'
              '<span><span class="tag inferred">inferred</span> analyst judgment</span></div>')
    stats = ", ".join(f"{k}: {v}" for k, v in counts.items())
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(TITLE)} — Koray Nar</title>
<meta name="description" content="{html.escape(SUBTITLE)}. Public-source research method sample by Koray Nar with confidence-labeled sources.">
<link rel="stylesheet" href="../style.css">
</head>
<body>
<div class="wrap">
  <header class="doc">
    <span class="kicker">Public method sample · not commissioned · no forecasts</span>
    <h1>{html.escape(TITLE)}</h1>
    <p class="meta">{html.escape(SUBTITLE)}</p>
    <p class="meta">Koray Nar · Public-source research analyst · Istanbul (remote) · <a href="mailto:koraynar@gmail.com">koraynar@gmail.com</a> · Information cutoff {generated} · <a class="btn" href="brief.pdf">Download PDF</a></p>
    {legend}
  </header>

  <div class="box">
    <h3>How this was produced</h3>
    <p>Sources were collected first by parallel research passes (one per section), then <em>every</em> claim was checked against its cited document by a separate verification pass that could downgrade or drop it. Items that failed verification were removed. Scenarios and “what a change would signal” lines are analyst judgment and are labeled <span class="tag inferred">inferred</span>. Several AI models worked the task in fixed roles; the author supervised, resolved disagreements, and signed off. Source tally: {stats}.</p>
  </div>

  <div class="brief">
  {brief_html}
  </div>

  <h2 id="sources">Source appendix</h2>
  <p class="meta">Each entry: id · confidence · date — claim · source. Ids match the [S#] cites above.</p>
  {sources_html}

  <footer>© Koray Nar · Public-source method sample published {generated} · No insider or exclusive sources · Not investment, legal, or policy advice · <a href="../">All samples</a></footer>
</div>
</body>
</html>
"""


def main(path):
    d = load(path)
    idx = build_index(d["data"])
    counts = {}
    for it in idx.values():
        counts[it.get("verdict", "?")] = counts.get(it.get("verdict", "?"), 0) + 1
    brief_html = render_brief_html(d["brief"], idx)
    sources_html = render_sources(idx)
    os.makedirs(OUTDIR, exist_ok=True)
    out = os.path.join(OUTDIR, "index.html")
    with open(out, "w") as f:
        f.write(page(brief_html, sources_html, d.get("generated", ""), counts))
    print("wrote", out, "sources", len(idx), counts)
    # PDF via headless Chrome
    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    pdf = os.path.join(OUTDIR, "brief.pdf")
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}", "file://" + out],
                   check=False, capture_output=True, timeout=120)
    print("pdf", os.path.exists(pdf), os.path.getsize(pdf) if os.path.exists(pdf) else 0)


if __name__ == "__main__":
    main(sys.argv[1])
