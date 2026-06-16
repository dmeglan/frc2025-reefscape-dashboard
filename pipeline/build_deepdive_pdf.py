from deepdive_data import TEAMS, BONUS, META, link_type, STUDY_PICKS
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, HRFlowable, PageBreak)
from reportlab.lib.enums import TA_LEFT
import html as H, os
import config as C
BASE = os.path.dirname(os.path.abspath(__file__))

NAVY=colors.HexColor("#16264a"); BLUE=colors.HexColor("#2e5496"); BLUE2=colors.HexColor("#3f72c4")
GOLD=colors.HexColor("#f4ad17"); INK=colors.HexColor("#1a2235"); MUT=colors.HexColor("#5b6678")
LINE=colors.HexColor("#d8e0ec"); BG=colors.HexColor("#f4f7fb"); GREEN=colors.HexColor("#1a9c5b")
TEAL=colors.HexColor("#0e7d7d"); LIGHT=colors.HexColor("#eef3fb")
PICKS=STUDY_PICKS

ss=getSampleStyleSheet()
def st(n,**k):
    base=k.pop("parent",ss["Normal"]); return ParagraphStyle(n,parent=base,**k)
H1=st("H1",fontName="Helvetica-Bold",fontSize=22,textColor=colors.white,leading=25)
SUB=st("SUB",fontName="Helvetica",fontSize=9.5,textColor=colors.HexColor("#dbe6f7"),leading=13)
SEC=st("SEC",fontName="Helvetica-Bold",fontSize=14,textColor=NAVY,spaceBefore=10,spaceAfter=4)
OVH=st("OVH",fontName="Helvetica-Bold",fontSize=10.5,textColor=BLUE,spaceBefore=5,spaceAfter=1)
OVB=st("OVB",fontName="Helvetica",fontSize=9.3,textColor=INK,leading=13,spaceAfter=3)
ARCH=st("ARCH",fontName="Helvetica-Bold",fontSize=10,textColor=BLUE,leading=12,spaceBefore=2,spaceAfter=2)
KEY=st("KEY",fontName="Helvetica-Bold",fontSize=6.8,textColor=MUT,leading=8)
VAL=st("VAL",fontName="Helvetica",fontSize=8.2,textColor=INK,leading=10)
VALV=st("VALV",fontName="Helvetica",fontSize=8.2,textColor=colors.HexColor("#0b5c5c"),leading=10)
LESH=st("LESH",fontName="Helvetica-Bold",fontSize=7,textColor=colors.HexColor("#9a6a00"),leading=9,spaceBefore=3)
LES=st("LES",fontName="Helvetica",fontSize=8.4,textColor=INK,leading=10.5,leftIndent=8,bulletIndent=0)
SRC=st("SRC",fontName="Helvetica",fontSize=7.2,textColor=BLUE,leading=9)
TH=st("TH",fontName="Helvetica-Bold",fontSize=7.3,textColor=colors.white,leading=8.5)
TD=st("TD",fontName="Helvetica",fontSize=7.3,textColor=INK,leading=8.6)
TDb=st("TDb",fontName="Helvetica-Bold",fontSize=7.3,textColor=NAVY,leading=8.6)

def esc(s): return H.escape(str(s))

story=[]

# ---------- Cover band ----------
cover=Table([[Paragraph(esc(META["title"]),H1)],
             [Paragraph(esc(META["subtitle"]),SUB)]],colWidths=[7.0*inch])
cover.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),NAVY),("LEFTPADDING",(0,0),(-1,-1),16),
    ("RIGHTPADDING",(0,0),(-1,-1),16),("TOPPADDING",(0,0),(0,0),16),("BOTTOMPADDING",(0,0),(0,0),3),
    ("TOPPADDING",(0,1),(0,1),0),("BOTTOMPADDING",(0,1),(0,1),14),("ROUNDEDCORNERS",[8,8,8,8])]))
story+=[cover,Spacer(1,10)]

# ---------- Overview ----------
story.append(Paragraph("The REEFSCAPE design landscape",SEC))
for h,b in META["overview"]:
    story.append(Paragraph(esc(h),OVH)); story.append(Paragraph(esc(b),OVB))
story.append(Spacer(1,6))

# ---------- Summary table ----------
story.append(Paragraph("Profiled robots at a glance",SEC))
hdr=["","Team","Robot","EPA","Rec","Archetype","Public CAD/Design"]
rows=[[Paragraph(h,TH) for h in hdr]]
def cadcell(t):
    lt,lab=link_type(t.get("cad_url",""),t.get("cad_label",""))
    return lab
for t in TEAMS:
    star="* " if t["team"] in PICKS else ""
    rows.append([Paragraph("&#9733;" if t["team"] in PICKS else "",TD),
        Paragraph(f"{t['team']} {esc(t['name'])}",TDb),
        Paragraph(esc(t["robot"]),TD),
        Paragraph(str(t["epa"]) if t["epa"] else "—",TDb),
        Paragraph(esc(t["record"]) or "—",TD),
        Paragraph(esc(t["archetype"][:62]),TD),
        Paragraph(esc(cadcell(t)),TD)])
tbl=Table(rows,colWidths=[0.3*inch,1.35*inch,1.05*inch,0.42*inch,0.5*inch,2.25*inch,1.43*inch],repeatRows=1)
sty=[("BACKGROUND",(0,0),(-1,0),BLUE),("VALIGN",(0,0),(-1,-1),"TOP"),
     ("LINEBELOW",(0,0),(-1,-1),0.4,LINE),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
     ("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4)]
for i,t in enumerate(TEAMS,1):
    if t["team"] in PICKS: sty.append(("BACKGROUND",(0,i),(-1,i),colors.HexColor("#fff6e0")))
    elif i%2==0: sty.append(("BACKGROUND",(0,i),(-1,i),LIGHT))
tbl.setStyle(TableStyle(sty)); story+=[tbl,Spacer(1,3)]
story.append(Paragraph("&#9733; = recommended study pick (downloadable CAD or a full technical binder + a clear design lesson). EPA / rank pending a Statbotics outage.",SRC))
story.append(PageBreak())

# ---------- Per-team cards ----------
LT_COLOR={"cad":GREEN,"binder":colors.HexColor("#9a5b00"),"code":colors.HexColor("#5a3bb0"),
 "thread":BLUE,"dds":colors.HexColor("#7a1fb0"),"video":colors.HexColor("#b02a37"),
 "stats":MUT,"site":MUT,"none":MUT}

def team_card(t, bonus=False):
    pick=t["team"] in PICKS
    rank="Profile"
    epatxt=(f'EPA {t["epa"]}' if t["epa"] else "EPA pending")
    rectxt=(esc(t["record"]) if t["epa"] else "")
    # header band
    head=Table([[Paragraph(f'<font color="white"><b>{rank}</b></font>',st("r",fontSize=8,leading=10)),
        Paragraph(f'<font color="white"><b>{t["team"]} {esc(t["name"])}</b>  <font size=7>{esc(t["robot"])}</font><br/><font size=6.5 color="#cfe0fa">{esc(t["region"])}</font></font>',st("hh",fontSize=11,leading=12)),
        Paragraph(f'<font color="white"><b>{epatxt}</b><br/><font size=7 color="#cfe0fa">{rectxt}</font></font>',st("e",fontSize=10,leading=12,alignment=2))]],
        colWidths=[0.6*inch,5.0*inch,1.4*inch])
    hc=GOLD if pick else NAVY
    htxt=colors.HexColor("#3a2c00") if pick else colors.white
    if pick:
        head=Table([[Paragraph(f'<b>&#9733; Study pick</b>',st("r2",fontSize=8,leading=10,textColor=colors.HexColor("#3a2c00"))),
            Paragraph(f'<b>{t["team"]} {esc(t["name"])}</b>  <font size=7>{esc(t["robot"])}</font><br/><font size=6.5>{esc(t["region"])}</font>',st("hh2",fontSize=11,leading=12,textColor=colors.HexColor("#3a2c00"))),
            Paragraph(f'<b>{epatxt}</b><br/><font size=7>{rectxt}</font>',st("e2",fontSize=10,leading=12,alignment=2,textColor=colors.HexColor("#3a2c00")))]],
            colWidths=[0.95*inch,4.65*inch,1.4*inch])
    head.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),hc),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
    flow=[head, Spacer(1,3), Paragraph(esc(t["archetype"]),ARCH)]
    # subsystem 2x2 + vision
    def cell(k,v,vis=False):
        return [Paragraph(k,KEY),Paragraph(esc(v),VALV if vis else VAL)]
    sg=Table([[cell("SCORING (CORAL / ALGAE)",t["shooter"]),cell("INTAKE",t["intake"])],
              [cell("ELEVATOR / LIFT",t["indexer"]),cell("DRIVETRAIN",t["drivetrain"])],
              [cell("VISION",t["vision"],True),cell("PUBLIC CAD / DESIGN",t["cad_label"])]],
             colWidths=[3.5*inch,3.5*inch])
    sg.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("BOX",(0,0),(-1,-1),0.5,LINE),
        ("INNERGRID",(0,0),(-1,-1),0.5,LINE),("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#f7f9fd")),
        ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]))
    flow+=[Spacer(1,3),sg,Spacer(1,3),Paragraph("LESSONS FOR STUDENTS",LESH)]
    for l in t.get("lessons",[]):
        flow.append(Paragraph(esc(l),LES,bulletText="•"))
    # links line
    parts=[f'<b>{esc(link_type(t.get("cad_url",""))[1])}:</b> <link href="{t.get("cad_url","")}"><font color="#1a7d44">{esc(t.get("cad_url","") or "n/a")}</font></link>'] if t.get("cad_url") else []
    for l,u in t.get("sources",[]):
        c=LT_COLOR.get(link_type(u)[0],BLUE).hexval()[2:]
        parts.append(f'<link href="{u}"><font color="#{c}">{esc(l)}</font></link>')
    flow.append(Spacer(1,2)); flow.append(Paragraph(" &nbsp;·&nbsp; ".join(parts),SRC))
    flow.append(Spacer(1,2)); flow.append(HRFlowable(width="100%",thickness=0.5,color=LINE,spaceBefore=2,spaceAfter=6))
    return KeepTogether(flow)

story.append(Paragraph("Team-by-team profiles",SEC))
for t in TEAMS:
    story.append(team_card(t))

story.append(PageBreak())
story.append(Paragraph("Additional well-documented robots for study",SEC))
story.append(Paragraph("Each has a strong public release (CAD, code, binder, or detailed reveal) and a clear design lesson. &#9733; marks the recommended study picks.",OVB))
for t in BONUS:
    story.append(team_card(t,bonus=True))

# footer note
story.append(Spacer(1,4))
story.append(Paragraph("<b>Sources:</b> the Spectrum 3847 CAD Collection and team CAD releases (Onshape, GrabCAD), Chief Delphi reveal / CAD-release threads, and Statbotics EPA & records (2025 — EPA/rank backfilled once the API recovers). \"Unconfirmed\" means a detail was not publicly published, not that it is absent.",SRC))

def deco(canvas,doc):
    canvas.saveState()
    canvas.setFont("Helvetica",7); canvas.setFillColor(MUT)
    canvas.drawString(0.6*inch,0.4*inch,C.DEEPDIVE_TITLE)
    canvas.drawRightString(7.9*inch,0.4*inch,f"Page {doc.page}")
    canvas.restoreState()

doc=SimpleDocTemplate(os.path.join(BASE, C.DEEPDIVE_PDF),
    pagesize=letter,leftMargin=0.55*inch,rightMargin=0.55*inch,topMargin=0.5*inch,bottomMargin=0.6*inch,
    title=C.DEEPDIVE_TITLE,author="Cowork research")
doc.build(story,onFirstPage=deco,onLaterPages=deco)
print("pdf ok")
