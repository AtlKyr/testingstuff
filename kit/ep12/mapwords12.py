import json, subprocess
TEMPO=1.05
tmap=json.load(open("tmap.json"))
def m(t):
    for a,b,d in tmap:
        if t<a: return d/TEMPO
        if a<=t<=b: return (d+t-a)/TEMPO
    a,b,d=tmap[-1]; return (d+b-a)/TEMPO
W=json.load(open("words_raw.json"))["words"]
out=[]
for w in W:
    if w.get("type")!="word" or w["text"].startswith("["): continue
    out.append(dict(text=w["text"],start=round(m(w["start"]),3),end=round(m(w["end"]),3)))
json.dump({"words":out},open("words_12.json","w"),indent=0)
subprocess.run(["ffmpeg","-y","-v","error","-i","vo_tight.wav","-af",f"atempo={TEMPO}","-ar","48000","vo_12.wav"],check=True)
print(len(out), out[0], out[-1])
r=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0","vo_12.wav"],capture_output=True,text=True); print(r.stdout)
