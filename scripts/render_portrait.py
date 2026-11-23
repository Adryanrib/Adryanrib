from PIL import Image, ImageOps
import html
from pathlib import Path
im=Image.open('portrait.png').convert('L')
# Crop the approved artwork, excluding its baked-in terminal frame.
w,h=im.size
im=im.crop((int(w*.045),int(h*.065),int(w*.955),int(h*.935)))
cols,rows=132,75
im=im.resize((cols,rows),Image.Resampling.LANCZOS)
ramp=' .,:;irsXA253hMHGS#9B&@'
lines=[]
for y in range(rows):
    lines.append(''.join(ramp[min(len(ramp)-1,int(max(0,min(1,(im.getpixel((x,y))-17)/180))*(len(ramp)-1)))] for x in range(cols)))
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="840" height="880" viewBox="0 0 840 880" font-family="monospace">','<rect x="1" y="1" width="838" height="878" rx="12" fill="#0d1117" stroke="#30363d"/>','<circle cx="22" cy="19" r="5" fill="#f85149"/><circle cx="40" cy="19" r="5" fill="#d29922"/><circle cx="58" cy="19" r="5" fill="#3fb950"/><text x="420" y="24" text-anchor="middle" fill="#8b949e" font-size="15">retrato / terminal</text><path d="M20 37H820 M20 830H820" stroke="#30363d"/>']
parts.append('<defs>')
for i in range(rows):
    y=48+i*10.3
    parts.append(f'<clipPath id="r{i}"><rect x="24" y="{y}" width="792" height="12"><animate attributeName="width" from="0" to="792" begin="{i*.075:.3f}s" dur=".075s" fill="freeze"/></rect></clipPath>')
parts.append('</defs><g font-size="10" fill="#c9d1d9" xml:space="preserve">')
for i,s in enumerate(lines):
    parts.append(f'<text x="24" y="{57+i*10.3}" textLength="792" lengthAdjust="spacingAndGlyphs" clip-path="url(#r{i})">{html.escape(s)}</text>')
parts.append('</g><text x="23" y="856" font-size="15" fill="#39d353">adryan@github:~$</text><rect x="180" y="843" width="9" height="15" fill="#39d353"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect><text x="815" y="856" text-anchor="end" font-size="13" fill="#8b949e">clique para abrir o terminal</text></svg>')
Path('portrait-animated.svg').write_text(''.join(parts),encoding='utf-8')
