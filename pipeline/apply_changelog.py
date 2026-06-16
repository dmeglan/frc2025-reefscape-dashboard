#!/usr/bin/env python3
"""apply_changelog.py — FRC 2026 REBUILT dashboard changelog + publish-prep.

Mirrors the SRS "build_site.py" changelog mechanism, adapted to this project:
  * diffs codex_data.json against pipeline/snapshot.json (added/removed teams,
    new study picks, CAD upgrades),
  * prepends a dated entry to pipeline/changelog.json when something changed,
  * injects an "Updated …" banner + a "What's changed" panel into the freshly
    built dashboard HTML,
  * writes the published copy as <repo root>/index.html (for GitHub Pages) and
    refreshes the local FRC2026_Rebuilt_Robot_Study_Dashboard_v3.html, and
  * copies the deep-dive HTML/PDF to the repo root as deep-dive.html / deep-dive.pdf.

Run it AFTER build_dashboard_v3.py / build_deepdive_*.py. Then push with publish.sh.

Usage:  python3 pipeline/apply_changelog.py ["one-line summary override"]
Env:    FRC_DATE=YYYY-MM-DD to override the date (testing).
"""
import json, os, sys, datetime, shutil
import config as C

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TODAY = os.environ.get("FRC_DATE") or datetime.date.today().isoformat()

DASH_SRC = os.path.join(HERE, C.DASH_FILE)
DASH_LOCAL = os.path.join(REPO, C.DASH_FILE)
DEEP_HTML_SRC = os.path.join(HERE, C.DEEPDIVE_HTML)
DEEP_PDF_SRC = os.path.join(HERE, C.DEEPDIVE_PDF)
INDEX_OUT = os.path.join(REPO, "index.html")
DEEP_HTML_OUT = os.path.join(REPO, "deep-dive.html")
DEEP_PDF_OUT = os.path.join(REPO, "deep-dive.pdf")

def _e(s):
    return ("" if s is None else str(s)).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ---------- load the dashboard's own state (authoritative counts + pick/CAD set) ----------
# build_dashboard_v3.py writes dashboard_state.json; using it guarantees the banner
# and changelog match exactly what the rendered table shows (it excludes the DROP set
# and uses PICKS = STUDY_PICKS, not the raw codex `pick` flags).
state = json.load(open(os.path.join(HERE, "dashboard_state.json"), encoding="utf-8"))
counts = state["counts"]
cur = {str(r["team"]): {"name": r.get("name", ""), "pick": bool(r.get("pick")),
                        "cad": r.get("cad", "")} for r in state["rows"]}
teams_n = counts["teams"]
picks_n = counts["picks"]
cadyes_n = counts["cadYes"]

# ---------- diff vs last published snapshot ----------
spath = os.path.join(HERE, "snapshot.json")
old = json.load(open(spath)) if os.path.exists(spath) else {}
added = sorted(set(cur) - set(old), key=int)
removed = sorted(set(old) - set(cur), key=int)
became_pick = sorted([t for t in cur if t in old and cur[t]["pick"] and not old[t].get("pick")], key=int)
cad_up = sorted([t for t in cur if t in old and cur[t]["cad"] == "Yes" and old[t].get("cad") != "Yes"], key=int)
diff_nonempty = bool(added or removed or became_pick or cad_up)

def name_of(t):
    nm = cur.get(t, {}).get("name") or old.get(t, {}).get("name") or ""
    return f"{t} ({nm})" if nm else t

# ---------- changelog (persisted) ----------
clpath = os.path.join(HERE, "changelog.json")
cl = json.load(open(clpath)) if os.path.exists(clpath) else {"last_updated": TODAY, "entries": []}
override = sys.argv[1] if len(sys.argv) > 1 else ""

if override or diff_nonempty:
    if override:
        summary = override
    else:
        bits = []
        if added:       bits.append("added " + ", ".join(name_of(t) for t in added))
        if removed:     bits.append("removed " + ", ".join(name_of(t) for t in removed))
        if became_pick: bits.append(", ".join(name_of(t) for t in became_pick) + " → study pick")
        if cad_up:      bits.append("CAD upgraded for " + ", ".join(name_of(t) for t in cad_up))
        summary = "; ".join(bits) if bits else "minor updates"
    entry = {"date": TODAY, "summary": summary, "teams": teams_n, "picks": picks_n, "cadYes": cadyes_n}
    if cl["entries"] and cl["entries"][0].get("date") == TODAY:
        cl["entries"][0].update(entry)
    else:
        cl["entries"].insert(0, entry)
    cl["last_updated"] = TODAY

json.dump(cl, open(clpath, "w"), indent=1, ensure_ascii=False)
json.dump(cur, open(spath, "w"), indent=1, ensure_ascii=False)

# ---------- build banner + changelog panel HTML ----------
upd = cl.get("last_updated", TODAY)
updated_html = (
    '<div class=updated>Updated ' + _e(upd) + ' · ' + str(teams_n) + ' teams · '
    + str(picks_n) + ' study picks · ' + str(cadyes_n) + ' with downloadable CAD'
    ' · <a href="deep-dive.html">top-teams deep-dive ↗</a></div>'
)
rows = "".join(
    '<div class=cl-row><b>' + _e(e.get("date")) + '</b> — ' + _e(e.get("summary", ""))
    + ' <span class=cl-tot>(' + str(e.get("teams", "?")) + ' teams · '
    + str(e.get("picks", "?")) + ' picks)</span></div>'
    for e in cl["entries"][:12]
)
if not rows:
    rows = '<div class=cl-row>No changes recorded yet.</div>'
changelog_html = (
    '<details class=changelog><summary>What’s changed · ' + str(len(cl["entries"]))
    + ' update(s)</summary><div class=cl-body>' + rows + '</div></details>'
)
css_extra = (
    '.updated{margin-top:10px;font-size:12px;color:rgba(255,255,255,.85);font-weight:600}'
    '.updated a{color:#cfe0fb;text-decoration:none}'
    '.changelog{background:#fff;border:1px solid var(--line);border-radius:11px;margin:16px 0;box-shadow:0 2px 8px rgba(30,50,90,.05)}'
    '.changelog>summary{cursor:pointer;list-style:none;padding:11px 15px;font-weight:800;font-size:13px;color:var(--navy)}'
    '.changelog>summary::-webkit-details-marker{display:none}'
    '.cl-body{padding:2px 15px 13px}'
    '.cl-row{font-size:12.3px;color:var(--ink);padding:8px 0;border-top:1px solid #eef1f6;line-height:1.45}'
    '.cl-row:first-child{border-top:none}.cl-row b{color:var(--blue2)}.cl-tot{color:var(--mut)}'
)

# ---------- inject into the freshly built dashboard ----------
html = open(DASH_SRC, encoding="utf-8").read()
if "class=updated" not in html:  # idempotent: don't double-inject on re-runs
    html = html.replace("</style>", css_extra + "</style>", 1)
    # inject into EVERY header so both the desktop (.wrap) and mobile (.view-mobile) views show it
    html = html.replace("</header>", updated_html + "</header>" + changelog_html)

open(INDEX_OUT, "w", encoding="utf-8").write(html)
open(DASH_LOCAL, "w", encoding="utf-8").write(html)
if os.path.exists(DEEP_HTML_SRC): shutil.copyfile(DEEP_HTML_SRC, DEEP_HTML_OUT)
if os.path.exists(DEEP_PDF_SRC):  shutil.copyfile(DEEP_PDF_SRC, DEEP_PDF_OUT)

print(json.dumps({"date": upd, "teams": teams_n, "picks": picks_n, "cadYes": cadyes_n,
                  "added": [name_of(t) for t in added], "removed": [name_of(t) for t in removed],
                  "became_pick": [name_of(t) for t in became_pick], "cad_upgraded": [name_of(t) for t in cad_up],
                  "changed": bool(override or diff_nonempty), "index": INDEX_OUT}, ensure_ascii=False))
