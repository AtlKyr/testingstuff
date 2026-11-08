
# ================================================================ long #2 audio
import sys
sys.argv = ["x", "none"]
import importlib.util
_spec = importlib.util.spec_from_file_location("R", "long2_render.py"); R = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(R)
from music import make_music_sections
A = R.A
TOTAL = R.TOTAL
NS = int(TOTAL * SR)
sfx = np.zeros(NS, np.float32)
names = [s[1].__name__ for s in R.SCENES]


def sc(name, nth=1):
    k = [i for i, n in enumerate(names) if n == name][nth - 1]
    return R.SCENES[k][0], (R.SCENES[k + 1][0] if k + 1 < len(R.SCENES) else TOTAL)


def place(x, t0, gain=1.0):
    i = int(t0 * SR)
    if i < 0 or i >= NS:
        return
    j = min(NS, i + len(x)); sfx[i:j] += x[:j - i] * gain


def ticks(t0, t1, dt=0.07, g=0.45):
    tt = t0
    while tt < t1:
        place(tick(), tt, g); tt += dt


CARDS = [R.SCENES[k][0] for k, n in enumerate(names) if n == "f" and R.SCENES[k][3] is None]
# transitions
for b in R.BOUNDS:
    place(whoosh(0.42), b - 0.2, 0.55)
for c0 in CARDS:
    place(stamp(), c0 + 0.08, 0.75)
    for k in range(2):
        place(heart_beep() * 0.7, c0 + 0.55 + k * 0.5, 0.6)
for (t0, x, y, pal, sz) in R.EVENTS:
    place(pop(), t0, 0.7)
    if sz >= 1.2:
        place(ding(1318 if pal[0] != R.C["red"] else 659), t0 + 0.03, 0.4)
for t0 in R.FLASH:
    place(stamp(), t0, 0.85)

# ---- ch0 cold open
place(thud(80, 0.6, 1.0), 0.0, 0.9); place(thunder(2.6), 0.05, 0.45); place(siren(1.8), 0.3, 0.5)
ticks(0.5, 4.3, 0.15, 0.25)
s0, _ = sc("s_hook2")
for j in range(19):
    place(tick(), s0 + j * 1.6 / 19, 0.6)
place(stamp(), A("ch0", "worst"), 0.6)
s0, s1 = sc("s_hook3")
for j in range(10):
    place(coin(), s0 + 0.2 + j * 0.28, 0.35)
place(whoosh(0.8), A("ch0", "gone") - 0.2, 0.6)
s0, _ = sc("s_hook4")
for j in range(7):
    place(pop(), A("ch0", "everyone") + j * 0.22, 0.5)
place(buzzer(), A("ch0", "Do") + 0.05, 0.7)
for j in range(39):
    place(tick(), A("ch0", "every", 1) + j / 39 * 2.2, 0.5)
for w, n in (("day", 3), ("month", 1), ("year", 1)):
    place(ding(1568), A("ch0", w, n), 0.4)
s0, _ = sc("s_guess")
for j in range(39):
    place(tick(), s0 + 0.4 + j * 0.035, 0.25)
tt = s0 + 1.0
while tt < A("ch0", "Lock"):
    place(tick(), tt, 0.35); tt += 0.5
place(key_click() * 2, A("ch0", "Lock"), 0.6); place(thud(140, 0.3, 0.6), A("ch0", "Lock") + 0.05, 0.5)
place(scratch(), A("ch0", "wouldn't") - 0.1, 0.5)
# ---- ch1
place(shimmer(), A("ch1", "record"), 0.5)
place(whistle_fall(1.6), A("ch1", "Then"), 0.6)
place(thud(90, 0.5, 0.9), A("ch1", "twelve"), 0.6); place(thud(80, 0.5, 0.9), A("ch1", "six"), 0.6)
place(jump(), A("ch1", "bounced"), 0.6)
place(thunder(2.0), A("ch1", "end") - 0.3, 0.3)
place(stamp(), A("ch1", "first") - 0.1, 0.5)
# ---- ch2
for w in ("used", "Two", "Every", "Thirty-nine"):
    t0 = A("ch2", w)
    for j in range(12):
        place(key_click(), t0 + j * 0.055, 0.35)
s0, _ = sc("s_timeline39")
for j in range(39):
    place(tick(), s0 + 0.2 + j / 39 * 1.6, 0.4)
place(thud(70, 0.6, 1.0), A("ch2", "Minus"), 0.8)
place(shimmer(), A("ch2", "next") - 0.2, 0.5)
# ---- ch3
place(blip(660, 0.12), A("ch3", "fifty-nine"), 0.6); place(blip(587, 0.12), A("ch3", "fifty-five"), 0.6)
place(blip(523, 0.12), A("ch3", "sixty-two"), 0.6); place(blip(659, 0.12), A("ch3", "sixty-seven"), 0.6)
place(womp(), A("ch3", "worse") + 0.1, 0.55)
place(whistle_fall(1.4), A("ch3", "eight", 2) - 0.4, 0.5)
s0, s1 = sc("s_coin")
for j in range(6):
    place(coin(), s0 + 0.3 + j * 0.45, 0.35)
place(horn(), A("ch3", "test"), 0.5)
# ---- ch4
place(coin(), A("ch4", "Ten"), 0.6)
s0, s1 = sc("s_race")
tt = s0 + 0.2
while tt < A("ch4", "front"):
    place(step(), tt, 0.35); tt += 0.32
for w in ("out", "ahead", "eleven", "rebound", "behind"):
    place(blip(784 if w in ("ahead",) else 392, 0.1), A("ch4", w), 0.5)
place(crowd(1.8), A("ch4", "front") - 0.2, 0.6)
s0, _ = sc("f", 6)
ticks(s0 + 0.3, A("ch4", "seventy") - 0.1, 0.06, 0.4)
place(ding(1318), A("ch4", "seventy"), 0.5)
ticks(A("ch4", "seventy") + 0.6, A("ch4", "eighty") - 0.1, 0.06, 0.4)
place(ding(1568), A("ch4", "eighty"), 0.5); place(horn(), A("ch4", "won") + 0.05, 0.5)
place(scratch(), A("ch4", "Not") - 0.1, 0.6)
s0, _ = sc("s_windows")
place(blip(523, 0.12), s0 + 0.5, 0.5)
for w, n in (("One", 1), ("Two", 2), ("Three", 1), ("Six", 1)):
    place(blip(330, 0.14), A("ch4", w, n), 0.6)
for j in range(4):
    place(blip(660 + j * 110, 0.1), A("ch4", "narrow") + j * 0.08, 0.5)
place(stamp(), A("ch4", "looking"), 0.6)
# ---- ch5
place(shimmer(), A("ch5", "ten"), 0.5)
for j in range(10):
    place(pop(), A("ch5", "ten") + j * 0.08, 0.35)
place(stamp(), A("ch5", "worst") - 0.1, 0.4)
place(thud(100, 0.4, 0.7), A("ch5", "earlier") - 0.1, 0.5)
place(whoosh(1.0), A("ch5", "doors") - 0.4, 0.5); place(shimmer(), A("ch5", "doors"), 0.6)
# ---- ch6
ta = A("ch6", "Thirty-six", 1)
tt = A("ch6", "Your"); dt = 0.25
while tt < ta - 0.05:
    place(tick(), tt, 0.5); tt += dt; dt = max(0.05, dt * 0.93)
place(shimmer(), ta, 0.8); place(crowd(2.0), ta + 0.05, 0.6)
s0, _ = sc("s_tiles")
for j in range(39):
    place(tick(), s0 + 0.1 + j * 0.03, 0.35)
for k in range(3):
    place(thud(110, 0.35, 0.7), A("ch6", "three") + k * 0.15, 0.45)
place(flatline(1.2), A("ch6", "dot-com"), 0.35)
s0, s1 = sc("s_verdict")
tt = s0 + 0.2
while tt < s1 - 0.2:
    place(heart_beep(), tt, 0.35); tt += 1.0
place(stamp(), A("ch6", "loud") - 0.2, 0.7); place(shimmer(), A("ch6", "quiet") - 0.2, 0.6)
# ---- ch7
s0, _ = sc("s_outro")
for j in range(9):
    place(pop(), s0 + 0.6 + j * 1.15, 0.25)
place(beep_ok(), A("ch7", "Fees"), 0.6); place(buzzer(), A("ch7", "Losers"), 0.4)
place(sting(), A("ch7", "subscribe"), 0.7)

# ---------------------------------------------------------------- music: switches at key moments
SECT = [(0.0, "trap"), (sc("s_guess")[0], "marimba"), (CARDS[0], "synthwave"), (CARDS[1], "chip"), (CARDS[2], "lofi"),
        (CARDS[3], "funk"), (sc("s_windows")[0], "trap"), (CARDS[4], "synthwave"), (CARDS[5], "funk"),
        (sc("s_honest")[0], "lofi"), (sc("s_verdict")[0], "marimba")]
print("music sections", [(round(a, 1), b) for a, b in SECT])
M = make_music_sections(TOTAL, SECT, SR, xfade=0.18, fx=True)
tt = np.arange(NS) / SR


def seg(a, b):
    return ((tt >= a) & (tt < b)).astype(np.float32)


music_all = np.ones(NS, np.float32); drums_g = np.ones(NS, np.float32)
for c0 in CARDS:
    music_all *= 1 - 0.5 * seg(c0 + 0.2, c0 + 1.6)
for nm in ("s_world", "s_month", "s_hindsight", "s_lehman", "s_honest"):
    a, b = sc(nm); drums_g *= 1 - 0.75 * seg(a, b)
a = A("ch6", "Your"); drums_g *= 1 - 0.85 * seg(a, ta)       # drumroll space before the reveal
music_all *= 1 - 0.85 * seg(ta - 0.6, ta + 0.05)              # the beat drops out right before 36/39
for t0 in R.FLASH:
    music_all *= 1 - 0.6 * seg(t0 - 0.05, t0 + 0.5)
fade = np.minimum(1, tt / 0.05) * np.clip((TOTAL - tt) / 1.8, 0, 1)
L = lambda k: M[k][:NS]
music = (L("drums") * drums_g + L("bass") + L("arp")) * music_all * fade + L("fx") * fade

# ---------------------------------------------------------------- mix
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "vo_long.wav", "-ac", "1", "-ar", str(SR), "/tmp/vo48_l2.wav"], check=True)
with wave.open("/tmp/vo48_l2.wav") as w:
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
voice = np.zeros(NS, np.float32); voice[:min(NS, len(x))] = x[:NS]
env_s = lowpass(np.abs(voice), 6)
duck = 1 - 0.55 * np.clip(env_s / 0.03, 0, 1)
voice_n = voice / (np.abs(voice).max() + 1e-9) * 0.85
music_n = music / (np.percentile(np.abs(music), 99.9) + 1e-9) * 0.26 * duck
sfx_n = sfx / (np.abs(sfx).max() + 1e-9) * 0.45
mix = np.stack([voice_n + music_n * 0.95 + sfx_n, voice_n + music_n + sfx_n * 0.95], 1)
mix = mix / max(1.0, np.abs(mix).max() / 0.95)
save("premix_long.wav", mix)
print("premix", TOTAL)
