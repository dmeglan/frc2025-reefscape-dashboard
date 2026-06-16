import json, html, os
import config as C
from deepdive_data import TEAMS, BONUS, link_type, STUDY_PICKS, DROP, CONF_HIGH, CAD_FIX, STUDY_PICK_WHY

BASE = os.path.dirname(os.path.abspath(__file__))
codex = json.load(open(os.path.join(BASE, "codex_data.json")))
DD = {t["team"]: t for t in (TEAMS + BONUS)}
PICKS = STUDY_PICKS

# (a) Refresh stale confidence: teams now backed by a BtB transcript or strong public code -> High.
# (c) Drop the low-rank, build-thread-only tail (no deep profile, mechanisms unconfirmed).
# CAD/Design badge corrections from the audit (codex flag vs researched cad_label).

# Explicit "why this is a study pick" rationale. Every pick has downloadable CAD OR a tech binder;
# the text leads with what to study and names the public resource that makes it reproducible.

# priority for ordering links by usefulness
TYPE_ORDER = {"cad":0,"binder":1,"code":2,"thread":3,"dds":4,"video":5,"site":6,"stats":7,"none":9}

def merge_links(team):
    seen={}; out=[]
    def add(label,url):
        if not url: return
        k=url.lower().rstrip("/")
        if k in seen: return
        seen[k]=1
        ty,tl=link_type(url)
        out.append({"label":label,"url":url,"t":ty,"tl":tl})
    dd=DD.get(team)
    if dd:
        add(dd["cad_label"], dd.get("cad_url"))
        for l,u in dd.get("sources",[]): add(l,u)
    for l in (next((c for c in codex if c["team"]==team),{}) or {}).get("links",[]):
        add(l.get("label"), l.get("url"))
    out.sort(key=lambda x: TYPE_ORDER.get(x["t"],8))
    return out

rows=[]
for c in codex:
    t=c["team"]; dd=DD.get(t)
    if t in DROP: continue
    plink = (dd.get("cad_url") if dd else None) or c.get("link") or ""
    plabel = (dd.get("cad_label") if dd else None) or "Primary source"
    pt,ptl = link_type(plink)
    cad = CAD_FIX.get(t, c.get("cad"))
    deep=None
    if dd:
        deep={"shooter":dd["shooter"],"intake":dd["intake"],"indexer":dd["indexer"],
              "drivetrain":dd["drivetrain"],"lessons":dd.get("lessons",[])}
    rows.append({
        "team":t,"name":c.get("name"),"region":c.get("region"),
        "epa":c.get("epa"),"rank":c.get("rank"),"rec":c.get("rec"),
        "wr":c.get("winrate"),"evts":c.get("eventCount"),
        "conf":("High" if t in CONF_HIGH else (c.get("confidence") or "—")),"cad":cad,
        "plink":plink,"plabel":plabel,"pt":pt,"ptl":ptl,
        "arch":(dd["archetype"] if dd else c.get("arch")),
        "vis":(dd["vision"] if dd else c.get("vis")),
        "pick":t in PICKS,
        "study":(STUDY_PICK_WHY.get(t) if t in PICKS else None) or c.get("study") or "","evidence":c.get("evidence") or "",
        "sourceNote":c.get("sourceNote") or "","tags":c.get("tags") or [],
        "status":c.get("status") or "","deep":deep,
        "links":merge_links(t),
    })
_has_epa = any(r["epa"] for r in rows)
if _has_epa:
    rows.sort(key=lambda r:-(r["epa"] or 0))
else:
    rows.sort(key=lambda r: r["team"])   # EPA enrichment pending (Statbotics outage) -> stable team-number order
maxepa=max([r["epa"] or 0 for r in rows], default=1) or 1
n=len(rows)
ny=sum(1 for r in rows if r["cad"]=="Yes"); npart=sum(1 for r in rows if r["cad"]=="Partial")
nno=sum(1 for r in rows if r["cad"]=="No"); npick=sum(1 for r in rows if r["pick"])
nhi=sum(1 for r in rows if r["conf"]=="High")
ndeep=sum(1 for r in rows if r["deep"])
J=json.dumps(rows, ensure_ascii=False)

# Export the dashboard's own state so the changelog/banner (apply_changelog.py)
# uses the exact counts and pick/CAD set that the table actually displays.
_state={"counts":{"teams":n,"cadYes":ny,"partial":npart,"none":nno,"highConf":nhi,"picks":npick},
        "rows":[{"team":r["team"],"name":r["name"],"pick":bool(r["pick"]),"cad":r["cad"]} for r in rows]}
json.dump(_state, open(os.path.join(BASE,"dashboard_state.json"),"w"), indent=1, ensure_ascii=False)

TMPL = r"""<!DOCTYPE html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>__DASHTITLE__</title>
<style>
:root{--navy:#16264a;--blue:#2e5496;--blue2:#3f72c4;--ink:#1a2235;--mut:#65718a;--line:#e4e9f2;--bg:#eef2f8;--card:#fff;--gold:#f4ad17;--green:#1a9c5b;--amber:#d98300;--red:#d1495b;--purple:#6b4ec2;--teal:#0e9b9b}
*{box-sizing:border-box}body{margin:0;font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;background:var(--bg);color:var(--ink);line-height:1.5}
.wrap{max-width:1500px;margin:0 auto;padding:22px}
header{position:relative;background:linear-gradient(120deg,#13213f,#2e5496 65%,#3f72c4);color:#fff;border-radius:16px;padding:26px 32px;box-shadow:0 10px 30px rgba(16,32,64,.26)}
header h1{margin:0 0 6px;font-size:25px;padding-right:230px}
header p{margin:0;opacity:.9;font-size:13.5px;max-width:1000px}
.brand{position:absolute;top:22px;right:26px;display:inline-flex;align-items:center;gap:6px;text-decoration:none;font-size:12px;font-weight:700;color:rgba(255,255,255,.92);background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.28);padding:5px 11px;border-radius:20px;line-height:1}
.brand:hover{background:rgba(255,255,255,.22);color:#fff}
.foot .by{color:var(--blue);text-decoration:none;font-weight:700}
@media(max-width:680px){header h1{padding-right:0}.brand{position:static;margin-top:11px}}
.method{margin:16px 0;padding:12px 16px;border:1px solid var(--line);border-radius:11px;background:#fffdf6;color:#3d4654;font-size:12.7px;line-height:1.55}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:13px;margin:18px 0}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;box-shadow:0 2px 8px rgba(30,50,90,.05)}
.kpi .n{font-size:26px;font-weight:800;color:var(--navy);line-height:1}
.kpi .l{font-size:11.5px;color:var(--mut);margin-top:6px;text-transform:uppercase;letter-spacing:.5px;font-weight:700}
.kpi.gold{background:linear-gradient(135deg,#fff8e6,#fff);border-color:#f3d98a}
.controls{position:sticky;top:0;z-index:6;display:flex;flex-wrap:wrap;gap:9px;align-items:center;background:var(--bg);padding:12px 0;margin-bottom:4px}
input[type=search],select{padding:9px 12px;border:1px solid var(--line);border-radius:9px;font-size:13.5px;background:#fff;color:var(--ink)}
input[type=search]{min-width:230px;flex:1}
.chip{padding:8px 13px;border-radius:9px;border:1px solid var(--line);background:#fff;cursor:pointer;font-size:13px;font-weight:700;user-select:none}
.chip.on{background:var(--navy);color:#fff;border-color:var(--navy)}
.count{margin-left:auto;font-size:12.5px;color:var(--mut);font-weight:700}
.legend{display:flex;flex-wrap:wrap;gap:8px;font-size:11.5px;color:var(--mut);margin:4px 2px 10px;align-items:center}
.tablewrap{background:var(--card);border:1px solid var(--line);border-radius:13px;overflow:auto;box-shadow:0 3px 14px rgba(30,50,90,.06)}
table{border-collapse:collapse;width:100%;font-size:13px;min-width:1120px}
thead th{position:sticky;top:0;background:var(--blue);color:#fff;text-align:left;padding:10px 11px;font-weight:600;white-space:nowrap;z-index:2;cursor:pointer}
thead th:hover{background:#27487f}.thsort{font-size:10px;opacity:.6}
tbody td{padding:9px 11px;border-top:1px solid var(--line);vertical-align:top}
tbody tr.main{cursor:pointer}tbody tr.main:hover{background:#f0f4fc}
tr.pick td{background:#fffaed}tr.pick:hover td{background:#fff4d6!important}
.tm{font-weight:800;color:var(--navy)}.region{font-size:10.5px;color:var(--mut);font-weight:700}
.nm{font-weight:700}.nm .star{color:var(--gold)}
.epaCell{min-width:104px}.epaNum{font-weight:800;font-size:14px}
.bar{height:7px;border-radius:5px;background:linear-gradient(90deg,#3f72c4,#1a9c5b);margin-top:4px}
.badge{display:inline-block;padding:3px 9px;border-radius:20px;font-size:11px;font-weight:800;letter-spacing:.3px;white-space:nowrap}
.b-Yes{background:#dcf5e6;color:var(--green)}.b-Partial{background:#fdeecb;color:var(--amber)}.b-No{background:#fbdcdf;color:var(--red)}
.cf-High{background:#dcf5e6;color:#0a7d44}.cf-Medium{background:#fdeecb;color:#9a5b00}.cf-Low{background:#eceff4;color:#5b6678}
.why{color:#43506a;font-size:12.3px;max-width:330px}
.exp{font-size:15px;color:var(--blue);font-weight:800;width:20px;text-align:center}
a.lk{font-size:11.5px;font-weight:700;text-decoration:none;padding:3px 9px;border-radius:7px;border:1px solid;white-space:nowrap}
.t-cad{color:#0a7d44;border-color:#9bdab9;background:#e9f8f0}.t-binder{color:#9a5b00;border-color:#f0c48a;background:#fdf2df}
.t-code{color:#5a3bb0;border-color:#cdbdf0;background:#f0ebfb}.t-thread{color:#1f5fb0;border-color:#b8d2f0;background:#eaf2fc}
.t-dds{color:#7a1fb0;border-color:#dcb8f0;background:#f6eafc}.t-video{color:#b02a37;border-color:#f0bcc2;background:#fceaec}
.t-stats,.t-site,.t-none{color:#566;border-color:#d6deea;background:#eef2f8}
tr.detail td{background:#f7f9fd;border-top:none}
.panel{padding:6px 4px 12px}
.parch{font-size:14px;font-weight:800;color:var(--blue);margin:2px 0 8px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:9px;margin-bottom:9px}
.sub{background:#fff;border:1px solid var(--line);border-radius:9px;padding:8px 11px}
.sub .k{font-size:10px;text-transform:uppercase;letter-spacing:.5px;color:var(--mut);font-weight:800}
.sub .v{font-size:12.6px;margin-top:2px}.sub.vis .k{color:var(--teal)}
.block{margin:9px 0}.block .h{font-size:10.5px;text-transform:uppercase;letter-spacing:.6px;font-weight:800;margin-bottom:4px}
.h-why{color:#1f5fb0}.h-les{color:var(--gold)}.h-ev{color:var(--mut)}.h-src{color:var(--navy)}
.block ul{margin:0;padding-left:18px}.block li{font-size:12.8px;margin:3px 0}
.evidence{font-size:12.5px;color:#43506a}
.links{display:flex;flex-wrap:wrap;gap:7px}
.tags{margin-top:7px}.tag{display:inline-block;font-size:10.5px;color:#566;background:#eef2f8;border:1px solid #d6deea;border-radius:6px;padding:2px 7px;margin:2px 4px 0 0;font-weight:700}
.foot{color:var(--mut);font-size:12px;margin:16px 4px;line-height:1.6}
/* ===== platform auto-switch: wide screens use the interactive table (.wrap); narrow screens use the no-JS card view (.view-mobile) ===== */
.view-mobile{display:none}
@media(max-width:820px){.wrap{display:none}.view-mobile{display:block;max-width:820px;margin:0 auto;padding:12px}}
.view-mobile header{padding:16px 17px}
.view-mobile header h1{font-size:18px;padding-right:0;line-height:1.25}
.view-mobile header p{font-size:12.5px}
.view-mobile .brand{position:static;margin-top:11px}
.m-kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:12px 0}
.m-kpi{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 8px;text-align:center}
.m-kpi.gold{background:linear-gradient(135deg,#fff8e6,#fff);border-color:#f3d98a}
.m-kpi .n{font-size:20px;font-weight:800;color:var(--navy);line-height:1}
.m-kpi .l{font-size:9px;color:var(--mut);margin-top:3px;text-transform:uppercase;letter-spacing:.4px;font-weight:700}
.m-hint{font-size:12px;color:var(--mut);font-weight:600;margin:10px 2px}
.m-list{display:flex;flex-direction:column;gap:9px}
.mcard{background:#fff;border:1px solid var(--line);border-radius:13px;box-shadow:0 2px 9px rgba(30,50,90,.06);overflow:hidden}
.mcard.pick{border-color:#f3d98a;background:linear-gradient(180deg,#fffdf4,#fff)}
summary.mhead{list-style:none;padding:12px 14px;cursor:pointer;display:flex;align-items:flex-start;gap:11px}
summary.mhead::-webkit-details-marker{display:none}
.mteam{font-size:18px;font-weight:800;color:var(--navy);line-height:1}
.mname{font-size:13.5px;font-weight:700;margin-top:3px}.mname .star{color:var(--gold)}
.march{font-size:11.5px;color:var(--mut);margin-top:5px;line-height:1.35}
.mright{flex:0 0 auto;text-align:center;min-width:54px}
.mepa{font-size:21px;font-weight:800;color:var(--navy);line-height:1}
.mepal{font-size:8px;font-weight:700;text-transform:uppercase;letter-spacing:.4px;color:var(--mut);margin-top:2px}
.mbadge{margin-top:6px}
.mdetail{border-top:1px solid var(--line);background:#f7f9fd;padding:11px 14px}
.mmeta{font-size:11.5px;color:var(--mut);font-weight:700;margin-bottom:8px}
.view-mobile .grid{grid-template-columns:1fr}
.view-mobile .exp{display:none}
/* CSS-only "study picks only" toggle (no JS on mobile) */
.mpick-cb{position:absolute;left:-9999px;opacity:0}
.mpill{display:inline-block;font-size:13px;font-weight:800;padding:8px 15px;border-radius:20px;border:1px solid var(--line);background:#fff;color:var(--navy);cursor:pointer;user-select:none;margin:2px 0 9px}
.mpick-cb:checked + .mpill{background:var(--navy);color:#fff;border-color:var(--navy)}
.mpick-cb:checked ~ .m-list .mcard:not(.pick){display:none}
.mpill .lp-on{display:none}
.mpick-cb:checked + .mpill .lp-off{display:none}
.mpick-cb:checked + .mpill .lp-on{display:inline}
</style></head><body><div class=wrap>
<header><h1>__DASHTITLE__</h1>
<p>__SUB__</p><a class=brand href="https://linkedin.com/in/dmeglan" target="_blank" rel="noopener" aria-label="Dwight Meglan on LinkedIn"><svg viewBox="0 0 24 24" width="13" height="13" aria-hidden="true"><path fill="currentColor" d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.13 1.45-2.13 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.45v6.29zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z"/></svg><span>Dwight Meglan · 1757/8567</span></a></header>
<div class=method><b>How to read this:</b> <b>Confidence</b> rates how well the design is publicly documented — <b>High</b> = downloadable CAD located; <b>Medium</b> = tech binder / code / renders / photos; <b>Low</b> = little public. <b>Click any row</b> (or the ▸) to expand its Details panel: subsystem breakdown, why it's worth studying, the evidence behind the rating, study lessons, and every source link. "Unconfirmed" vision = not publicly stated, not necessarily absent.</div>
<div class=cards id=cards></div>
<div class=controls>
<input id=q type=search placeholder="Search team, name, mechanism, vision, why-study, tag…">
<select id=arch><option value="">Archetype: all</option><option value=elevator>Elevator</option><option value=arm>Arm / pivot</option><option value=algae>Algae-capable</option><option value=coral-only>Coral-only</option><option value=ground>Ground intake</option><option value="deep climb">Deep climb</option></select>
<select id=cad><option value="">CAD: all</option><option value=Yes>CAD released</option><option value=Partial>Partial</option><option value=No>None public</option></select>
<select id=conf><option value="">Confidence: all</option><option value=High>High</option><option value=Medium>Medium</option><option value=Low>Low</option></select>
<div class=chip id=pick>★ Study picks</div>
<div class=count id=count></div></div>
<div class=legend>Link types:
<span class="lk t-cad">CAD</span><span class="lk t-binder">Tech binder</span><span class="lk t-code">Code</span><span class="lk t-thread">CD thread</span><span class="lk t-dds">DDS</span><span class="lk t-video">Video</span><span class="lk t-stats">Stats</span></div>
<div class=tablewrap><table>
<thead><tr>
<th data-k=team>Team <span class=thsort></span></th>
<th data-k=name>Name</th>
<th data-k=epa>EPA <span class=thsort>▼</span></th>
<th data-k=rank>Rank</th>
<th data-k=rec>Record</th>
<th data-k=conf>Conf.</th>
<th data-k=cad>CAD / Design</th>
<th data-k=arch>Archetype</th>
<th data-k=study>Why study</th>
<th></th></tr></thead><tbody id=tb></tbody></table></div>
<div class=foot><b>Sources:</b> <a href="https://cadcollection.spectrum3847.org">Spectrum 3847 CAD Collection</a> & team CAD releases (Onshape / GrabCAD), <a href="https://www.chiefdelphi.com">Chief Delphi</a> reveal / CAD-release threads, and <a href="https://www.statbotics.io">Statbotics</a> EPA/records (2025, backfilled when the API recovers). This page is fully self-contained — all data embedded. Built June 2026. &nbsp;·&nbsp; __CREDIT_NAME__</div>
</div>
__MOBILE__
<script>
const DATA=__J__, MAX=__MAX__;
const cards=[['__N__','Robots tracked',''],['__NY__','CAD released','gold'],['__NPART__','Partial',''],['__NHI__','High confidence',''],['__NPICK__','★ Study picks','gold']];
document.getElementById('cards').innerHTML=cards.map(c=>`<div class="kpi ${c[2]}"><div class=n>${c[0]}</div><div class=l>${c[1]}</div></div>`).join('');
let sortK='epa',dir=-1,pickOnly=false;
function am(a,f){a=(a||'').toLowerCase();if(!f)return true;if(f=='ground')return a.includes('ground')||a.includes('floor');if(f=='deep climb')return a.includes('deep climb')||a.includes('deep cage');if(f=='coral-only')return a.includes('coral-only')||a.includes('coral only');return a.includes(f);}
function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function detail(d){
  let subs='';
  if(d.deep){subs=`<div class=grid>
    <div class=sub><div class=k>Scoring (coral / algae)</div><div class=v>${esc(d.deep.shooter)}</div></div>
    <div class=sub><div class=k>Intake</div><div class=v>${esc(d.deep.intake)}</div></div>
    <div class=sub><div class=k>Elevator / lift</div><div class=v>${esc(d.deep.indexer)}</div></div>
    <div class=sub><div class=k>Drivetrain</div><div class=v>${esc(d.deep.drivetrain)}</div></div>
    <div class="sub vis"><div class=k>Vision</div><div class=v>${esc(d.vis)}</div></div></div>`;}
  else{subs=`<div class=grid><div class="sub vis"><div class=k>Vision</div><div class=v>${esc(d.vis)}</div></div></div>`;}
  const lessons=(d.deep&&d.deep.lessons&&d.deep.lessons.length)?`<div class=block><div class="h h-les">Lessons for students</div><ul>${d.deep.lessons.map(l=>`<li>${esc(l)}</li>`).join('')}</ul></div>`:'';
  const links=d.links.map(l=>`<a class="lk t-${l.t}" href="${l.url}" target=_blank rel=noopener>${esc(l.label)} ↗</a>`).join('');
  const tags=d.tags&&d.tags.length?`<div class=tags>${d.tags.map(t=>`<span class=tag>${esc(t)}</span>`).join('')}</div>`:'';
  return `<div class=panel>
    <div class=parch>${esc(d.arch)}</div>
    ${subs}
    <div class=block><div class="h h-why">Why study it</div><div class=why style="max-width:none">${esc(d.study)}</div></div>
    ${lessons}
    <div class=block><div class="h h-ev">Evidence &amp; confidence</div><div class=evidence><b>${esc(d.conf)} confidence.</b> ${esc(d.evidence)}${d.sourceNote?' — '+esc(d.sourceNote):''}</div></div>
    <div class=block><div class="h h-src">Sources &amp; links</div><div class=links>${links}</div>${tags}</div>
  </div>`;
}
function render(){
  const q=document.getElementById('q').value.toLowerCase(),af=document.getElementById('arch').value,cf=document.getElementById('cad').value,kf=document.getElementById('conf').value;
  let rows=DATA.filter(d=>{
    if(pickOnly&&!d.pick)return false;
    if(cf&&d.cad!=cf)return false;
    if(kf&&d.conf!=kf)return false;
    if(af&&!am(d.arch,af))return false;
    if(q){const b=(d.team+' '+d.name+' '+d.arch+' '+d.vis+' '+d.study+' '+(d.tags||[]).join(' ')+' '+(d.deep?d.deep.shooter+d.deep.intake+d.deep.indexer:'')+' '+d.region).toLowerCase();if(!b.includes(q))return false;}
    return true;});
  rows.sort((a,b)=>{let x=a[sortK],y=b[sortK];if(sortK=='rank'){x=x||1e9;y=y||1e9;}if(typeof x=='string'){x=(x||'').toLowerCase();y=(y||'').toLowerCase();return x<y?-dir:x>y?dir:0;}return ((x||0)-(y||0))*dir;});
  document.getElementById('count').textContent=rows.length+' robots';
  const tb=document.getElementById('tb');tb.innerHTML='';
  rows.forEach((d,i)=>{
    const w=Math.max(4,Math.round((d.epa||0)/MAX*100));
    const epaTxt=d.epa?d.epa:'—';
    const epaBar=d.epa?`<div class=bar style="width:${w}%"></div>`:'';
    const plink=d.plink?`<a class="lk t-${d.pt}" href="${d.plink}" target=_blank rel=noopener>${esc(d.ptl)} ↗</a>`:'<span style=color:#aab>—</span>';
    const tr=document.createElement('tr');tr.className='main'+(d.pick?' pick':'');
    tr.innerHTML=`<td class=tm>${d.team}<div class=region>${esc(d.region)}</div></td>
      <td class=nm>${d.pick?'<span class=star>★ </span>':''}${esc(d.name)}</td>
      <td class=epaCell><span class=epaNum>${epaTxt}</span>${epaBar}</td>
      <td>#${d.rank||'—'}</td><td>${esc(d.rec)}</td>
      <td><span class="badge cf-${d.conf}">${esc(d.conf)}</span></td>
      <td><span class="badge b-${d.cad}">${d.cad}</span><div style=margin-top:5px>${plink}</div></td>
      <td style="max-width:260px"><div style="font-size:12.3px">${esc(d.arch)}</div></td>
      <td class=why>${esc(d.study).slice(0,150)}${d.study.length>150?'…':''}</td>
      <td class=exp>▸</td>`;
    const dr=document.createElement('tr');dr.className='detail';dr.style.display='none';
    dr.innerHTML=`<td colspan=10>${detail(d)}</td>`;
    tr.onclick=(e)=>{if(e.target.tagName=='A')return;const open=dr.style.display!='none';dr.style.display=open?'none':'';tr.querySelector('.exp').textContent=open?'▸':'▾';};
    tb.appendChild(tr);tb.appendChild(dr);
  });
}
document.querySelectorAll('thead th[data-k]').forEach(th=>th.onclick=()=>{const k=th.dataset.k;if(sortK==k)dir*=-1;else{sortK=k;dir=(k=='epa')?-1:1;}document.querySelectorAll('.thsort').forEach(s=>s.textContent='');th.querySelector('.thsort').textContent=dir<0?'▼':'▲';render();});
['q','arch','cad','conf'].forEach(id=>document.getElementById(id).addEventListener('input',render));
document.getElementById('pick').onclick=function(){pickOnly=!pickOnly;this.classList.toggle('on',pickOnly);render();};
render();
</script></body></html>"""

_epa_note = ("" if _has_epa else
    "EPA / rank / record columns show — because Statbotics' data API is mid-outage; they will be backfilled once it recovers. ")
sub=(f"A catalog of {n} FRC {C.YEAR} {C.GAME} robots that publicly released downloadable CAD "
     f"({ny} with CAD), enriched with mechanism and vision detail mined from each team's Chief Delphi reveal/release thread. "
     f"{_epa_note}"
     f"Discovery: the Spectrum 3847 CAD Collection + Chief Delphi. "
     f"Each row shows a CAD/Design status, a documentation-confidence rating ({nhi} High), archetype, vision system, and a 'why study it' note. "
     f"The {npick} ★ study picks all have downloadable CAD or a full technical binder. "
     f"Click any row for an expandable subsystem teardown of the {ndeep} deeply-profiled teams. ")
# ---- static, no-JS MOBILE view (mirrors the SRS dashboard's phone layout) ----
def _esc(s): return html.escape("" if s is None else str(s))
_BRAND=('<a class=brand href="https://linkedin.com/in/dmeglan" target="_blank" rel="noopener" '
        'aria-label="Dwight Meglan on LinkedIn"><svg viewBox="0 0 24 24" width="13" height="13" aria-hidden="true">'
        '<path fill="currentColor" d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.13 1.45-2.13 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.45v6.29zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z"/></svg>'
        '<span>Dwight Meglan · 1757/8567</span></a>')
def _msubs(d):
    dd=d["deep"]
    if dd:
        return ('<div class=grid>'
          f'<div class=sub><div class=k>Scoring (coral / algae)</div><div class=v>{_esc(dd["shooter"])}</div></div>'
          f'<div class=sub><div class=k>Intake</div><div class=v>{_esc(dd["intake"])}</div></div>'
          f'<div class=sub><div class=k>Elevator / lift</div><div class=v>{_esc(dd["indexer"])}</div></div>'
          f'<div class=sub><div class=k>Drivetrain</div><div class=v>{_esc(dd["drivetrain"])}</div></div>'
          f'<div class="sub vis"><div class=k>Vision</div><div class=v>{_esc(d["vis"])}</div></div></div>')
    return f'<div class=grid><div class="sub vis"><div class=k>Vision</div><div class=v>{_esc(d["vis"])}</div></div></div>'
def _mcard(d):
    dd=d["deep"]
    star='<span class=star>★ </span>' if d["pick"] else ''
    lessons=''
    if dd and dd.get("lessons"):
        lessons=('<div class=block><div class="h h-les">Lessons for students</div><ul>'
                 +''.join(f'<li>{_esc(l)}</li>' for l in dd["lessons"])+'</ul></div>')
    links=''.join(f'<a class="lk t-{l["t"]}" href="{l["url"]}" target=_blank rel=noopener>{_esc(l["label"])} ↗</a>' for l in d["links"])
    tags=('<div class=tags>'+''.join(f'<span class=tag>{_esc(t)}</span>' for t in d["tags"])+'</div>') if d.get("tags") else ''
    src=(' — '+_esc(d["sourceNote"])) if d.get("sourceNote") else ''
    return (f'<details class="mcard{" pick" if d["pick"] else ""}"><summary class=mhead>'
      f'<div style="flex:1;min-width:0"><div class=mteam>{d["team"]}</div>'
      f'<div class=mname>{star}{_esc(d["name"])}</div><div class=march>{_esc(d["arch"])}</div></div>'
      f'<div class=mright><div class=mepa>{d["epa"] or "—"}</div><div class=mepal>EPA</div>'
      f'<div class=mbadge><span class="badge b-{d["cad"]}">{d["cad"]}</span></div></div></summary>'
      f'<div class=mdetail><div class=mmeta>{_esc(d["region"])} · {_esc(d["rec"])} · #{d["rank"] or "—"} · {_esc(d["conf"])} confidence</div>'
      f'{_msubs(d)}'
      f'<div class=block><div class="h h-why">Why study it</div><div class=why style="max-width:none">{_esc(d["study"])}</div></div>'
      f'{lessons}'
      f'<div class=block><div class="h h-ev">Evidence &amp; confidence</div><div class=evidence><b>{_esc(d["conf"])} confidence.</b> {_esc(d["evidence"])}{src}</div></div>'
      f'<div class=block><div class="h h-src">Sources &amp; links</div><div class=links>{links}</div>{tags}</div>'
      f'</div></details>')
_m_kpis="".join(f'<div class="m-kpi {cls}"><div class=n>{val}</div><div class=l>{lab}</div></div>'
    for val,lab,cls in [(n,'Robots',''),(ny,'CAD',''),(npick,'★ Picks','gold')])
_m_cards="".join(_mcard(d) for d in rows)   # rows already sorted by EPA desc
MOBILE_HTML=('<div class="view-mobile"><header><h1>__DASHTITLE__</h1><p>'
    +_esc("Teams that released downloadable CAD for REEFSCAPE. Tap a team for its subsystem teardown, why-study notes and links. "
          "★ = study pick. EPA/rank pending a Statbotics outage. Open on a computer for live search, filtering and column sorting.")
    +'</p>'+_BRAND+'</header>'
    +f'<div class=m-kpis>{_m_kpis}</div>'
    +f'<div class=m-hint>{n} robots with released CAD · ★ {npick} study picks. Tap any card to expand.</div>'
    +'<input type=checkbox id=mpick class=mpick-cb>'
    +f'<label for=mpick class=mpill><span class=lp-off>★ Show study picks only</span>'
     f'<span class=lp-on>★ Showing {npick} picks · show all {n}</span></label>'
    +f'<div class=m-list>{_m_cards}</div>'
    +'<div class=foot>Sources: Spectrum 3847 CAD Collection, team CAD releases (Onshape / GrabCAD), '
     'Chief Delphi reveal / CAD-release threads, Statbotics (2025). Open on a computer for the full interactive table. '
     '&nbsp;·&nbsp; Compiled by <a class=by href="https://linkedin.com/in/dmeglan" target="_blank" rel="noopener">'
     '__CREDIT_NAME__</a></div></div>')

out=(TMPL.replace("__J__",J).replace("__MAX__",str(maxepa)).replace("__SUB__",html.escape(sub))
     .replace("__N__",str(n)).replace("__NY__",str(ny)).replace("__NPART__",str(npart))
     .replace("__NHI__",str(nhi)).replace("__NPICK__",str(npick))
     .replace("__MOBILE__",MOBILE_HTML).replace("__DASHTITLE__",C.DASH_TITLE).replace("__CREDIT_NAME__",C.CREDIT_NAME))
open(os.path.join(BASE, C.DASH_FILE),"w").write(out)
print("v3 ok rows",n,"Yes",ny,"Partial",npart,"No",nno,"HighConf",nhi,"picks",npick)
