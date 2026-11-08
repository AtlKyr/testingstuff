import subprocess, json, re, wave, numpy as np
SR=48000; TEMPO=1.05
raw=json.load(open("words_raw.json"))
GAP={"ch0":0.25,"ch1":1.3,"ch2":1.3,"ch3":1.1,"ch4":1.3,"ch5":1.3,"ch6":1.5,"ch7":0.7}   # silence BEFORE each chapter (chapter card stinger)
def load(f):
    subprocess.run(["ffmpeg","-y","-v","error","-i",f,"-ac","1","-ar",str(SR),"/tmp/x.wav"],check=True)
    with wave.open("/tmp/x.wav") as w: return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
allx=[]; words=[]; chstart={}; cur=0.0
for ch in ["ch0","ch1","ch2","ch3","ch4","ch5","ch6","ch7"]:
    x=load(f"{ch}.mp3")
    log=subprocess.run(["ffmpeg","-hide_banner","-i","/tmp/x.wav","-af","silencedetect=noise=-38dB:d=0.3","-f","null","-"],capture_output=True,text=True).stderr
    st=[float(v) for v in re.findall(r"silence_start: ([0-9.]+)",log)]; en=[float(v) for v in re.findall(r"silence_end: ([0-9.]+)",log)]
    sil=list(zip(st,en))
    segs=[]; c=0.0
    for a,b in sil:
        k=0.36 if b-a<1.0 else 0.55           # long pauses (dramatic beats) stay a bit longer
        if a<0.05: c=max(c,b-0.05); continue   # trim leading silence
        if b>=len(x)/SR-0.05: break
        if b-a<=k: continue
        segs.append((c,a+k/2)); c=b-k/2
    end=len(x)/SR
    # trim trailing silence
    if sil and sil[-1][1]>=end-0.05: end=sil[-1][0]+0.15
    segs.append((c,end))
    pieces=[];tmap=[];d=0.0
    for a,b in segs:
        p=x[int(a*SR):int(b*SR)].copy(); f=int(0.006*SR)
        if len(p)>2*f: p[:f]*=np.linspace(0,1,f); p[-f:]*=np.linspace(1,0,f)
        pieces.append(p); tmap.append((a,b,d)); d+=b-a
    y=np.concatenate(pieces)
    def m(t):
        for a,b,dd in tmap:
            if t<a: return dd
            if t<=b: return dd+t-a
        a,b,dd=tmap[-1]; return dd+b-a
    cur+=GAP[ch]
    allx.append(np.zeros(int(GAP[ch]*SR*TEMPO),np.float32)); allx.append(y)
    chstart[ch]=cur
    for w in raw[ch]:
        words.append(dict(text=w["text"],ch=ch,start=round(cur+m(w["start"])/TEMPO,3),end=round(cur+m(w["end"])/TEMPO,3)))
    cur+=len(y)/SR/TEMPO
    print(ch, round(len(x)/SR,1), "->", round(len(y)/SR/TEMPO,1))
z=np.concatenate(allx)
with wave.open("/tmp/vo_cat.wav","wb") as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(z,-1,1)*32767).astype(np.int16).tobytes())
subprocess.run(["ffmpeg","-y","-v","error","-i","/tmp/vo_cat.wav","-af",f"atempo={TEMPO}","-ar",str(SR),"vo_long.wav"],check=True)
json.dump({"words":words,"chstart":chstart},open("words_long.json","w"))
print("total", round(cur,2), chstart)
