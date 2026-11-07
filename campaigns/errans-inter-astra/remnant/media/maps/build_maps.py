#!/usr/bin/env python3
"""REMNANT shipboard schematic generator. Self-contained SVGs with no scripts or external assets.

PROPOSED spatial layout only. The story-specific nodes and locks follow supplied GM guide v1.3.
Requires svgwrite, cairosvg and Pillow for preview. Generated files require no runtime deps.
"""
import math, os, re, html, copy
from pathlib import Path
from collections import namedtuple
import svgwrite
from PIL import Image, ImageOps, ImageDraw, ImageFont
import cairosvg

ROOT=Path(__file__).resolve().parent
S=ROOT/'scan_svg'; SP=ROOT/'scan_png'; E=ROOT/'encounter_svg'; EP=ROOT/'encounter_png'; PR=ROOT/'preview'
for p in (S,SP,E,EP,PR): p.mkdir(exist_ok=True)
C={
 'bg':'#06131e', 'bg2':'#091e2b','panel':'#0c2837','panel2':'#102f40','border':'#24506a',
 'grid':'#163b4d', 'grid2':'#0b2634','fg':'#e6f7fb','muted':'#88acbb','dim':'#547b8b',
 'cyan':'#66d5ee','cyan2':'#b8f3fb','amber':'#ffd16a','red':'#ff707c','green':'#8feda9',
 'pink':'#ee8ce0','blue':'#729ff9','purple':'#ac9efb', 'black':'#03101a',
}
FONT='DejaVu Sans, Liberation Sans, sans-serif'
MONO='DejaVu Sans Mono, Liberation Mono, monospace'


def new_svg(path,w,h,name):
 d=svgwrite.Drawing(str(path), size=(f'{w}px',f'{h}px'), viewBox=f'0 0 {w} {h}', profile='full')
 d.set_desc(title=name,desc='REMNANT navigation or tactical scan. Not-to-scale. Self-contained vector schematic.')
 d.add(d.rect(insert=(0,0),size=(w,h),fill=C['bg']))
 # fine & coarse grids: explicit lines for SVG portability and visual regularity
 for x in range(0,w+1,50): d.add(d.line((x,0),(x,h),stroke=C['grid2'],stroke_width=1,opacity=.30))
 for y in range(0,h+1,50): d.add(d.line((0,y),(w,y),stroke=C['grid2'],stroke_width=1,opacity=.30))
 for x in range(0,w+1,250): d.add(d.line((x,0),(x,h),stroke=C['grid'],stroke_width=1.6,opacity=.45))
 for y in range(0,h+1,250): d.add(d.line((0,y),(w,y),stroke=C['grid'],stroke_width=1.6,opacity=.45))
 return d

def rect(d,x,y,w,h,fill=None,stroke=None,sw=2,r=0,opacity=1,dash=None):
 q=d.rect(insert=(x,y),size=(w,h),rx=r,ry=r,fill=fill or 'none',stroke=stroke or 'none',stroke_width=sw,opacity=opacity)
 if dash:q.update({'stroke-dasharray':dash})
 d.add(q);return q

def line(d,points,color='cyan',sw=3,opacity=1,dash=None):
 p=d.polyline(points,fill='none',stroke=C.get(color,color),stroke_width=sw,stroke_linecap='round',stroke_linejoin='round',opacity=opacity)
 if dash:p.update({'stroke-dasharray':dash})
 d.add(p)

def circle(d,x,y,r,col='cyan',fill=None,sw=3,opacity=1):
 d.add(d.circle(center=(x,y),r=r,fill=fill if fill is not None else 'none',stroke=C.get(col,col),stroke_width=sw,opacity=opacity))

def tx(d,text,x,y,size=26,color='fg',weight=400,anchor='start',mono=False,letter=0):
 t=d.text(str(text), insert=(x,y), font_size=size,font_family=MONO if mono else FONT,font_weight=weight,
  fill=C.get(color,color),text_anchor=anchor)
 if letter:t.update({'letter-spacing':letter})
 d.add(t);return t

def path(d,pathstr,color='cyan',sw=3,opacity=1,dash=None):
 q=d.path(d=pathstr,fill='none',stroke=C.get(color,color),stroke_width=sw,opacity=opacity,
          stroke_linejoin='round',stroke_linecap='round')
 if dash:q.update({'stroke-dasharray':dash})
 d.add(q)

def hud(d,w,h,code,title,subtitle,classification='NAVIGATION / PLAYER SAFE',accent='cyan'):
 rect(d,50,38,w-100,152,fill=C['panel'],stroke=C['border'],sw=3,r=12)
 rect(d,50,38,13,152,fill=C[accent])
 tx(d,'ANDIS // REMNANT',85,88,24,'muted',700,mono=True,letter=2)
 tx(d,code,86,141,43,accent,700,mono=True)
 tx(d,title,500,110,49,'fg',700)
 tx(d,subtitle,503,151,21,'muted',400)
 tx(d,classification,w-100,87,22,'amber' if 'GM' in classification else 'green',700,'end',True)
 tx(d,'SENSOR-RECONSTRUCTION // NTS',w-100,148,19,'muted',400,'end',True)


def footer(d,w,h,detail='Proposed routing topology  |  schematic spacing does not indicate real distance.'):
 y=h-136
 rect(d,50,y,w-100,86,fill=C['panel'],stroke=C['border'],sw=2,r=8)
 # symbols legend
 line(d,[(85,y+32),(175,y+32)],'cyan',12)
 line(d,[(85,y+32),(175,y+32)],'cyan2',2,dash='8 12')
 tx(d,'MECH ROUTE',188,y+40,19,'fg',700,mono=True)
 line(d,[(455,y+32),(535,y+32)],'amber',4,dash='12 10')
 tx(d,'PILOT ROUTE',550,y+40,19,'fg',700,mono=True)
 rect(d,800,y+20,16,27,C['red'])
 tx(d,'ISOLATED / BLOCKED',832,y+40,19,'fg',700,mono=True)
 circle(d,1182,y+32,13,'green',C['panel'],3)
 tx(d,'ACCESS / LIFT',1212,y+40,19,'fg',700,mono=True)
 tx(d,detail,w-95,y+71,17,'muted',400,'end',True)


def field(d,x,y,w,h,code,accent='cyan'):
 rect(d,x,y,w,h,fill=C['panel'],stroke=C['border'],sw=3,r=14)
 rect(d,x,y,9,h,fill=C[accent],opacity=.78)
 tx(d,code,x+24,y+42,20,accent,700,mono=True,letter=1.1)


def big_stamp(d,x,y,title,sub='',accent='cyan'):
 # not a physical compartment; abstract section highlight
 rect(d,x,y,670,180,fill=C['panel2'],stroke=C[accent],sw=3,r=15,opacity=.84)
 rect(d,x+18,y+20,14,138,fill=C[accent],opacity=.8)
 tx(d,title,x+56,y+75,35,'fg',700)
 if sub: tx(d,sub,x+56,y+119,21,'muted',400,mono=True)


def rail(d,points,route='MECH',color='cyan',width=33):
 cc=C.get(color,color)
 # backbone, glowing side ribbons, repeated centerline
 line(d,points,cc,width+19,opacity=.10)
 line(d,points,'#144356',width+9,opacity=1)
 line(d,points,cc,width,opacity=.55)
 line(d,points,C['bg2'],width-11,opacity=1)
 line(d,points,'cyan2' if color=='cyan' else color,2.5,opacity=.85,dash='9 17')


def pilot(d,points):line(d,points,'amber',5,opacity=.85,dash='13 12')

def junction(d,x,y,accent='cyan',name=None):
 circle(d,x,y,22,accent,C['panel2'],4)
 circle(d,x,y,7,accent,C[accent],2)
 if name:tx(d,name,x,y-39,18,accent,700,'middle',True)

def block_gate(d,x,y,orientation='v',tag='GATE',col='amber'):
 if orientation=='v':
  rect(d,x-13,y-30,26,60,fill=C[col],stroke=C['bg'],sw=3)
  tx(d,tag,x,y-48,18,col,700,'middle',True)
 else:
  rect(d,x-30,y-13,60,26,fill=C[col],stroke=C['bg'],sw=3)
  tx(d,tag,x+54,y+8,18,col,700,mono=True)

def node(d,x,y,code,title,detail='',kind='normal',w=390,h=130):
 palette={'normal':'cyan','mission':'green','hazard':'amber','enemy':'red','rem':'pink','rhant':'green','remnant':'blue','optional':'muted','locked':'amber'}
 accent=palette.get(kind,kind); cc=C.get(accent,accent)
 x0=x-w/2; y0=y-h/2
 rect(d,x0,y0,w,h,fill=C['panel'],stroke=cc,sw=3,r=9)
 rect(d,x0+2,y0+2,8,h-4,fill=cc)
 tx(d,code,x0+26,y0+33,21,accent,700,mono=True)
 if len(title)>27:sz=24
 elif len(title)>21:sz=27
 else: sz=30
 tx(d,title,x0+26,y0+76,sz,'fg',700)
 if detail:tx(d,detail,x0+26,y0+107,17,'muted',400,mono=True)


def small_label(d,x,y,code,desc,accent='cyan',w=490):
 rect(d,x,y,w,72,fill=C['bg2'],stroke=C['border'],sw=2,r=6)
 rect(d,x+10,y+13,8,45,fill=C[accent])
 tx(d,code,x+33,y+29,16,accent,700,mono=True)
 tx(d,desc,x+33,y+55,20,'fg',600)

def corner_frame(d,x,y,w,h,accent='cyan'):
 for ax,ay,sgnx,sgny in [(x,y,1,1),(x+w,y,-1,1),(x,y+h,1,-1),(x+w,y+h,-1,-1)]:
  line(d,[(ax,ay+sgny*46),(ax,ay),(ax+sgnx*46,ay)],accent,4,opacity=.65)


def scale_bar(d,x,y,w=870):
 tx(d,'RELATIVE TRANSIT SEGMENTS / NO DISTANCE IMPLIED',x,y-23,18,'muted',700,mono=True)
 line(d,[(x,y),(x+w,y)],'dim',3)
 for i in range(17):
  xx=x+w*i/16
  line(d,[(xx,y-9),(xx,y+9)],'dim',2)


def sector_art(d,w,h,kind):
 """Decorative, anonymous infrastructure motifs. Not drawn to measured scale."""
 x0=110;y0=260;W=w-220;H=h-440
 rect(d,x0,y0,W,H,fill=C['bg2'],stroke=C['border'],sw=2,r=10)
 for i in range(12):
  x=x0+85+i*(W-170)/12
  rect(d,x,y0+24,154,26,fill=C['panel'],stroke=C['border'],sw=1,opacity=.55)
  rect(d,x,y0+H-54,154,26,fill=C['panel'],stroke=C['border'],sw=1,opacity=.55)
  if i%3==0:tx(d,f'FRAME-{i+1:02d}',x+4,y0+90,16,'dim',700,mono=True)
 for q in range(3):
  cx=x0+450+900*q
  circle(d,cx,y0+H/2,260,'border',sw=2,opacity=.22)
  circle(d,cx,y0+H/2,205,'border',sw=1,opacity=.16)
 if kind=='lance':
  cx=w*0.58;cy=y0+H*.52
  for r in [90,155,230,320]:
   circle(d,cx,cy,r,'blue',sw=3,opacity=.14)
 if kind=='cargo':
  for i in range(12):
   x=320+i*230
   rect(d,x,470,180,370,fill='none',stroke=C['border'],sw=2,opacity=.18)


def make_master(safe=False):
 w,h=3200,1650
 fn='00_MASTER_PLAYER_SCAN.svg' if safe else '00_MASTER_ROUTE_NETWORK.svg'
 d=new_svg(S/fn,w,h,'REMNANT master route network')
 hud(d,w,h,'M-00','PROXIMA PRIME // SECTOR NETWORK','Two independent vessels. Connections represent access, not deck geometry.',classification='NAVIGATION / PLAYER DISPLAY' if safe else 'GM PLANNING / CONTAINS SPOILERS',accent='blue')
 field(d,115,235,2980,510,'PCV-L  DEIMOS // ATTACHED AT PROXIMA NOSE','green')
 field(d,115,780,2980,680,'PCV-EN PROXIMA // MICHEL NEY DREADNOUGHT','pink')
 tx(d,'D-AXIS / PROPOSED',265,318,19,'muted',700,mono=True)
 tx(d,'P-AXIS / PROPOSED',265,864,19,'muted',700,mono=True)
 # route graph under nodes
 rail(d,[(1120,520),(1740,520),(2670,520)],color='green')
 rail(d,[(380,1050),(1050,1050),(2100,1050),(2690,1050)])
 rail(d,[(1050,1050),(1050,520),(1120,520)],color='cyan')
 rail(d,[(1050,1050),(1430,1293)],color='cyan')
 rail(d,[(2100,1050),(2240,1293)],color='cyan')
 rail(d,[(1740,520),(1930,663)],color='green')
 pilot(d,[(480,1125),(640,1316)])
 # nodes: same graph but no encounter, casket, or prototype spoilers on player maps
 if safe:
  node(d,380,1050,'P-01','SERVICE HANGAR','External maintenance entry',kind='normal',w=405)
  node(d,1050,1050,'P-02','TRANSIT SPINE','Primary mech artery',w=412)
  node(d,2100,1050,'P-04','ENGINEERING','Restricted sector',kind='normal',w=420)
  node(d,2690,1050,'P-05','SUPPORT / FAB','Repair infrastructure',kind='normal',w=445)
  node(d,1430,1293,'P-03','CARGO TRANSFER','Freight transit galleries',kind='normal',w=420)
  node(d,2240,1293,'P-06','SECURE SYSTEMS','Restricted local access',kind='optional',w=432)
  node(d,1120,520,'D-01','DOCKING SPINE','Emergency safety control',kind='normal',w=430)
  node(d,1740,520,'D-02','WEAPONS ACCESS','Restricted compartments',kind='normal',w=415)
  node(d,2670,520,'D-03','RESEARCH BAY','Classified installation',kind='normal',w=390)
  node(d,1930,663,'D-04','SECURE SYSTEMS','Local service cabinet',kind='optional',w=398,h=112)
 else:
  node(d,380,1050,'P-01','SERVICE HANGAR','Initial mech boarding',kind='mission',w=405)
  node(d,1050,1050,'P-02','TRANSIT SPINE','Primary mech artery',w=412)
  node(d,2100,1050,'P-04','ENGINEERING','Lock 2 / Kraven',kind='mission',w=420)
  node(d,2690,1050,'P-05','SUPPORT / PRINTER','Prepare for finale',kind='mission',w=445)
  node(d,1430,1293,'P-03','CARGO TRANSFER','Optional pirate scene',kind='enemy',w=420)
  node(d,2240,1293,'P-06','REM CASKET ACCESS','Manual cycle if needed',kind='rem',w=432)
  node(d,1120,520,'D-01','DOCKING INTERLOCK','Lock 1 / hardwired',kind='mission',w=430)
  node(d,1740,520,'D-02','WEAPONS ACCESS','RHANT cabinet branch',kind='rhant',w=415)
  node(d,2670,520,'D-03','LANCE BAY','Lock 3 / final battle',kind='mission',w=390)
  node(d,1930,663,'D-04','RHANT CASKET','Manual cycle if needed',kind='rhant',w=398,h=112)
 small_label(d,260,1332,'OPTIONAL','MED / CREW SUPPORT',accent='cyan',w=435)
 if not safe:tx(d,'RETURN TO D-03 VIA D-01 AFTER ENGINEERING',1540,940,20,'amber',700,'middle',True)
 # outline transfer seam only
 line(d,[(770,766),(1400,766)],'blue',2,dash='12 15')
 tx(d,'HARD DOCKING COUPLER',1130,762,17,'blue',700,'middle',True)
 # header & footer custom
 tx(d,'LINKED VESSELS  /  SELECT A SECTOR FOR LOCAL SCAN',250,1531,26,'fg',700,mono=True) if safe else tx(d,'PRIMARY PLAY ROUTE  P-01 > P-02 > D-01 > P-04 > P-05 > D-03',250,1531,26,'fg',700,mono=True)
 tx(d,'P-03 / P-06 / D-04  :  SUBSYSTEM BRANCHES' if safe else 'P-03 OPTIONAL  /  P-06 + D-04 CONDITIONAL',2950,1531,19,'muted',700,'end',True)
 tx(d,'SCANNED FUNCTIONAL BANDS / CORRIDOR LENGTHS NOT TO SCALE' if safe else 'GM DESIGN NOTE: FUNCTIONAL BANDS, NOT ACTUAL DECK NUMBERS. ALL CORRIDOR LENGTHS UNMEASURED.',1600,1608,18,'amber',700,'middle',True)
 d.save()


# route stage geometry. Nodes are [x,y,code,title,detail,kind,w].
SECTORS=[
 dict(code='P-01',title='OUTER ACCESS / SERVICE HANGAR',ship='PROXIMA',kind='access',
      note='Initial boarding through the damaged maintenance lock. Hangar doors and environmental integrity are unreliable.',
      rails=[[(180,700),(3040,700)],[(480,1020),(1720,1020),(1720,700)]],
      pilots=[[(480,700),(480,1020),(990,1020)]],
      nodes=[(390,700,'ENTRY-01','MAINTENANCE LOCK','MECH / EVA','mission',430),(1170,700,'ACCESS-02','PRESSURE VESTIBULE','Damaged seal / risk','hazard',435),(2220,700,'LINK-P02','TRANSIT GATE','To P-02 / main spine','mission',425),(1080,1020,'PILOT-01','CREW ACCESS','Pilot-only side route','optional',430)],
      gates=[(1670,700,'A-12','amber'),(2690,700,'P02','green')],
      labels=[(170,345,'SVC HANGAR // LARGE VOID'),(170,400,'Gantries • service trains • pressure compartments'),(1600,1120,'DARK HANGAR WING // NO NETWORKED ASSUMPTIONS')],
      stamp=('BAY PRESSURE','UNSTABLE / CHECK BEFORE OPENING','amber')),
 dict(code='P-02',title='TRANSIT SPINE / INTERNAL LOGISTICS',ship='PROXIMA',kind='transit',
      note='The main mech-capable transit network. Navigation overlays can contradict real doors; visible hard landmarks remain reliable.',
      rails=[[(190,590),(3020,590)],[(190,830),(3020,830)],[(860,590),(860,830)],[(1820,590),(1820,1010)]],
      pilots=[[(860,830),(1110,1040),(1800,1040)]],
      nodes=[(385,590,'FROM-P01','HANGAR TRANSIT','Ingress from P-01','mission',440),(1260,590,'JCT-14','TRANSFER JUNCTION','AR maps inconsistent','hazard',445),(2435,590,'TO-P04','ENGINEERING LINE','To central engineering','mission',450),
             (700,830,'D01-LINK','NOSE TRANSFER LIFT','To Deimos D-01','mission',470),(1850,830,'CARGO-LINK','FREIGHT SPUR','To cargo gallery P-03','optional',445),(2470,830,'SUPPORT','FABRICATION SPUR','To P-05 printer','optional',425)],
      gates=[(1730,590,'B-08','amber'),(2750,830,'G-11','amber')],
      labels=[(230,360,'TRANSIT TRUNK // MECH-CAPABLE'),(1650,370,'REFERENCE: SERVICE TRAIN / HEAVY BULKHEADS'),(1000,1120,'UNRELIABLE AR ROUTING  /  PHYSICAL ROUTE MARKERS REMAIN VALID')],
      stamp=('SENSOR CONFLICT','TWO EXCLUSIVE ROUTE OVERLAYS','amber')),
 dict(code='P-03',title='CARGO TRANSFER / SALVAGE SPUR',ship='PROXIMA',kind='cargo',
      note='Independent pirate salvage confrontation. Intercepting the hauler is optional, and losing it does not lock campaign progress.',
      rails=[[(195,660),(3040,660)],[(510,950),(2700,950)],[(640,660),(640,950)],[(2720,950),(2720,660)]],
      pilots=[[(1120,950),(1430,1070),(1920,1070)]],
      nodes=[(410,660,'FROM-P02','SERVICE LIFT','Lancers arrive from west','mission',430),(1210,660,'CARGO-04','TRANSFER GALLERY','Pirate / hauler corridor','enemy',465),(2130,660,'HAULER','SALVAGE TRACK','Escape attempt east','enemy',435),(2840,660,'EXIT-09','ESCAPE AIRLOCK','Pirate departure point','hazard',420),
             (1670,950,'BYPASS','UTILITY GANTRY','Pilot-only alternate','optional',430)],
      gates=[(1770,660,'F-15','amber')],
      labels=[(200,360,'SIX-ROUND SALVAGE CLOCK // IF COMBAT'),(700,1190,'SERVICES / CARGO STACKS ABSTRACTED; TACTICAL SCAN E-02 PROVIDES HEX FIELD')],
      stamp=('SALVAGE ACTIVITY','UNAUTHORIZED FREIGHT TRANSFER','red')),
 dict(code='P-04',title='CENTRAL ENGINEERING / TRANSIT BAY',ship='PROXIMA',kind='engineering',
      note='Hell’s Kraven GAUNTLET. Western deployment, eastern control enclosure; protect the Lock 2 hardwired safety console.',
      rails=[[(190,760),(3040,760)],[(710,470),(2320,470)],[(710,1040),(2320,1040)],[(1060,470),(1060,760)],[(2140,470),(2140,1040)]],
      pilots=[[(2700,760),(2700,1080),(2950,1080)]],
      nodes=[(385,760,'FROM-P02','WEST TRANSIT','PC arrival / ADZ','mission',425),(1260,760,'ENG-BAY','CENTRAL TRANSIT BAY','Kraven contested / CZ east','enemy',465),(2420,760,'LOCK-2','SAFETY CONTROL','Hardwired power/casket cycle','mission',490),
             (1190,470,'ING-N','NORTH INGRESS','Reinforcement access','hazard',430),(1190,1040,'ING-S','SOUTH INGRESS','Reinforcement access','hazard',430),(2690,1070,'REM-CASKET','LOCAL CASKET LINK','P-06 / if manual cycle','rem',430)],
      gates=[(1860,760,'E-17','amber')],
      labels=[(260,353,'CORE ACCESS / REACTOR SERVICE'),(1720,352,'UPPER+LOWER INGRESS // MULTIPLE ACCESS LANES'),(1550,1157,'TACTICAL HEX FIELD: E-01 // DO NOT PLACE CONSOLE IN OPEN CROSS-FIRE')],
      stamp=('CORE SAFETY','AUTHORIZED ISOLATION AFTER LOCK 1','amber')),
 dict(code='P-05',title='SUPPORT / FABRICATION / MEDICAL',ship='PROXIMA',kind='support',
      note='Ship printer repair and pre-final preparation are campaign beats. Medical and crew support are proposed atmosphere branches.',
      rails=[[(200,650),(3050,650)],[(790,970),(2460,970)],[(760,650),(760,970)],[(2470,650),(2470,970)]],
      pilots=[[(1980,970),(2700,1100)]],
      nodes=[(410,650,'FROM-P02','SERVICE TRANSFER','From transit / engineering','mission',450),(1340,650,'PRINTER','SHIP FABRICATOR','Repair / preparation beat','mission',460),(2460,650,'RETURN','NOSE ROUTE','Back toward D-01 / D-03','mission',455),
             (1080,970,'MED-01','MEDICAL BAY','Optional location marker','optional',430),(2040,970,'SUP-02','CREW SERVICES','Optional / ghost sightings','optional',460)],
      gates=[(1950,650,'M-06','amber')],
      labels=[(190,345,'FIELD SERVICE / SUPPORT BAND'),(1020,1175,'PLACEHOLDER IMAGE MARKERS: MED BAY / FABRICATION / CREW SUPPORT')],
      stamp=('FABRICATION','REPAIR PRINTER BEFORE FINAL BATTLE','green')),
 dict(code='D-01',title='DOCKING SPINE / ISOLATION INTERLOCK',ship='DEIMOS',kind='dock',
      note='Lock 1 physically disconnects the automatic legionspace coupler. It is air-gapped; REMNANT cannot activate it remotely.',
      rails=[[(190,710),(3050,710)],[(860,990),(2250,990)],[(860,710),(860,990)],[(2250,710),(2250,990)]],
      pilots=[[(1200,710),(1410,1080),(1900,1080)]],
      nodes=[(400,710,'FROM-P02','NOSE DOCK TRANSFER','From Proxima', 'mission',455),(1210,710,'LOCK-1','ISOLATION INTERLOCK','Manual / non-networked','mission',470),(2080,710,'COUPLER','DOCKING COUPLER','Staged separation link','hazard',455),(2840,710,'TO-D02','DEIMOS TRANSIT','Toward weapon access','mission',425),
             (1550,990,'SERVICE','SAFETY CRAWLSPACE','Pilot-only maintenance','optional',470)],
      gates=[(1730,710,'H-01','amber'),(2460,710,'D-02','green')],
      labels=[(235,355,'TWO HULLS / ONE DOCKING ASSEMBLY'),(1160,1170,'LOCK 1 ARMS DISCONNECT; IT DOES NOT SPLIT REMNANT')],
      stamp=('PHYSICAL INTERLOCK','OFF-NET / AIR-GAPPED','green')),
 dict(code='D-02',title='WEAPONS ACCESS / RHANT SUPPORT',ship='DEIMOS',kind='weapons',
      note='Service transit between docking spine, RHANT’s casket cabinet, and the Co-Consciousness Lance bay.',
      rails=[[(190,620),(3050,620)],[(610,955),(2560,955)],[(800,620),(800,955)],[(2390,620),(2390,955)]],
      pilots=[[(1690,955),(1870,1070),(2340,1070)]],
      nodes=[(410,620,'FROM-D01','DOCKING TRANSFER','From physical interlock','mission',455),(1400,620,'WEAPONS','ARMORED ACCESS TRUNK','Mech capable','normal',480),(2650,620,'TO-D03','LANCE BAY GATE','Final encounter access','mission',445),
             (1120,955,'D-04','RHANT CASKET CABINET','Manual cycle if necessary','rhant',490),(2110,955,'SVC-12','COUNTERMEASURES','Support maintenance / proposed','optional',450)],
      gates=[(2090,620,'L-18','amber')],
      labels=[(190,346,'DEIMOS IS A DETACHABLE FRIGATE / NOT A CORRIDOR ON PROXIMA'),(1100,1190,'RHANT CASKET EXISTS ON DEIMOS; ACCESS ROUTE SHOWN PROVISIONALLY')],
      stamp=('WEAPON SYSTEMS','LANCE BAY AHEAD','amber')),
 dict(code='D-03',title='CO-CONSCIOUSNESS LANCE BAY',ship='DEIMOS',kind='lance',
      note='Finale in the prototype bay. The seam and crew phase anomalies are present; the enemy is not named on player scans.',
      rails=[[(190,735),(3040,735)],[(1330,445),(2470,445)],[(1330,1035),(2470,1035)],[(1510,445),(1510,1035)],[(2460,445),(2460,1035)]],
      pilots=[[(650,735),(650,1060),(1150,1060)]],
      nodes=[(410,735,'FROM-D02','PRESSURE ENTRY','Sealed approach / mech','mission',440),(1590,735,'LANCE-CORE','EXPERIMENTAL BAY','Lock 3 / central chamber','mission',495),(2750,735,'EVAC-02','RETREAT ACCESS','Emergency route / GM choice','hazard',445)],
      gates=[(990,735,'L-99','amber')],
      labels=[(205,354,'TEMPORAL DRIFT / SEAM ECHOES'),(1210,1150,'FINAL ENCOUNTER HEX FIELD: E-03 // BODY CENTERED; CELLS 8 HEXES OUT')],
      stamp=('LANCE CAPACITY','TEMPORAL ANOMALY / INVESTIGATE','blue')),
]


def make_sector(spec,safe=False):
 w,h=3200,1460; code=spec['code']; d=new_svg(S/f"{code}_{'PLAYER' if safe else 'SECTOR'}_SCAN.svg",w,h,code)
 col='pink' if code[0]=='P' else 'green'
 hud(d,w,h,code,spec['title'],f"{spec['ship']} // functional band // conceptual not-to-scale scan",classification='NAVIGATION / PLAYER DISPLAY' if safe else 'GM PLANNING / CONTAINS SPOILERS',accent=col)
 sector_art(d,w,h,spec['kind'])
 for points in spec['rails']:rail(d,points,color='cyan' if code[0]=='P' else 'green')
 for points in spec['pilots']:pilot(d,points)
 for x,y,g,c in spec['gates']:block_gate(d,x,y,tag=g,col=c)
 for x,y,n,title,detail,kind,width in spec['nodes']:node(d,x,y,n,title,detail,kind,w=width)
 for x,y,t in spec['labels']:
  tx(d,t,x,y,20,'muted',700,mono=True)
 # status stamp at upper right inside viewport; header y<200
 a,b,c=spec['stamp']
 sx=2330;sy=315
 rect(d,sx,sy,680,120,fill=C['panel2'],stroke=C[c],sw=3,r=8)
 tx(d,a,sx+24,sy+45,24,c,700,mono=True)
 tx(d,b,sx+24,sy+85,18,'fg',700,mono=True)
 # connectivity info & scan serial
 rect(d,115,1215,2960,70,fill=C['panel'],stroke=C['border'],sw=1,r=8)
 tx(d,spec['note'],145,1258,20,'fg')
 footer(d,w,h,'SPECULATIVE LINK POSITIONS  /  CONFIRMED STORY LOCATIONS LABELED')
 d.save()

# HEX ENCOUTER GENERATION
HEX_SIZE=31
HEX_W=math.sqrt(3)*HEX_SIZE
HEX_STEP_Y=1.5*HEX_SIZE

def oddr_to_ax(c,r):return c-(r-(r&1))//2,r

def ax_to_oddr(q,r):return q+(r-(r&1))//2,r

def hex_dist(a,b):
 q1,r1=oddr_to_ax(*a);q2,r2=oddr_to_ax(*b)
 dq=q1-q2;dr=r1-r2
 return max(abs(dq),abs(dr),abs(dq+dr))

def hxy(c,r,ox,oy,s=HEX_SIZE):return ox+math.sqrt(3)*s*(c+0.5*(r&1)),oy+1.5*s*r

def hex_path(x,y,s):
 pts=[(x+s*math.cos(math.radians(-90+60*k)),y+s*math.sin(math.radians(-90+60*k))) for k in range(6)]
 return pts

def draw_hex(d,x,y,s,fill=C['panel'],stroke='#32637b',sw=1.5,opacity=1):
 d.add(d.polygon(hex_path(x,y,s),fill=fill,stroke=stroke,stroke_width=sw,opacity=opacity))

def encounter_base(code,title,subtitle,ncols,nrows,gm=True):
 w,h=3200,1650;d=new_svg(E/f'{code}.svg',w,h,title)
 hud(d,w,h,code,title,subtitle,classification='TACTICAL REFERENCE / GM USE ONLY' if gm else 'PLAYER SCAN / NO SPOILERS',accent='amber')
 # map field can fit 29x21 with 31 hex radius => width 1600 and height 980
 boxx=80;boxy=265;boxw=2020;boxh=1115
 rect(d,boxx,boxy,boxw,boxh,fill=C['bg2'],stroke=C['border'],sw=3,r=13)
 ox=160;oy=boxy+110
 for r in range(nrows):
  for c in range(ncols):
   x,y=hxy(c,r,ox,oy)
   draw_hex(d,x,y,HEX_SIZE,fill='#0f2d40',stroke='#3d6c81',sw=1.2,opacity=.92)
  if r%4==0:tx(d,str(r).zfill(2),95,oy+HEX_STEP_Y*r+8,17,'muted',700,mono=True)
 for c in range(0,ncols,4):
  x,y=hxy(c,0,ox,oy)
  tx(d,str(c).zfill(2),x,boxy+47,17,'muted',700,'middle',True)
 # Right rail
 x=2130
 rect(d,x,265,985,1115,fill=C['panel'],stroke=C['border'],sw=3,r=13)
 tx(d,'AREA SCAN // OBJECTIVES',x+48,322,28,'fg',700,mono=True)
 line(d,[(x+42,348),(x+945,348)],'border',2)
 return d,ox,oy,w,h

def tint_cell(d,c,r,ox,oy,color,alpha=.5,mark=None):
 x,y=hxy(c,r,ox,oy)
 draw_hex(d,x,y,HEX_SIZE,fill=C[color],stroke=C[color],sw=1,opacity=alpha)
 if mark:tx(d,mark,x,y+7,16,C['bg'],700,'middle',True)

def arrow(d,pts,color='cyan'):
 line(d,pts,color,6)
 if len(pts)>=2:
  (x1,y1),(x2,y2)=pts[-2:];theta=math.atan2(y2-y1,x2-x1)
  al=21;ang=.53
  p1=(x2-al*math.cos(theta-ang),y2-al*math.sin(theta-ang))
  p2=(x2-al*math.cos(theta+ang),y2-al*math.sin(theta+ang))
  d.add(d.polygon([p1,(x2,y2),p2],fill=C[color]))

def sidebar(d,lines,foot):
 x=2175;y=420
 for i,(heading,value,col) in enumerate(lines):
  yy=y+i*142
  rect(d,x,yy,875,119,fill=C['bg2'],stroke=C['border'],sw=1.8,r=10)
  rect(d,x+15,yy+17,9,84,fill=C[col])
  tx(d,heading,x+45,yy+43,23,col,700,mono=True)
  for j,txt in enumerate(value if isinstance(value,list) else [value]):
   tx(d,txt,x+45,yy+78+j*22,18,'fg',400,mono=True)
 tx(d,foot,2160,1300,17,'amber',700,mono=True)

def safe_spec(spec):
 a=copy.deepcopy(spec)
 code=a['code']
 # Restrict exact GM lock, combat, NHP and final encounter information to GM version.
 changes={
 'P-01':{'note':'Damaged service hangar with environmental disruption. Validate pressure doors locally before transfer.',
         'labels':[(170,345,'SVC HANGAR // LARGE VOID'),(170,400,'Gantries / service trains / pressure compartments')],
         'stamp':('BAY PRESSURE','UNSTABLE / CHECK BEFORE OPENING','amber')},
 'P-02':{'note':'Mech-scale logistics trunk with unreliable AR routing; verify paths using hardwired visual indicators.',
         'labels':[(230,360,'TRANSIT TRUNK // MECH CAPABLE'),(1000,1120,'AR LABELS INCONSISTENT / PHYSICAL ROUTE MARKERS RELIABLE')],
         'stamp':('SENSOR CONFLICT','TWO ROUTE OVERLAYS DISAGREE','amber')},
 'P-03':{'title':'CARGO TRANSFER / FREIGHT GALLERIES',
         'note':'Wide cargo galleries with service lifts, freight tracks, gantries, and a dockside airlock.',
         'labels':[(200,360,'TRANSFER TRACKS / CARGO ACTIVITY DETECTED')],
         'stamp':('FREIGHT TRANSIT','UNIDENTIFIED EQUIPMENT MOVEMENT','amber')},
 'P-04':{'title':'CENTRAL ENGINEERING / TRANSIT BAY',
         'note':'Engineering access, high-capacity machinery, layered transit decks, and restricted safety controls.',
         'labels':[(260,353,'CORE ACCESS / REACTOR SERVICE'),(1720,352,'UPPER AND LOWER ACCESS GALLERIES')],
         'stamp':('CORE SAFETY','RESTRICTED CONTROL ENCLOSURE','amber')},
 'P-05':{'title':'SUPPORT / FABRICATION / MEDICAL',
         'note':'Ship fabrication, clinical support, crew services, and diagnostic transfer links.',
         'labels':[(190,345,'FIELD SERVICE / SUPPORT BAND')],
         'stamp':('FABRICATION','DEVICE STATUS UNKNOWN','amber')},
 'D-01':{'title':'DOCKING SPINE / SAFETY SYSTEMS',
         'note':'Heavy docking assembly joins Deimos to the forward end of Proxima. Emergency systems are locally controlled.',
         'labels':[(235,355,'TWO HULLS / ONE DOCKING ASSEMBLY')],
         'stamp':('EMERGENCY ISOLATION','LOCAL CONTROL / OFF-NET','amber')},
 'D-02':{'title':'WEAPONS ACCESS / SECURE SYSTEMS',
         'note':'Restricted weapons service trunk. Core-system maintenance remains isolated from remote access.',
         'labels':[(190,346,'DEIMOS / DETACHABLE FRIGATE')],
         'stamp':('WEAPON SYSTEMS','RESTRICTED ACCESS','amber')},
 'D-03':{'title':'RESEARCH CHAMBER / EXPERIMENTAL SYSTEMS',
         'note':'Large research chamber exhibits intermittent energy peaks and unexplained timing discrepancies.',
         'labels':[(205,354,'LOCAL TIMING ANOMALY / INCOMPLETE SENSOR DATA')],
         'stamp':('RESEARCH SYSTEMS','UNREGISTERED ENERGY FLUX','amber')}
 }
 for key,val in changes[code].items():a[key]=val
 replacements={
 'P-01':{'nodes':{ 'ENTRY-01':('MAINTENANCE LOCK','MECH / EVA','normal'),'ACCESS-02':('PRESSURE VESTIBULE','Damaged seal / risk','hazard'),'LINK-P02':('TRANSIT GATE','To P-02 main spine','normal')}},
 'P-02':{'nodes':{'JCT-14':('TRANSFER JUNCTION','AR routes inconsistent','hazard')}},
 'P-03':{'nodes':{'CARGO-04':('TRANSFER GALLERY','Cargo movement observed','normal'),'HAULER':('FREIGHT TRACK','Bulk transfer lane','normal'),'EXIT-09':('EXTERNAL AIRLOCK','Sealed cargo airlock','hazard')}},
 'P-04':{'nodes':{'FROM-P02':('WEST TRANSIT','Access from P-02','normal'),'ENG-BAY':('CENTRAL TRANSIT BAY','Heavy machinery access','normal'),'LOCK-2':('SAFETY ENCLOSURE','Restricted controls','hazard'),'ING-N':('NORTH SERVICE GALLERY','Upper cross-access','normal'),'ING-S':('SOUTH SERVICE GALLERY','Lower cross-access','normal'),'REM-CASKET':('RESTRICTED CORE ACCESS','Local system cabinet','optional')}},
 'P-05':{'nodes':{'PRINTER':('SHIP FABRICATOR','Local repair platform','normal'),'RETURN':('NOSE ROUTE','Toward docking assembly','normal'),'SUP-02':('CREW SERVICES','Auxiliary compartments','optional')}},
 'D-01':{'nodes':{'LOCK-1':('SAFETY INTERLOCK','Manual isolation controls','hazard'),'COUPLER':('DOCKING COUPLER','Local junction','normal'),'TO-D02':('DEIMOS TRANSIT','Weapons access trunk','normal')}},
 'D-02':{'nodes':{'FROM-D01':('DOCKING TRANSFER','From docking spine','normal'),'WEAPONS':('ARMORED ACCESS TRUNK','Restricted sector','normal'),'TO-D03':('RESEARCH BAY GATE','Experimental systems','normal'),'D-04':('SECURE CORE CABINET','Authorized service only','optional')}},
 'D-03':{'nodes':{'FROM-D02':('PRESSURE ENTRY','Sealed approach / mech','normal'),'LANCE-CORE':('EXPERIMENTAL CHAMBER','Power source uncertain','hazard'),'EVAC-02':('EMERGENCY ACCESS','Auxiliary return route','normal')}}
 }
 for i,n in enumerate(a['nodes']):
  replacement=replacements.get(code,{}).get('nodes',{}).get(n[2])
  if replacement:
   title,detail,kind=replacement
   safe_id={('P-03','HAULER'):'TRACK-07',('P-04','LOCK-2'):'CTRL-02',('P-04','REM-CASKET'):'CORE-12',('D-01','LOCK-1'):'SAFE-01',('D-03','LANCE-CORE'):'RES-01'}.get((code,n[2]),n[2])
   a['nodes'][i]=(n[0],n[1],safe_id,title,detail,kind,n[6])
 return a


def make_gauntlet():
 code='E-01_GAUNTLET'; d,ox,oy,w,h=encounter_base(code,'CENTRAL ENGINEERING / GAUNTLET','26 x 16 hex fields // illustrative deployment and abstract cover, not a detailed room plan',26,16)
 # west deploy r3..12,c0..2; east c20..25,r3..12
 for r in range(3,13):
  for c in range(0,3):tint_cell(d,c,r,ox,oy,'cyan',.48)
  for c in range(20,26):tint_cell(d,c,r,ox,oy,'red',.45)
 # top bottom ingress
 for r in [0,1,14,15]:
  for c in [5,6,7,8,16,17,18,19]:tint_cell(d,c,r,ox,oy,'amber',.5)
 # abstract cover, avoid two main lanes at r4/5 and 10/11
 for c,r in [(9,7),(10,7),(10,8),(13,7),(14,7),(15,7),(15,8),(16,8),(18,8),(19,7),(21,7),(22,7),(22,8),(23,6),(23,9),(11,12),(14,12)]:
  if not (c>=20 and 3<=r<=12):tint_cell(d,c,r,ox,oy,'purple',.45,'▥')
 # east CZ border highlights and western marker
 tx(d,'ADZ',*[(hxy(1,8,ox,oy)[0]),hxy(1,8,ox,oy)[1]+12],40,'fg',700,'middle',True)
 tx(d,'CZ',hxy(22,8,ox,oy)[0],hxy(22,8,ox,oy)[1]+15,47,'fg',700,'middle',True)
 sidebar(d,[('PLAYER DEPLOYMENT',['WEST / LEFT EDGE','Keep the approach mech-accessible'],'cyan'),
  ('ENEMY CONTROL ZONE',['EAST / RIGHT EDGE','Fortified objective / Lock 2'],'red'),
  ('INGRESS ZONES',['2 NORTH + 2 SOUTH','Held units arrive end of round 1'],'amber'),
  ('HARD COVER / MACHINERY',['▥ = possible cover or major conduits','Maintain two Size-2-wide routes'],'purple'),
  ('ROUND 8 CONTROL',['Compare characters inside CZ','Social solutions remain valid'],'green')],
  'MAP FOR GM ADAPTATION / COVER MAY MOVE')
 tx(d,'GOAL: SECURE HARDWIRED ENGINEERING ENCLOSURE',210,1438,26,'fg',700,mono=True)
 tx(d,'NO SPECIFIED METRIC LENGTH',211,1500,17,'muted',700,mono=True)
 d.save()

def make_pirate():
 d,ox,oy,w,h=encounter_base('E-02_PIRATE_SALVAGE','CARGO TRANSFER / PIRATE SALVAGE','24 x 16 hex fields // separate optional encounter, do not combine with GAUNTLET',24,16)
 for r in range(5,11):
  for c in range(0,3):tint_cell(d,c,r,ox,oy,'cyan',.48)
  for c in range(21,24):tint_cell(d,c,r,ox,oy,'red',.48)
 # track and 2 clear corridors r4/5 and r11/12
 for c in range(4,21):
  tint_cell(d,c,8,ox,oy,'amber',.27)
 for c,r in [(6,7),(6,8),(7,7),(8,8),(8,9),(9,7),(12,6),(13,6),(14,6),(14,8),(15,8),(16,8),(18,7),(18,8),(18,9),(19,9)]:
  tint_cell(d,c,r,ox,oy,'purple',.43,'▥')
 # hauler 2x2-ish abstract group
 for c,r in [(11,7),(12,7),(11,8),(12,8)]:tint_cell(d,c,r,ox,oy,'green',.72)
 tx(d,'H',hxy(11,7,ox,oy)[0]+30,hxy(11,7,ox,oy)[1]+26,40,'bg',700,'middle',True)
 tx(d,'LIFT',hxy(1,8,ox,oy)[0],hxy(1,8,ox,oy)[1]+12,22,'fg',700,'middle',True)
 tx(d,'EXIT',hxy(22,8,ox,oy)[0],hxy(22,8,ox,oy)[1]+11,21,'fg',700,'middle',True)
 sidebar(d,[('ARRIVAL',['WEST SERVICE LIFT / PC ENTRY'],'cyan'),
  ('SALVAGE HAULER',['H = SIZE 2 HAULER START','Cargo: spares + crew records'],'green'),
  ('ESCAPE',['EAST AIRLOCK / PIRATE GOAL','Six-segment escape clock'],'red'),
  ('LANES',['Two distinct mech-capable routes','▥ = adjustable cargo cover'],'purple'),
  ('OUTCOMES',['Stop / seize / disable / negotiate','Loss never blocks Lock 1 or 2'],'amber')],
  'PIRATE TEMPLATE / TIER 1 / LL2')
 tx(d,'GOAL: INTERCEPT HAULER BEFORE ESCAPE',210,1438,26,'fg',700,mono=True)
 d.save()

def seam_positions(n):
 center=(14,10); cq,cr=oddr_to_ax(*center)
 dirs=[(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)]
 idxs={3:[0,2,4],4:[0,2,3,5],5:[0,1,2,3,4]}[n]
 cells=[ax_to_oddr(cq+8*dirs[i][0],cr+8*dirs[i][1]) for i in idxs]
 assert all(hex_dist(center,cell)==8 for cell in cells)
 assert all(hex_dist(a,b)>3 for j,a in enumerate(cells) for b in cells[j+1:])
 return center,cells

def make_seam(n):
 code=f'E-03_SEAM_{n}PCS';d,ox,oy,w,h=encounter_base(code,'CO-CONSCIOUSNESS LANCE BAY / THE SEAM',f'29 x 21 hexes // GM variant for {n} PCs // exact coupler ring positions',29,21)
 center,cells=seam_positions(n)
 cx,cy=hxy(*center,ox,oy)
 # objective energy ring to signal nonphysical hardware, not a wall
 for ring in [110,215,325]:circle(d,cx,cy,ring,'blue',sw=3,opacity=.16)
 # gradual marks at ring radius, no physical walls
 for c,r in cells:
  tint_cell(d,c,r,ox,oy,'green',.65)
  x,y=hxy(c,r,ox,oy)
  circle(d,x,y,HEX_SIZE-6,'green',sw=4)
  tx(d,'C',x,y+11,28,'fg',700,'middle',True)
 tint_cell(d,*center,ox,oy,'red',.8)
 circle(d,cx,cy,68,'red',sw=5,opacity=.75)
 tx(d,'A/B',cx,cy+11,31,'fg',700,'middle',True)
 # optional escort starts off-center, leave light marker
 for c,r in [(7,6),(7,15),(21,5),(22,16)]:
  tint_cell(d,c,r,ox,oy,'purple',.35,'S')
 sidebar(d,[('PHASE 1 / ANCHOR',['A/B starts in central space','Anchor immovable; break Overshield'],'red'),
  ('PHASE 2 / BODY',['Size 3 body emerges on Anchor','Anchor remains active / invulnerable'],'amber'),
  (f'COUPLER CELLS / {n} PCS',['C = exactly 8 hexes from Body','Each cell >3 hexes from the others'],'green'),
  ('OBJECTIVE',['Carry cells into Body space','Then destroy exposed Anchor'],'cyan'),
  ('ECHOES / ENTOURAGE',['S = suggested escort start','Keep phase-shifted crew untargetable'],'purple')],
  'SPATIAL CONDITIONS VERIFIED IN SOURCE')
 tx(d,'ONE COUPLER CELL PER PLAYER // GM POSITIONAL OVERLAY',210,1438,25,'fg',700,mono=True)
 tx(d,'CELL POSITIONS COMPUTED IN HEX STEPS; NO HULL DIMENSIONS IMPLIED',210,1495,18,'muted',700,mono=True)
 d.save()

# Render SVG with Inkscape if available, otherwise CairoSVG (Pillow additionally supports jpg contacts).

def raster(svgs,outdir,width=2800):
 for p in sorted(svgs):
  target=outdir/(p.stem+'.png')
  cairosvg.svg2png(url=str(p),write_to=str(target),output_width=width)
  print('PNG',target.name, target.stat().st_size)

def contact_sheet(paths,dest,cols=2,thumbw=1150,label_h=58):
 images=[]
 for p in paths:
  with Image.open(p) as im:
   im=im.convert('RGB')
   thumbh=round(thumbw*im.height/im.width)
   preview=im.resize((thumbw,thumbh),Image.Resampling.LANCZOS)
   images.append((p.name,preview))
 rowh=max(p.height for _,p in images)+label_h+22
 rows=math.ceil(len(images)/cols)
 sheet=Image.new('RGB',(cols*(thumbw+36)+36,rows*rowh+35),(4,16,25))
 pen=ImageDraw.Draw(sheet)
 try:font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',25)
 except OSError:font=ImageFont.load_default()
 for i,(label,im) in enumerate(images):
  x=36+(i%cols)*(thumbw+36);y=35+(i//cols)*rowh
  sheet.paste(im,(x,y+label_h))
  pen.text((x+6,y+8),label,fill=(196,241,255),font=font)
 sheet.save(dest,optimize=True)

if __name__=='__main__':
 make_master();make_master(safe=True)
 for spec in SECTORS:
  make_sector(spec);make_sector(safe_spec(spec),safe=True)
 make_gauntlet();make_pirate()
 for n in [3,4,5]:make_seam(n)
 raster(list(S.glob('*.svg')),SP,width=2560)
 raster(list(E.glob('*.svg')),EP,width=2560)
 contact_sheet(list(sorted(SP.glob('*.png'))),PR/'NAVIGATION_OVERVIEW.jpg',cols=2,thumbw=1000)
 contact_sheet(list(sorted(EP.glob('*.png'))),PR/'ENCOUNTER_OVERVIEW.jpg',cols=1,thumbw=1300)
 print('SVG',len(list(S.glob('*.svg'))),'ENCOUNTERS',len(list(E.glob('*.svg'))))
