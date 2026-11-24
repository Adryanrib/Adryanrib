import datetime as dt, json, os, urllib.request, calendar
from collections import Counter
from xml.sax.saxutils import escape
from pathlib import Path
U='adryanribee'
START='2026-11-01'
MONTHS=['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
def save(name,w,h,body):
    Path(name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="monospace">{body}</svg>')
def txt(x,y,s,size=24,color='#e6edf3',extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" {extra}>{escape(str(s))}</text>'
def rect(x,y,w,h,c,extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" {extra}/>'
url=f'https://github-contributions-api.jogruber.de/v4/{U}'
try:
    raw=json.load(urllib.request.urlopen(url,timeout=30))
    days=raw['contributions']
    if not days: raise ValueError('empty calendar')
    Path('profile-data.json').write_text(json.dumps(days))
except Exception:
    if not Path('profile-data.json').exists(): raise
    days=json.loads(Path('profile-data.json').read_text())
days=sorted((d for d in days if d['date'] >= START and d['date'] <= dt.date.today().isoformat()),key=lambda d:d['date'])
if not days: raise ValueError('Nenhuma data disponível desde novembro de 2026')
start=dt.date.fromisoformat(START)
end=max(dt.date(2027,10,31),dt.date.today())
by_date={d['date']:d for d in days}
calendar_days=[by_date.get((start+dt.timedelta(days=i)).isoformat(),{'date':(start+dt.timedelta(days=i)).isoformat(),'count':0,'level':0}) for i in range((end-start).days+1)]
offset=(start.weekday()+1)%7
colors=['#30363d','#0e4429','#006d32','#26a641','#39d353']
total=sum(d['count'] for d in days)
b=''
last=None
for i,d in enumerate(calendar_days):
    date=dt.date.fromisoformat(d['date']); week,row=divmod(i+offset,7)
    x=39+week*15.2; y=25+row*15.2
    if date.month!=last:
        b+=txt(x,15,MONTHS[date.month],12,'#7d8590');last=date.month
    delay=(week+row*.5)*.065
    b+=f'<rect x="{x}" y="{y}" width="13" height="13" rx="2" fill="{colors[min(4,d["level"])]}"/>'
    if d['level']:
        b+=f'<rect x="{x}" y="{y}" width="13" height="13" rx="2" fill="#b4ffaa" opacity="0"><animate attributeName="opacity" values="0;.85;0" begin="{delay:.2f}s" dur=".6s" fill="freeze"/></rect>'
for r,n in [(1,'Mon'),(3,'Wed'),(5,'Fri')]: b+=txt(1,36+r*15.2,n,11,'#7d8590')
b+=txt(39,151,f'{total:,} contributions since Nov 2026',14)
save('contributions-en.svg',max(860,39+((len(calendar_days)+offset+6)//7)*15.2+12),158,b)
counts=[d['count'] for d in days];active=sum(c>0 for c in counts)
run=longest=0
for c in counts:
    run=run+1 if c else 0;longest=max(run,longest)
cur=0
for c in reversed(counts[:-1] if not counts[-1] else counts):
    if not c: break
    cur+=1
best=max(counts)
b=rect(1,1,838,878,'#0d1117','rx="12" stroke="#30363d"')
for x,c in [(22,'#f85149'),(40,'#d29922'),(58,'#3fb950')]: b+=f'<circle cx="{x}" cy="19" r="5" fill="{c}"/>'
b+=txt(420,24,'contributions / statistics',15,'#7d8590','text-anchor="middle"')
vals=[('current streak',cur,'days','#39d353'),('longest streak',longest,'days','#e6edf3'),('contributions',total,'since Nov 2026','#e6edf3'),('active days',active,f'of {len(days)} days','#e6edf3'),('best day',best,'contributions','#e6edf3'),('avg / active day',round(total/active,1) if active else 0,'contributions','#e6edf3')]
for i,(label,v,cap,color) in enumerate(vals):
    x=20+(i%2)*408;y=54+(i//2)*166
    tile=rect(x,y,392,150,'#161b22','rx="8"')+txt(x+20,y+32,label,21,'#7d8590')+txt(x+20,y+91,f'{v:,}',52,color,'font-weight="bold"')+txt(x+20,y+127,cap,18,'#7d8590')
    b+=f'<g>{tile}<animate attributeName="opacity" values="0;1" begin="{i*.15:.2f}s" dur=".45s" fill="freeze"/></g>'
b+=txt(22,582,'contributions / month',21,'#7d8590')
months=Counter()
for d in days: months[d['date'][:7]]+=d['count']
peak=max(1,*months.values());bw=790/len(months)
for i,(m,v) in enumerate(sorted(months.items())):
    x=25+i*bw+(bw-min(50,bw*.68))/2;h=190*v/peak
    b+=f'<rect x="{x}" y="{824-h}" width="{min(50,bw*.68)}" height="{h}" fill="#26a641"><animate attributeName="height" from="0" to="{h}" begin="{1+i*.06}s" dur=".6s" fill="freeze"/><animate attributeName="y" from="824" to="{824-h}" begin="{1+i*.06}s" dur=".6s" fill="freeze"/></rect>'
    b+=txt(x+min(50,bw*.68)/2,848,MONTHS[int(m[-2:])]+'/'+m[2:4],13,'#7d8590','text-anchor="middle"')
save('stats-en.svg',840,880,b)
