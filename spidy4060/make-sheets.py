from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json
p=Path(__file__).parent
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20)
def sheet(items,name,cols,w,h):
 rows=(len(items)+cols-1)//cols; im=Image.new('RGB',(cols*w,rows*h+95),'#e9e8df');d=ImageDraw.Draw(im);d.text((26,20),'SPIDY / '+name.replace('-',' ').upper(),font=font,fill='#24344a');d.text((26,51),'BRAIN DECOY • shared sculpted character rig',font=font,fill='#657080')
 for i,(file,label) in enumerate(items):
  a=Image.open(file).convert('RGBA');a.thumbnail((w-20,h-52));x=(i%cols)*w+(w-a.width)//2;y=95+(i//cols)*h;im.paste(a,(x,y),a);d.text(((i%cols)*w+12,y+h-42),label,font=font,fill='#24344a')
 im.save(p/'sheets'/f'{name}.jpg',quality=94)
cast=json.loads((p/'characters/manifest.json').read_text())
sheet([(p/'characters'/f'{a["key"]}.png',a['name']) for a in cast[:5]],'principal-cast',5,350,620)
sheet([(p/'characters'/f'{a["key"]}.png',a['name']) for a in cast[5:20]],'city-cast',5,350,620)
for key in ['spidy','peter','gwen','child']:
 sheet([(p/'review/heads'/f'{key}-{e}.png',e) for e in ['neutral','happy','shock','angry','sad','exhausted']],key+'-expressions',3,350,420)
 sheet([(p/'review/turns'/f'{key}-{f}.png',str(f)) for f in [-1,-.5,0,.5,1]],key+'-turns',5,300,380)
