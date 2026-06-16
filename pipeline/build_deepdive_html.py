import json, html, os
import config as C
from deepdive_data import TEAMS, BONUS, META, link_type, STUDY_PICKS
BASE = os.path.dirname(os.path.abspath(__file__))

def enrich(t):
    d=dict(t)
    d["lt"], d["ltlabel"]=link_type(t.get("cad_url",""), t.get("cad_label",""))
    d["src"]=[{"label":l,"url":u,"t":link_type(u)[0],"tl":link_type(u)[1]} for l,u in t.get("sources",[])]
    return d
data=[enrich(t) for t in TEAMS]
bonus=[enrich(t) for t in BONUS]
maxepa=(max([t["epa"] for t in TEAMS], default=1) or 1)
J=json.dumps(data); B=json.dumps(bonus); MAX=maxepa
OV=json.dumps(META["overview"])

H=r"""<!DOCTYPE html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>__DDTITLE__</title>
<style>
:root{--navy:#16264a;--blue:#2e5496;--blue2:#3f72c4;--ink:#1a2235;--mut:#65718a;--line:#e4e9f2;--bg:#eef2f8;--gold:#f4ad17;--card:#fff;--green:#1a9c5b;--amber:#d98300;--red:#d1495b;--purple:#6b4ec2;--teal:#0e9b9b}
*{box-sizing:border-box}body{margin:0;font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;background:var(--bg);color:var(--ink);line-height:1.5}
.wrap{max-width:1180px;margin:0 auto;padding:22px}
header{background:linear-gradient(120deg,#13213f,#2e5496 65%,#3f72c4);color:#fff;border-radius:18px;padding:30px 34px;box-shadow:0 10px 30px rgba(16,32,64,.28)}
header h1{margin:0 0 6px;font-size:27px}
header p{margin:0;opacity:.9;font-size:14px;max-width:900px}
.over{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:6px 22px;margin:18px 0;box-shadow:0 2px 10px rgba(30,50,90,.05)}
.over details{border-bottom:1px solid var(--line);padding:12px 0}.over details:last-child{border-bottom:none}
.over summary{cursor:pointer;font-weight:800;color:var(--navy);font-size:14.5px}
.over p{margin:8px 0 2px;font-size:13.6px;color:#333}
.controls{position:sticky;top:0;z-index:5;display:flex;flex-wrap:wrap;gap:9px;align-items:center;background:var(--bg);padding:12px 0;margin-bottom:6px}
input[type=search],select{padding:9px 12px;border:1px solid var(--line);border-radius:9px;font-size:13.5px;background:#fff;color:var(--ink)}
input[type=search]{min-width:240px;flex:1}
.chip{padding:8px 13px;border-radius:9px;border:1px solid var(--line);background:#fff;cursor:pointer;font-size:13px;font-weight:700;user-select:none}
.chip.on{background:var(--navy);color:#fff;border-color:var(--navy)}
.count{margin-left:auto;font-size:12.5px;color:var(--mut);font-weight:700}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;margin:13px 0;overflow:hidden;box-shadow:0 3px 12px rgba(30,50,90,.06)}
.card.pick{border:2px solid var(--gold)}
.chead{display:flex;align-items:center;gap:14px;padding:14px 18px;background:linear-gradient(90deg,#16264a,#27487f);color:#fff;cursor:pointer}
.rank{font-size:12px;font-weight:800;background:rgba(255,255,255,.16);padding:3px 9px;border-radius:20px;white-space:nowrap}
.rank.gold{background:var(--gold);color:#3a2c00}
.tnum{font-size:21px;font-weight:900;letter-spacing:.3px}
.tname{font-weight:700;font-size:15px}.trobot{opacity:.8;font-size:12.5px;font-weight:500}
.region{opacity:.72;font-size:11.5px}
.epaWrap{margin-left:auto;text-align:right;min-width:150px}
.epaNum{font-size:20px;font-weight:900;line-height:1}
.epaSub{font-size:10.5px;opacity:.8}
.bar{height:7px;border-radius:5px;background:rgba(255,255,255,.25);margin-top:5px;overflow:hidden}
.bar>i{display:block;height:100%;background:linear-gradient(90deg,#7fd6a6,#f4ad17)}
.cbody{padding:4px 18px 16px;display:none}
.card.open .cbody{display:block}
.arch{margin:12px 0 6px;font-size:14px;font-weight:800;color:var(--blue)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:10px;margin:8px 0 4px}
.sub{background:#f6f8fc;border:1px solid var(--line);border-radius:10px;padding:9px 12px}
.sub .k{font-size:10.5px;text-transform:uppercase;letter-spacing:.5px;color:var(--mut);font-weight:800}
.sub .v{font-size:13px;margin-top:2px}
.vis .k{color:var(--teal)}
.lessons{margin:10px 0 4px}
.lessons .h{font-size:11px;text-transform:uppercase;letter-spacing:.6px;color:var(--gold);font-weight:800;margin-bottom:5px}
.lessons ul{margin:0;padding-left:18px}.lessons li{font-size:13px;margin:3px 0}
.links{display:flex;flex-wrap:wrap;gap:7px;margin-top:11px;align-items:center}
.lk{font-size:11.5px;font-weight:700;text-decoration:none;padding:4px 10px;border-radius:7px;border:1px solid}
.t-cad{color:#0a7d44;border-color:#9bdab9;background:#e9f8f0}
.t-binder{color:#9a5b00;border-color:#f0c48a;background:#fdf2df}
.t-code{color:#5a3bb0;border-color:#cdbdf0;background:#f0ebfb}
.t-thread{color:#1f5fb0;border-color:#b8d2f0;background:#eaf2fc}
.t-dds{color:#7a1fb0;border-color:#dcb8f0;background:#f6eafc}
.t-video{color:#b02a37;border-color:#f0bcc2;background:#fceaec}
.t-stats,.t-site,.t-none{color:#566;border-color:#d6deea;background:#eef2f8}
.legend{display:flex;flex-wrap:wrap;gap:8px;font-size:11.5px;color:var(--mut);margin:6px 2px 0}
.sec{font-size:18px;font-weight:900;color:var(--navy);margin:26px 4px 4px}
.foot{color:var(--mut);font-size:12px;margin:18px 4px;line-height:1.6}
@media(max-width:640px){.epaWrap{min-width:96px}.trobot{display:none}}
</style></head><body><div class=wrap>
<header><h1>__DDTITLE__</h1>
<p>__SUB__</p></header>
<div class=over id=over></div>
<div class=controls>
<input id=q type=search placeholder="Search team, robot, mechanism, lesson, vision…">
<select id=arch><option value="">Archetype: all</option><option value=elevator>Elevator</option><option value=arm>Arm / pivot</option><option value=algae>Algae-capable</option><option value=ground>Ground intake</option><option value="deep climb">Deep climb</option></select>
<select id=cad><option value="">CAD: all</option><option value=cad>Onshape/GrabCAD</option><option value=binder>Tech binder</option><option value=code>Code only</option><option value=none>None public</option></select>
<div class=chip id=pick>★ Study picks</div>
<div class=count id=count></div></div>
<div class=legend>Link types:
<span class="lk t-cad">CAD</span><span class="lk t-binder">Tech binder</span><span class="lk t-code">Code</span><span class="lk t-thread">CD thread</span><span class="lk t-dds">DDS</span><span class="lk t-video">Video</span><span class="lk t-stats">Stats</span></div>
<div id=list></div>
<div class=sec>Additional well-documented robots for study</div>
<div id=bonuslist></div>
<div class=foot><b>Sources:</b> the <a href="https://cadcollection.spectrum3847.org">Spectrum 3847 CAD Collection</a> and team CAD releases (Onshape / GrabCAD), <a href="https://www.chiefdelphi.com">Chief Delphi</a> reveal / CAD-release threads, and <a href="https://www.statbotics.io">Statbotics</a> EPA &amp; records (2025 — EPA/rank backfilled once the API recovers). "Unconfirmed" = a detail was not publicly published, not that it is absent. This document is fully self-contained — all data is embedded. Built June 2026.</div>
</div>
<script>
const DATA=__J__, BONUS=__B__, MAX=__MAX__, OV=__OV__;
const PICKS=new Set(__PICKS__);
document.getElementById('over').innerHTML=OV.map((o,i)=>`<details ${i==0?'open':''}><summary>${o[0]}</summary><p>${o[1]}</p></details>`).join('');
function archMatch(a,f){a=(a||'').toLowerCase();if(!f)return true;if(f=='ground')return a.includes('ground')||a.includes('floor');if(f=='deep climb')return a.includes('deep climb')||a.includes('deep cage');return a.includes(f);}
function card(d){
  const pick=PICKS.has(d.team);
  const w=Math.round((d.epa||0)/MAX*100);
  const subs=[['Scoring (coral / algae)',d.shooter],['Intake',d.intake],['Elevator / lift',d.indexer],['Drivetrain',d.drivetrain]];
  const head = d.cad_url
    ? `<a class="lk t-${d.lt}" href="${d.cad_url}" target=_blank rel=noopener>${d.ltlabel}: ${d.cad_label} ↗</a>`
    : `<span class="lk t-${d.lt}">${d.cad_label}</span>`;
  const links=[head]
    .concat((d.src||[]).map(s=>`<a class="lk t-${s.t}" href="${s.url}" target=_blank rel=noopener>${s.label} ↗</a>`)).join('');
  return `<div class="card ${pick?'pick':''}" data-arch="${(d.archetype||'').toLowerCase()}" data-cad="${d.lt}" data-blob="${(d.team+' '+d.name+' '+d.robot+' '+d.archetype+' '+d.shooter+' '+d.intake+' '+d.indexer+' '+d.vision+' '+(d.lessons||[]).join(' ')+' '+d.region).toLowerCase().replace(/"/g,'')}" data-pick="${pick?1:0}">
   <div class=chead onclick="this.parentNode.classList.toggle('open')">
     <span class="rank ${pick?'gold':''}">${pick?'★ Study pick':'Profile'}</span>
     <div><div class=tnum>${d.team} <span class=tname>${d.name}</span> <span class=trobot>${d.robot||''}</span></div><div class=region>${d.region}</div></div>
     <div class=epaWrap><div class=epaNum>${d.epa||'—'}</div><div class=epaSub>${d.epa?('EPA · '+d.record):'EPA pending'}</div>${d.epa?`<div class=bar><i style="width:${w}%"></i></div>`:''}</div>
   </div>
   <div class=cbody>
     <div class=arch>${d.archetype}</div>
     <div class=grid>${subs.map(s=>`<div class=sub><div class=k>${s[0]}</div><div class=v>${s[1]}</div></div>`).join('')}
        <div class="sub vis"><div class=k>Vision</div><div class=v>${d.vision}</div></div></div>
     <div class=lessons><div class=h>Lessons for students</div><ul>${(d.lessons||[]).map(l=>`<li>${l}</li>`).join('')}</ul></div>
     <div class=links>${links}</div>
   </div></div>`;
}
document.getElementById('bonuslist').innerHTML=BONUS.map(card).join('');
function render(){
  const q=document.getElementById('q').value.toLowerCase(), af=document.getElementById('arch').value, cf=document.getElementById('cad').value, po=document.getElementById('pick').classList.contains('on');
  let n=0;
  document.querySelectorAll('#list .card').forEach(c=>{
    let ok=true;
    if(q&&!c.dataset.blob.includes(q))ok=false;
    if(af&&!archMatch(c.dataset.arch,af))ok=false;
    if(cf&&c.dataset.cad!=cf)ok=false;
    if(po&&c.dataset.pick!='1')ok=false;
    c.style.display=ok?'':'none'; if(ok)n++;
  });
  document.getElementById('count').textContent=n+' teams';
}
document.getElementById('list').innerHTML=DATA.map(card).join('');
['q','arch','cad'].forEach(id=>document.getElementById(id).addEventListener('input',render));
document.getElementById('pick').onclick=function(){this.classList.toggle('on');render();};
// open the study picks by default
document.querySelectorAll('#list .card.pick, #bonuslist .card.pick').forEach(c=>c.classList.add('open'));
render();
</script></body></html>"""

out=H.replace("__J__",J).replace("__B__",B).replace("__MAX__",str(MAX)).replace("__OV__",OV).replace("__SUB__",html.escape(META["subtitle"])).replace("__PICKS__",json.dumps(sorted(STUDY_PICKS)))
open(os.path.join(BASE, C.DEEPDIVE_HTML),"w").write(out.replace("__DDTITLE__", C.DEEPDIVE_TITLE))
print("html ok teams",len(data),"bonus",len(bonus))
