import importlib.util, sys, cairo
sys.argv=["x","none"]
spec=importlib.util.spec_from_file_location("L","long2_render.py"); L=importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
ts=[float(x) for x in sys.argv[2:]] if False else None
def sheet(times, out, cols=4, sc=0.25):
    w,h=int(L.W*sc),int(L.H*sc); rows=(len(times)+cols-1)//cols
    big=cairo.ImageSurface(cairo.FORMAT_RGB24,w*cols,(h+24)*rows); bc=cairo.Context(big)
    bc.set_source_rgb(1,1,1); bc.paint()
    surf=cairo.ImageSurface(cairo.FORMAT_RGB24,L.W,L.H); ctx=cairo.Context(surf)
    for k,t in enumerate(times):
        L.frame(ctx,t); surf.flush()
        x=(k%cols)*w; y=(k//cols)*(h+24)
        bc.save(); bc.translate(x,y+24); bc.scale(sc,sc); bc.set_source_surface(surf,0,0); bc.paint(); bc.restore()
        bc.set_source_rgb(0,0,0); bc.select_font_face("JetBrains Mono"); bc.set_font_size(18); bc.move_to(x+6,y+18); bc.show_text(f"{t:.1f}s")
    big.write_to_png(out)
if __name__=="__main__":
    import json
    groups=json.loads(open("sheet_times.json").read())
    for i,g in enumerate(groups): sheet(g, f"sheet{i+1}.png")
