import subprocess, json, re, numpy as np, wave
SR=48000
subprocess.run(["ffmpeg","-y","-v","error","-i","vo.mp3","-ac","1","-ar",str(SR),"vo_v.wav"],check=True)
with wave.open("vo_v.wav") as w: x=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
log=subprocess.run(["ffmpeg","-hide_banner","-i","vo_v.wav","-af","silencedetect=noise=-38dB:d=0.25","-f","null","-"],capture_output=True,text=True).stderr
st=[float(v) for v in re.findall(r"silence_start: ([0-9.]+)",log)]
en=[float(v) for v in re.findall(r"silence_end: ([0-9.]+)",log)]
sil=list(zip(st,en))
KEEP=0.15
def keep_for(a,b):
    if 49.3<a<49.7: return 0.9   # pause before Final score
    return KEEP
# build segments: list of (src_a, src_b) kept
segs=[]; cur=0.0
for a,b in sil:
    k=keep_for(a,b)
    if b-a<=k:
        if k>KEEP:   # dramatic pause longer than the real silence -> insert zeros at its middle
            m=(a+b)/2; segs.append((cur,m)); segs.append(("PAD",k-(b-a))); cur=m
        continue
    mid_a=a+k/2; mid_b=b-k/2
    segs.append((cur,mid_a)); cur=mid_b
segs.append((cur,len(x)/SR))
# trim leading silence <0.05
out=[]; tmap=[]; tdst=0.0
for a,b in segs:
    if a=="PAD":
        out.append(np.zeros(int(b*SR),np.float32)); tdst+=int(b*SR)/SR; continue
    ia,ib=int(a*SR),int(b*SR)
    piece=x[ia:ib].copy()
    # 6ms fades
    f=int(0.006*SR); 
    if len(piece)>2*f: piece[:f]*=np.linspace(0,1,f); piece[-f:]*=np.linspace(1,0,f)
    out.append(piece); tmap.append((a,b,tdst)); tdst+=b-a
y=np.concatenate(out)
print("tight dur", len(y)/SR)
with wave.open("vo_tight.wav","wb") as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(y,-1,1)*32767).astype(np.int16).tobytes())
json.dump(tmap,open("tmap.json","w"))
