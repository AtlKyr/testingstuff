"""Procedural SFX + SFX + music.py sections + mix for Autopsy #13.
All sounds are synthesized here (no samples) -> fully owned audio.
Outputs: final_mix.wav (48 kHz stereo, pre-master), stems/*.wav
"""
import subprocess, wave, math, json, os
import numpy as np

SR = 48000
rng = np.random.default_rng(11)

import importlib.util
spec = importlib.util.spec_from_file_location("r2", "render2.py")
# only need timing info; import lightweight pieces
WORDS = json.load(open("words_14.json"))["words"]


def wt(word, nth=1):
    k = 0
    for w in WORDS:
        if w["text"].strip(".,?:…—") == word:
            k += 1
            if k == nth:
                return w["start"]
    raise KeyError(word)



import render_14 as R
T = R.T
END = WORDS[-1]["end"]
TOTAL = R.TOTAL
BOUNDS = R.BOUNDS
SC = {name: s for s, name in R.SCENES}
NS = int(TOTAL * SR)


def tvec(d):
    return np.arange(int(d * SR)) / SR

# ---------------------------------------------------------------- io
def load_voice():
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "vo_14.wav", "-ac", "1", "-ar", str(SR), "voice48_14.wav"], check=True)
    with wave.open("voice48_14.wav") as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    out = np.zeros(NS, np.float32); out[:min(NS, len(x))] = x[:NS]
    return out


def save(path, st):
    st = np.clip(st, -1, 1)
    if st.ndim == 1:
        st = np.stack([st, st], 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())


# ---------------------------------------------------------------- dsp helpers
def tvec(d):
    return np.arange(int(d * SR)) / SR


def env_ad(n, a, d):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) / max(d, 1e-4))
    return e


def lowpass(x, fc):
    """one-pole lowpass, fc may be array"""
    fc_arr = np.asarray(fc, dtype=np.float64)
    if fc_arr.ndim == 0:
        from scipy.signal import lfilter
        a = math.exp(-2 * math.pi * float(fc_arr) / SR)
        return lfilter([1 - a], [1, -a], x).astype(np.float32)
    fc = np.broadcast_to(fc_arr, x.shape)
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.zeros(len(x), dtype=np.float64)
    acc = 0.0
    xs = x.tolist(); al = a.tolist()
    for i in range(len(xs)):
        acc = (1 - al[i]) * xs[i] + al[i] * acc
        y[i] = acc
    return y.astype(np.float32)


def highpass(x, fc):
    return (x - lowpass(x, fc)).astype(np.float32)


def sweep_sine(f0, f1, d, curve=1.0):
    t = tvec(d)
    f = f0 + (f1 - f0) * (t / d) ** curve
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph).astype(np.float32), f


def square(ph, duty=0.5):
    return np.where((ph / (2 * np.pi)) % 1 < duty, 1.0, -1.0).astype(np.float32)



# ---------------------------------------------------------------- SFX library
def whoosh(d=0.42, up=True):
    n = int(d * SR)
    t = np.arange(n) / SR
    noise = rng.standard_normal(n).astype(np.float32)
    fc = 300 + 5200 * (np.sin(np.pi * t / d) ** 2)
    x = lowpass(noise, fc) - lowpass(noise, fc * 0.25)
    e = np.sin(np.pi * t / d) ** 1.6
    return (x * e * 1.6).astype(np.float32)


def pop():
    s, _ = sweep_sine(950, 260, 0.09, 0.6)
    e = env_ad(len(s), 0.002, 0.03)
    click = rng.standard_normal(len(s)).astype(np.float32) * env_ad(len(s), 0.0005, 0.004) * 0.3
    return (s * e * 0.9 + click).astype(np.float32)


def ding(f=1320):
    t = tvec(0.6)
    x = np.sin(2 * np.pi * f * t) + 0.45 * np.sin(2 * np.pi * f * 2.01 * t) + 0.2 * np.sin(2 * np.pi * f * 3.02 * t)
    return (x * env_ad(len(t), 0.002, 0.16) * 0.45).astype(np.float32)


def tick():
    n = int(0.012 * SR)
    x = rng.standard_normal(n).astype(np.float32)
    return highpass(x, 2500) * env_ad(n, 0.0003, 0.002) * 0.7


def key_click():
    n = int(0.03 * SR)
    t = np.arange(n) / SR
    x = highpass(rng.standard_normal(n).astype(np.float32), 1800) * env_ad(n, 0.0002, 0.004)
    x += np.sin(2 * np.pi * (220 + rng.random() * 80) * t) * env_ad(n, 0.0005, 0.01) * 0.5
    return x.astype(np.float32) * 0.6


def blip(f=880, d=0.07, duty=0.25):
    t = tvec(d)
    return square(2 * np.pi * f * t, duty) * env_ad(len(t), 0.001, d / 3) * 0.25


def jump():
    s, f = sweep_sine(260, 820, 0.16, 0.7)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return square(ph, 0.25) * env_ad(len(f), 0.002, 0.08) * 0.22


def step():
    return blip(140 + rng.random() * 40, 0.04, 0.5) * 0.6


def thud(f0=95, d=0.55, amt=1.0):
    s, _ = sweep_sine(f0, 38, d, 0.5)
    e = env_ad(len(s), 0.002, d / 3.5)
    n = lowpass(rng.standard_normal(len(s)).astype(np.float32), 900) * env_ad(len(s), 0.001, 0.05) * 2.0
    return ((s * 1.1 + n) * e * amt).astype(np.float32)


def stamp():
    x = thud(120, 0.6, 1.0)
    crack = highpass(rng.standard_normal(int(0.06 * SR)).astype(np.float32), 1200) * env_ad(int(0.06 * SR), 0.0005, 0.012) * 0.9
    x[:len(crack)] += crack
    return x


def flatline(d=1.4):
    t = tvec(d)
    x = np.sin(2 * np.pi * 1000 * t) * 0.6 + 0.25 * np.sin(2 * np.pi * 2000 * t)
    e = np.minimum(1, t / 0.01) * np.minimum(1, (d - t) / 0.08)
    return (x * e * 0.22).astype(np.float32)


def heart_beep():
    t = tvec(0.12)
    return (np.sin(2 * np.pi * 1000 * t) * np.minimum(1, (0.12 - t) / 0.02) * 0.22).astype(np.float32)


def scratch():
    d = 0.32
    n = int(d * SR); t = np.arange(n) / SR
    noise = rng.standard_normal(n).astype(np.float32)
    fc = 600 + 3000 * np.abs(np.sin(2 * np.pi * 4.5 * t))
    x = lowpass(noise, fc) - lowpass(noise, fc * 0.4)
    return (x * env_ad(n, 0.005, 0.12) * 2.2).astype(np.float32)


def womp():
    out = []
    for f0, f1, d in ((392, 370, 0.28), (370, 349, 0.28), (349, 300, 0.6)):
        s, f = sweep_sine(f0, f1, d)
        ph = 2 * np.pi * np.cumsum(f * (1 + 0.02 * np.sin(2 * np.pi * 6 * tvec(d)))) / SR
        x = 0.6 * np.sin(ph) + 0.3 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph)
        out.append((x * np.minimum(1, tvec(d) / 0.02) * np.minimum(1, (d - tvec(d)) / 0.06)).astype(np.float32))
    return np.concatenate(out) * 0.32


def thunder(d=2.6):
    n = int(d * SR); t = np.arange(n) / SR
    x = lowpass(rng.standard_normal(n).astype(np.float32), 180) * 6
    rumble = 0.6 + 0.4 * np.sin(2 * np.pi * 1.7 * t) * np.sin(2 * np.pi * 0.6 * t)
    crack = highpass(rng.standard_normal(n).astype(np.float32), 900) * env_ad(n, 0.002, 0.08) * 0.7
    return ((x * rumble + crack) * env_ad(n, 0.02, 0.9)).astype(np.float32)


def rain(d):
    n = int(d * SR)
    x = highpass(lowpass(rng.standard_normal(n).astype(np.float32), 6000), 900)
    return x * 0.10


def whistle_fall(d=1.2):
    s, _ = sweep_sine(1500, 280, d, 1.3)
    return s * np.minimum(1, tvec(d) / 0.05) * 0.16


def coin():
    t = tvec(0.45)
    x = np.sin(2 * np.pi * 2350 * t) + 0.6 * np.sin(2 * np.pi * 3520 * t)
    return (x * env_ad(len(t), 0.001, 0.09) * 0.28).astype(np.float32)


def horn():
    d = 0.55; t = tvec(d)
    f = 520 + 40 * np.sin(2 * np.pi * 14 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = ((ph / (2 * np.pi)) % 1) * 2 - 1
    return (lowpass(x.astype(np.float32), 2500) * np.minimum(1, t / 0.03) * np.minimum(1, (d - t) / 0.08) * 0.22).astype(np.float32)


def sting():
    """end jingle: rising arpeggio A C E A"""
    out = np.zeros(int(1.0 * SR), np.float32)
    for k, f in enumerate((440, 523.25, 659.25, 880)):
        b = blip(f, 0.16, 0.25) * 1.4
        i = int(k * 0.09 * SR); out[i:i + len(b)] += b
    return out



# ---------------------------------------------------------------- placement
sfx = np.zeros(NS, np.float32)


def place(x, t0, gain=1.0):
    i = int(t0 * SR)
    if i < 0 or i >= NS:
        return
    j = min(NS, i + len(x))
    sfx[i:j] += x[:j - i] * gain


def shimmer():
    out = np.zeros(int(1.2 * SR), np.float32)
    for k, f in enumerate((1318.5, 1568, 1760, 2093, 2637)):
        b = ding(f) * 0.7
        i = int(k * 0.07 * SR); out[i:i + len(b)] += b[:len(out) - i]
    return out


def siren(d=1.6):
    t = tvec(d)
    f = 700 + 250 * np.sin(2 * np.pi * 2.2 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * np.minimum(1, t / 0.05) * np.minimum(1, (d - t) / 0.2) * 0.12).astype(np.float32)


def crowd(d=1.6):
    n = int(d * SR)
    x = lowpass(rng.standard_normal(n).astype(np.float32), 1800) - lowpass(rng.standard_normal(n).astype(np.float32), 300)
    return (x * env_ad(n, 0.15, 0.7) * 1.4).astype(np.float32)


def beep_ok():
    t = tvec(0.14)
    return (np.sin(2 * np.pi * 880 * t) * np.minimum(1, (0.14 - t) / 0.03) * 0.2).astype(np.float32)


def buzzer():
    t = tvec(0.35)
    return (square(2 * np.pi * 140 * t, 0.5) * np.minimum(1, (0.35 - t) / 0.05) * 0.12).astype(np.float32)



# ---------------------------------------------------------------- SFX on the same anchors as the visuals (Autopsy #14)
place(whoosh(0.5), 0.0, 0.6); place(thud(80, 0.5, 1.0), 0.0, 1.0); place(stamp(), 0.01, 0.6); place(jump(), 0.0, 0.4)
place(ding(1318), 0.05, 0.3); place(coin(), T["two1"], 0.4); place(jump(), T["jumped"], 0.4)
for b in BOUNDS:
    place(whoosh(0.42), b - 0.2, 0.75)
place(pop(), SC["bestday"] + 0.05, 0.7); place(shimmer(), T["best"], 0.4); place(crowd(1.0), T["best"], 0.3); place(ding(1568), T["April"], 0.45)
place(pop(), SC["chase"] + 0.05, 0.6); place(thud(80, 0.4, 0.8), T["chase"], 0.7); place(pop(), T["bounce1"] - 0.25, 0.8)
for q in range(5):
    place(jump(), SC["chase"] + 0.3 + q * 0.6, 0.25)
place(pop(), T["A"] - 0.15, 0.8); place(ding(1046), T["wins"], 0.35); place(pop(), T["B"] - 0.15, 0.8); place(ding(1318), T["B"] + 0.03, 0.4)
place(pop(), T["hold1"] - 0.2, 0.9); place(ding(1568), T["hold1"], 0.5)
for q in range(4):
    place(blip(880 if q % 2 else 660, 0.06), T["hold1"] + 0.4 + q * 0.25, 0.3)
place(pop(), T["one1"] - 0.35, 0.8); place(thud(80, 0.4, 0.7), T["number1"], 0.6)
place(pop(), T["buy2"] - 0.12, 0.9); place(ding(1046), T["jump"], 0.4); place(pop(), T["hold2"] - 0.12, 0.9); place(ding(1318), T["month"], 0.4)
place(horn(), SC["rules"] + 0.3, 0.3)
for q in range(6):
    place(step(), SC["rules"] + 0.4 + q * 0.13, 0.3)
place(thunder(2.0), SC["race08"] + 0.1, 0.35); place(pop(), T["Thirty"] - 0.1, 0.7)
for q in range(8):
    place(blip(990 + 60 * (q % 3), 0.05), T["Thirty"] + 0.25 + q * 0.16, 0.28)
place(pop(), T["buys"] - 0.1, 0.6); place(whistle_fall(0.9), T["sinks"] - 0.25, 0.45); place(thud(70, 0.5, 1.0), T["sinks"], 0.8)
place(womp(), T["anyway"], 0.4)
place(pop(), T["calm"] - 0.25, 0.6); place(shimmer(), T["calm"], 0.3); place(pop(), T["Stocks"] - 0.1, 0.6); place(ding(1046), T["climb"], 0.4)
place(pop(), T["vanish"] - 0.25, 0.7); place(scratch(), T["vanish"], 0.4); place(pop(), T["sits"] - 0.3, 0.6); place(womp(), T["cash"], 0.3)
place(scratch(), SC["strange"] - 0.1, 0.6); place(thud(70, 0.5, 0.9), T["strange"], 0.7)
for q in range(10):
    place(tick(), T["Four"] + 0.2 + q * 0.3, 0.4)
place(stamp(), T["Four"] - 0.1, 0.8); place(pop(), T["already"] - 0.15, 0.7); place(thud(70, 0.5, 1.0), T["hole"], 0.8); place(buzzer(), T["hole"] + 0.1, 0.25)
place(thud(70, 0.5, 0.9), T["Remember"], 0.8); place(pop(), SC["remember"] + 0.05, 0.6)
place(stamp(), T["Two2"] - 0.1, 0.9); place(shimmer(), T["Two2"] + 0.1, 0.45); place(ding(1568), T["three2"], 0.45)
place(pop(), T["Thats"] - 0.2, 0.6); place(whistle_fall(1.2), T["whole"], 0.4); place(stamp(), T["erased"] - 0.05, 0.9); place(buzzer(), T["erased"] + 0.1, 0.3)
place(pop(), T["within"] - 0.1, 0.6)
k = 0
while SC["score"] + 0.2 + k * 0.08 < T["rev1"] - 0.15:   # drumroll
    place(tick(), SC["score"] + 0.2 + k * 0.08, 0.5); k += 1
place(scratch(), T["rev1"] - 0.1, 0.6); place(stamp(), T["rev1"], 0.9); place(womp(), T["rev1"] + 0.3, 0.35)
place(scratch(), T["rev2"] - 0.1, 0.6); place(stamp(), T["rev2"], 0.9); place(crowd(1.5), T["rev2"] + 0.2, 0.5)
place(shimmer(), T["rev2"] + 0.3, 0.4); place(horn(), T["rev2"] + 0.3, 0.5); place(pop(), T["rev2"] + 0.35, 0.7)
place(pop(), T["rev3"] - 0.1, 0.7); place(coin(), T["rev3"], 0.5)
place(stamp(), T["green"] - 0.1, 0.9); place(ding(1318), T["allclear"], 0.4)
place(scratch(), T["Its2"] - 0.15, 0.5); place(stamp(), T["Its2"] - 0.05, 1.0); place(thud(70, 0.5, 1.0), T["symptom"], 0.8)
place(pop(), T["Its2"] + 0.1, 0.7)
place(whoosh(0.5), SC["loop"] - 0.25, 0.6); place(sting(), END + 0.05, 0.6)

# ---------------------------------------------------------------- music: synthwave -> trap (the strange part + the clue) -> synthwave (final score)
from music import make_music_sections
MUSIC_PLAN = [(0.0, "synthwave"), (SC["strange"], "trap"), (SC["score"], "synthwave")]
M = make_music_sections(TOTAL, MUSIC_PLAN, SR)
music_drums, music_bass, music_arp, music_fx = M["drums"][:NS], M["bass"][:NS], M["arp"][:NS], M["fx"][:NS]
print("music switches", M["switches"])
tt = np.arange(NS) / SR


def seg(a, b):
    return ((tt >= a) & (tt < b)).astype(np.float32)


drums_g = np.ones(NS, np.float32)
arp_g = np.ones(NS, np.float32)
bass_g = np.ones(NS, np.float32)
drums_g *= 1 - 0.4 * seg(SC["guess"], SC["rules"])             # guess: thinner, let the question breathe
arp_g *= 1 - 0.5 * seg(SC["score"], T["rev1"] - 0.1)        # tension under the drumroll
music_all = np.ones(NS, np.float32)
music_all *= 1 - 0.7 * seg(T["rev1"] - 0.1, T["rev1"] + 0.35)
music_all *= 1 - 0.6 * seg(T["rev2"] - 0.1, T["rev2"] + 0.3)
music_all *= 1 - 0.6 * seg(T["Two2"] - 0.05, T["Two2"] + 0.3)
music_all *= 1 - 0.8 * seg(T["Its2"] - 0.05, T["Its2"] + 0.35)
fade_in = np.minimum(1, tt / 0.15)
fade_out = np.clip((TOTAL - tt) / 1.0, 0, 1)
music = (music_drums * drums_g + music_bass * bass_g + lowpass(music_arp, 5000) * arp_g + music_fx) * music_all * fade_in * fade_out
music = lowpass(music, 11000)

# ---------------------------------------------------------------- mix
voice = load_voice()
env = np.abs(voice)
env_s = lowpass(env, 6)
duck = 1 - 0.55 * np.clip(env_s / 0.03, 0, 1)
voice_n = voice / (np.abs(voice).max() + 1e-9) * 0.85
music_n = music / (np.abs(music).max() + 1e-9) * 0.40 * duck
sfx_n = sfx / (np.abs(sfx).max() + 1e-9) * 0.55
os.makedirs("stems", exist_ok=True)
save("stems/voice.wav", voice_n); save("stems/music.wav", music_n); save("stems/sfx.wav", sfx_n)
mix_l = voice_n + music_n * 0.95 + sfx_n * 1.0
mix_r = voice_n + music_n * 1.0 + sfx_n * 0.95
mix = np.stack([mix_l, mix_r], 1)
mix = mix / max(1.0, np.abs(mix).max() / 0.95)
save("premix_14.wav", mix)
print("premix done", TOTAL)
