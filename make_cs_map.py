from PIL import Image, ImageDraw, ImageFont
W,H=1800,1260
BG=(250,250,248); INK=(20,24,28); MUTED=(95,103,110); RULE=(200,205,210)
C={'found':(31,111,95),'core':(41,76,140),'web':(176,96,20),'data':(120,60,150),'sys':(150,40,50),'meta':(90,90,90)}
BOLD="/System/Library/Fonts/Supplemental/Arial Bold.ttf"; REG="/System/Library/Fonts/Supplemental/Arial.ttf"
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
def f(sz,bold=False): return ImageFont.truetype(BOLD if bold else REG,sz)
def box(x,y,w,h,title,lines,color,fill=(255,255,255)):
    d.rounded_rectangle([x,y,x+w,y+h],radius=14,fill=fill,outline=color,width=3)
    d.rectangle([x,y,x+w,y+42],fill=color); 
    d.rounded_rectangle([x,y,x+w,y+60],radius=14,fill=None,outline=color,width=3)
    d.text((x+16,y+10),title,font=f(22,True),fill=(255,255,255))
    yy=y+56
    for ln in lines:
        d.text((x+16,yy),ln,font=f(18),fill=INK); yy+=27
def arrow(x1,y1,x2,y2,color=MUTED):
    d.line([(x1,y1),(x2,y2)],fill=color,width=4)
    import math
    ang=math.atan2(y2-y1,x2-x1); L=14
    p1=(x2-L*math.cos(ang-0.5),y2-L*math.sin(ang-0.5)); p2=(x2-L*math.cos(ang+0.5),y2-L*math.sin(ang+0.5))
    d.polygon([ (x2,y2),p1,p2],fill=color)
# title
d.text((60,40),"Free CS self-study map 2026 — pick a goal, follow one path",font=f(40,True),fill=INK)
d.text((60,92),"One best free course per slot. Every link opened and checked on 23 Aug 2026. Hours are rough self-study estimates.",font=f(20),fill=MUTED)
# Foundations
box(60,150,520,290,"1  FOUNDATIONS  (everyone, ~150–300 h)",[
 "• Tools: MIT Missing Semester 2026  (~20 h)",
 "• Intro CS: Harvard CS50x 2026  (~120–200 h)",
 "     or Python-first: CS50P  (~60–90 h)",
 "• Practice: Exercism (free, mentored)",
 "• Git: Pro Git book (free) + Learn Git Branching",
 "• Discrete math: MIT 6.042J (free book + videos)",
 "",
 "Math for most jobs: algebra + logic + 6.042J."],C['found'])
# Core
box(640,150,520,290,"2  CORE CS  (~400–600 h, any order after 1)",[
 "• Data structures & algorithms: Berkeley CS61B sp26",
 "• Computer architecture: Nand to Tetris",
 "• Operating systems: OSTEP (free book) + CS537",
 "• Networks: Kurose & Ross free lectures",
 "• Databases: CMU 15-445 (Fall 2025 videos)",
 "• Languages & compilers: Crafting Interpreters",
 "• Software construction: MIT 6.102 sp26",
 "Each slot has a free alternative in the post."],C['core'])
arrow(580,295,640,295)
# Tracks
d.text((60,480),"3  PICK ONE TRACK  (you can come back for the others)",font=f(24,True),fill=INK)
arrow(900,440,900,470); 
box(60,520,540,330,"WEB DEVELOPMENT  (~300–500 h)",[
 "• HTML/CSS/JS: The Odin Project – Foundations",
 "• JavaScript deep dive: javascript.info",
 "• Frontend: react.dev Learn (or fCC certs)",
 "• Backend: Odin NodeJS  /  Django tutorial",
 "• SQL: SQLBolt  →  CS50 SQL",
 "• CI/CD & containers: Full Stack Open 11–12",
 "• Projects: app-ideas (GitHub) → deploy 2–3",
 "Math: high-school algebra is enough."],C['web'])
box(630,520,540,330,"DATA / ML / AI  (~400–600 h)",[
 "• Python: CS50P  (or Kaggle Learn)",
 "• Linear algebra: 3Blue1Brown + MIT 18.06",
 "• Probability & stats: MIT 18.05 (or 6.431x)",
 "• ML: Andrew Ng ML Specialization (audit free)",
 "• Deep learning: Karpathy – Zero to Hero",
 "• LLMs: Hugging Face LLM course",
 "• Hands-on: Kaggle Titanic → micro-courses",
 "Math: + linear algebra, prob/stats, some calculus."],C['data'])
box(1200,520,540,330,"SYSTEMS / SECURITY  (~400–600 h)",[
 "• C: CS50x  (or Beej's Guide to C)",
 "• Rust or Go: the Rust Book  /  A Tour of Go",
 "• Linux: Missing Semester  →  Linux Journey",
 "• Security: MIT 6.858 + pwn.college / OverTheWire",
 "• Crypto: Boneh's Cryptography I (audit free)",
 "• Distributed systems: MIT 6.5840 notes + videos",
 "",
 "Math: 6.042J + number theory for crypto."],C['sys'])
for x in (330,900,1470): arrow(x,500,x,520)
# Meta
box(60,900,1680,300,"FULL OPEN CURRICULA & HOW TO STUDY",[
 "Whole-degree maps: OSSU Computer Science (GitHub) · Teach Yourself CS · The Odin Project · freeCodeCamp · MIT OpenCourseWare · CS50 family · roadmap.sh",
 "How to learn: Learning How to Learn (Coursera, audit free) · Learning Scientists' six strategies (free PDFs) · Missing Semester for the tooling habits",
 "",
 "Rules of thumb: finish one slot before starting the next two · build something after every course · ship a project every month · ask for code review (Exercism mentors are free)",
 "Certificates: CS50's own certificate is free; edX/Coursera verified certificates cost money. Everything on this map is free to learn.",
 "",
 "Made by u/koraynar · links and alternatives in the post · tell me what is wrong or missing and I will update it",
],C['meta'],fill=(246,246,244))
img.save("/Users/koraynar/Documents/Jobsonplatforms_claude/research-samples/cs-map-2026.png",optimize=True)
print("ok")
