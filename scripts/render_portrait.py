from pathlib import Path
from base64 import b64encode
from PIL import Image
from io import BytesIO

# Preserve the exact approved picture; only add a reveal mask.
im = Image.open('portrait.png').convert('RGB')
im.thumbnail((1000, 1100), Image.Resampling.LANCZOS)
buf = BytesIO()
im.save(buf, format='PNG', optimize=True)
data = b64encode(buf.getvalue()).decode('ascii')
w,h = im.size
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs><clipPath id="reveal"><rect width="{w}" height="{h}"><animate attributeName="height" from="0" to="{h}" dur="5.5s" begin="0s" fill="freeze"/></rect></clipPath></defs>
<rect width="{w}" height="{h}" rx="12" fill="#0d1117" stroke="#30363d"/>
<image width="{w}" height="{h}" xlink:href="data:image/png;base64,{data}" clip-path="url(#reveal)"/>
<rect x="0" y="0" width="{w}" height="2" fill="#39d353" opacity="0">
<animate attributeName="y" from="0" to="{h-2}" dur="5.5s" fill="freeze"/>
<animate attributeName="opacity" values="0;0.8;0.8;0" keyTimes="0;0.03;0.97;1" dur="5.5s" fill="freeze"/>
</rect></svg>'''
Path('portrait-animated.svg').write_text(svg, encoding='utf-8')
