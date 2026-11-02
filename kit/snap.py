import sys, cairo
sys.argv=[sys.argv[0]]+sys.argv[1:]
import render_05 as R
from PIL import Image
ts=[float(x) for x in sys.argv[1].split(",")]
out=sys.argv[2]
ims=[]
for t in ts:
    surf=cairo.ImageSurface(cairo.FORMAT_RGB24,R.W,R.H); ctx=cairo.Context(surf)
    name,s0,s1=R.scene_at(t)
    ctx.save(); z=(1+0.035*R.prog(t,s0,max(0.5,s1-s0)))*R.punch(t)
    ctx.translate(R.W/2,R.H/2); ctx.scale(z,z); ctx.translate(-R.W/2,-R.H/2)
    R.SCENE_FN[name](ctx,t,s0,s1); R.bursts(ctx,t); ctx.restore(); R.vignette(ctx)
    if t<R.T["follow"]-0.2: R.captions(ctx,t)
    R.paper_grain(ctx,0.06); R.flash(ctx,t); R.wipe(ctx,t)
    surf.write_to_png("/tmp/_s.png"); im=Image.open("/tmp/_s.png").convert("RGB").resize((360,640)); ims.append((t,im))
cols=5; rows=(len(ims)+cols-1)//cols
sheet=Image.new("RGB",(cols*370,rows*670),(40,40,40))
from PIL import ImageDraw
d=ImageDraw.Draw(sheet)
for k,(t,im) in enumerate(ims):
    x,y=(k%cols)*370,(k//cols)*670; sheet.paste(im,(x+5,y+25)); d.text((x+8,y+5),f"t={t:.2f}",fill=(255,255,0))
sheet.save(out)
