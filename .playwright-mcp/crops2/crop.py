import sys
from PIL import Image
p,x0,y0,x1,y1,out=sys.argv[1:7]
im=Image.open(f'C:/repos/tombo/fontes/indice_godim/p{int(p):04d}.jpg')
c=im.crop((int(x0),int(y0),int(x1),int(y1)))
s=float(sys.argv[7]) if len(sys.argv)>7 else 2
c=c.resize((int(c.width*s),int(c.height*s)),Image.LANCZOS)
c.save(f'C:/repos/tombo/.playwright-mcp/crops2/{out}.jpg',quality=92)
