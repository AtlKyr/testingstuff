"""Procedural background-music library for Strategy Autopsy Shorts.

Every episode must use a DIFFERENT style from the previous episode (see LESSONS.md, "Music rotation").

    from music import make_music, STYLES
    M = make_music(TOTAL, "synthwave", SR)          # dict of float32 stems, each len = int(TOTAL*SR)
    music_drums, music_bass, music_arp = M["drums"], M["bass"], M["arp"]   # drop-in for the old chiptune block

Stems are pre-balanced so the existing section gains / ducking in audio_XX.py keep working unchanged
(drums dropped in the twist scene, arp thinned in the fees scene, music_all dips on big hits).
`M["bpm"]` is returned too, if you want to place SFX on the beat.

Styles
- chip     : 100 BPM 8-bit chiptune, Am-F-C-G square arps (used in #1-#6 — avoid now).
- synthwave: 112 BPM driving retro synth, detuned saw pad + offbeat bass, Em-C-G-D. Good for breakouts / momentum.
- lofi     : 84 BPM swung lo-fi hip-hop, soft electric-piano 7th chords, dusty kit, Dm7-G7-Cmaj7-Am7. Calm, "detective".
- funk     : 104 BPM heist funk, slap-ish pluck bass, clap on 2&4, 16th hats, Em7/A7 stabs. Cheeky, sneaky.
- trap     : 140 BPM half-time trap, 808 sine bass with glides, hat rolls, minor bell melody, Cm-Ab-Eb-Bb. Tense, dramatic.
- marimba  : 96 BPM bright tropical marimba + shaker + plucky bass, C-Am-F-G. Light, playful (seasonal topics).
"""
import numpy as np

STYLES = ["synthwave", "lofi", "funk", "trap", "marimba", "chip"]


def _nf(m):
    return 440.0 * 2 ** ((m - 69) / 12)


class _Ctx:
    def __init__(self, total, sr, seed):
        self.sr = sr
        self.ns = int(total * sr) + 1
        self.total = total
        self.rng = np.random.default_rng(seed)
        self.drums = np.zeros(self.ns, np.float32)
        self.bass = np.zeros(self.ns, np.float32)
        self.arp = np.zeros(self.ns, np.float32)

    def tv(self, d):
        return np.arange(int(max(d, 0.001) * self.sr)) / self.sr

    def env(self, n, a, d):
        t = np.arange(n) / self.sr
        e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) / max(d, 1e-4))
        return e.astype(np.float32)

    def adsr(self, n, a, r):
        t = np.arange(n) / self.sr
        dur = n / self.sr
        return (np.minimum(1, t / max(a, 1e-4)) * np.clip((dur - t) / max(r, 1e-4), 0, 1)).astype(np.float32)

    def add(self, buf, x, t0, g=1.0):
        i = int(t0 * self.sr)
        if i >= self.ns or i < 0:
            return
        j = min(self.ns, i + len(x))
        buf[i:j] += (x[:j - i] * g).astype(np.float32)

    def noise(self, d):
        return self.rng.standard_normal(int(d * self.sr)).astype(np.float32)


def _lp(x, fc, sr):
    a = np.exp(-2 * np.pi * fc / sr)
    y = np.empty_like(x)
    acc = 0.0
    # vectorised one-pole via lfilter-like cumulative trick is unstable; use scipy if available
    try:
        from scipy.signal import lfilter
        return lfilter([1 - a], [1, -a], x).astype(np.float32)
    except Exception:
        for i, v in enumerate(x):
            acc = (1 - a) * v + a * acc
            y[i] = acc
        return y


def _hp(x, fc, sr):
    return (x - _lp(x, fc, sr)).astype(np.float32)


def _sq(ph, duty=0.5):
    return np.where((ph / (2 * np.pi)) % 1.0 < duty, 1.0, -1.0).astype(np.float32)


def _saw(ph):
    return (2 * ((ph / (2 * np.pi)) % 1.0) - 1).astype(np.float32)


def _tri(ph):
    return (2 * np.abs(2 * ((ph / (2 * np.pi)) % 1.0) - 1) - 1).astype(np.float32)


# ------------------------------------------------------------------ drum voices
def _kick(c, f0=150, f1=45, d=0.22, punch=1.0):
    t = c.tv(d)
    f = f1 + (f0 - f1) * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / c.sr
    return (np.sin(ph) * c.env(len(t), 0.001, d / 3) * punch).astype(np.float32)


def _snare(c, d=0.16, hp=1500, g=0.6):
    n = _hp(c.noise(d), hp, c.sr) * c.env(int(d * c.sr), 0.001, d / 4)
    t = c.tv(d)
    body = np.sin(2 * np.pi * 190 * t) * c.env(len(t), 0.001, 0.03) * 0.5
    return ((n + body) * g).astype(np.float32)


def _clap(c, g=0.6):
    out = np.zeros(int(0.2 * c.sr), np.float32)
    for k, off in enumerate((0, 0.011, 0.022)):
        b = _hp(c.noise(0.15), 1200, c.sr) * c.env(int(0.15 * c.sr), 0.0005, 0.02 if k < 2 else 0.06)
        i = int(off * c.sr)
        out[i:i + len(b)] += b[:len(out) - i]
    return out * g


def _hat(c, d=0.04, g=0.3, open_=False):
    dd = 0.18 if open_ else d
    return (_hp(c.noise(dd), 7000, c.sr) * c.env(int(dd * c.sr), 0.0005, dd / (2 if open_ else 4)) * g).astype(np.float32)


def _shaker(c, g=0.18):
    d = 0.07
    return (_hp(c.noise(d), 5000, c.sr) * c.adsr(int(d * c.sr), 0.03, 0.04) * g).astype(np.float32)


# ------------------------------------------------------------------ styles
def _chip(c):
    bpm = 100; B = 60 / bpm
    CH = [(57, [69, 72, 76]), (53, [65, 69, 72]), (48, [64, 67, 72]), (55, [67, 71, 74])]
    for b in range(int(c.total / B) + 2):
        t = b * B; root, tones = CH[(b // 4) % 4]
        if b % 4 in (0, 2): c.add(c.drums, _kick(c), t, 0.9)
        if b % 4 in (1, 3): c.add(c.drums, _snare(c), t, 0.7)
        for h in range(2): c.add(c.drums, _hat(c), t + h * B / 2, 0.6)
        for h in range(2):
            m = root - 12 + (12 if h else 0); d = B / 2 * 0.9; tv = c.tv(d)
            c.add(c.bass, _lp(_sq(2 * np.pi * _nf(m) * tv) * c.env(len(tv), 0.003, d / 2) * 0.22, 1200, c.sr), t + h * B / 2)
        for q in range(4):
            m = tones[(b * 4 + q) % 3] + (12 if (b * 4 + q) % 6 >= 3 else 0); d = B / 4 * 0.8; tv = c.tv(d)
            c.add(c.arp, _sq(2 * np.pi * _nf(m) * tv, 0.25) * c.env(len(tv), 0.002, d / 3) * 0.10, t + q * B / 4)
    return bpm


def _synthwave(c):
    bpm = 112; B = 60 / bpm
    CH = [(40, [64, 67, 71]), (36, [60, 64, 67]), (43, [62, 67, 71]), (38, [62, 66, 69])]  # Em C G D
    bar_len = 4 * B
    for bar in range(int(c.total / bar_len) + 2):
        t0 = bar * bar_len; root, tones = CH[bar % 4]
        # pad: detuned saws, whole bar, slow attack
        tv = c.tv(bar_len * 1.02)
        pad = np.zeros(len(tv), np.float32)
        for m in tones:
            for det in (-0.12, 0.0, 0.11):
                pad += _saw(2 * np.pi * _nf(m) * (1 + det / 100 * 3) * tv)
        pad = _lp(pad * c.adsr(len(tv), 0.25, 0.3) * 0.028, 2600, c.sr)
        c.add(c.arp, pad, t0)
        for k in range(4):
            t = t0 + k * B
            c.add(c.drums, _kick(c, 120, 42, 0.25), t, 0.95)
            if k in (1, 3):
                c.add(c.drums, _snare(c, 0.28, 900, 0.55), t, 0.8)
            c.add(c.drums, _hat(c, g=0.25), t + B / 2, 0.7)
            # offbeat bass 8ths: root on off, octave pulse
            for h in range(2):
                d = B / 2 * 0.85; tv2 = c.tv(d)
                m = root - 12 + (12 if h else 0)
                x = _saw(2 * np.pi * _nf(m) * tv2) * c.env(len(tv2), 0.002, d / 2) * 0.24
                c.add(c.bass, _lp(x, 700, c.sr), t + h * B / 2)
        # lead arp, 16ths, every other bar
        if bar % 2 == 1:
            seq = [tones[0] + 12, tones[1] + 12, tones[2] + 12, tones[1] + 12]
            for q in range(16):
                m = seq[q % 4]; d = B / 4 * 0.7; tv3 = c.tv(d)
                c.add(c.arp, _sq(2 * np.pi * _nf(m) * tv3, 0.5) * c.env(len(tv3), 0.002, d / 3) * 0.05, t0 + q * B / 4)
    return bpm


def _lofi(c):
    bpm = 84; B = 60 / bpm; sw = 0.62  # swing ratio for 8ths
    CH = [(38, [62, 65, 69, 72]), (43, [62, 65, 67, 71]), (36, [60, 64, 67, 71]), (45, [60, 64, 67, 69])]  # Dm7 G7 Cmaj7 Am7
    bar_len = 4 * B
    vinyl = _hp(c.noise(c.total + 1), 3000, c.sr) * 0.004
    crackle = np.zeros_like(vinyl)
    idx = c.rng.integers(0, len(crackle), int(c.total * 9))
    crackle[idx] = c.rng.uniform(0.05, 0.18, len(idx)).astype(np.float32)
    c.add(c.drums, (vinyl + crackle)[:c.ns], 0.0, 1.0)
    for bar in range(int(c.total / bar_len) + 2):
        t0 = bar * bar_len; root, tones = CH[bar % 4]
        # electric-piano chord: sine + soft 2nd harmonic, tremolo, hit on 1 and the "and" of 2
        for hit, dur in ((0.0, 1.6 * B), (1.5 * B, 2.3 * B)):
            tv = c.tv(dur)
            ch = np.zeros(len(tv), np.float32)
            for m in tones:
                f = _nf(m) * (1 + c.rng.uniform(-0.002, 0.002))
                ch += np.sin(2 * np.pi * f * tv) + 0.25 * np.sin(4 * np.pi * f * tv)
            ch *= c.env(len(tv), 0.006, dur / 2.2) * (1 + 0.15 * np.sin(2 * np.pi * 4.5 * tv)) * 0.045
            c.add(c.arp, ch, t0 + hit)
        for k in range(4):
            t = t0 + k * B
            if k == 0 or (k == 2 and bar % 2 == 1):
                c.add(c.drums, _lp(_kick(c, 110, 48, 0.28), 900, c.sr), t, 0.9)
            if k == 2 and bar % 2 == 0:
                c.add(c.drums, _lp(_kick(c, 110, 48, 0.28), 900, c.sr), t + sw * B, 0.6)
            if k in (1, 3):
                c.add(c.drums, _lp(_snare(c, 0.2, 1200, 0.5), 5000, c.sr), t, 0.75)
            for h in range(2):
                c.add(c.drums, _lp(_hat(c, g=0.22), 9000, c.sr), t + (sw * B if h else 0), 0.55 if h else 0.75)
            # round sine bass, swung
            notes = [root - 12, root - 12, root - 5, root - 10]
            d = B * 0.9; tv2 = c.tv(d)
            x = np.sin(2 * np.pi * _nf(notes[k]) * tv2) * c.adsr(len(tv2), 0.01, 0.1) * 0.34
            c.add(c.bass, x, t)
    return bpm


def _funk(c):
    bpm = 104; B = 60 / bpm
    CH = [(40, [64, 67, 71, 74]), (45, [64, 67, 69, 73])]  # Em7, A7
    bar_len = 4 * B
    bass_pat = [(0, 0), (0.75, 0), (1.5, 12), (2.0, 10), (2.5, 0), (3.25, 7), (3.5, 10)]  # (beat, semitone)
    for bar in range(int(c.total / bar_len) + 2):
        t0 = bar * bar_len; root, tones = CH[(bar // 2) % 2]
        for beat, st in bass_pat:
            d = B * 0.35; tv = c.tv(d)
            f = _nf(root - 12 + st)
            x = (_sq(2 * np.pi * f * tv, 0.35) * 0.6 + np.sin(2 * np.pi * f * tv)) * c.env(len(tv), 0.001, d / 2.5) * 0.22
            c.add(c.bass, _lp(x, 1500, c.sr), t0 + beat * B)
        for k in range(4):
            t = t0 + k * B
            if k in (0, 2): c.add(c.drums, _kick(c, 140, 50, 0.2), t, 0.9)
            if k == 2 and bar % 2: c.add(c.drums, _kick(c, 140, 50, 0.2), t + 0.75 * B, 0.6)
            if k in (1, 3): c.add(c.drums, _clap(c), t, 0.8)
            for q in range(4):
                c.add(c.drums, _hat(c, g=0.2, open_=(q == 2 and k == 3)), t + q * B / 4, 0.75 if q % 2 == 0 else 0.45)
        # chord stabs on the off-16ths
        for beat in (0.5, 1.75, 2.5, 3.75):
            d = 0.13; tv = c.tv(d); st = np.zeros(len(tv), np.float32)
            for m in tones:
                st += _sq(2 * np.pi * _nf(m) * tv, 0.3)
            c.add(c.arp, _lp(st * c.env(len(tv), 0.001, 0.05) * 0.035, 3000, c.sr), t0 + beat * B)
    return bpm


def _trap(c):
    bpm = 140; B = 60 / bpm  # half-time feel: snare on beat 3
    CH = [36, 32, 39, 34]  # C Ab Eb Bb roots (minor feel)
    MEL = [[72, 75, 79, 75], [72, 75, 80, 75], [70, 74, 79, 74], [70, 74, 77, 74]]
    bar_len = 4 * B
    for bar in range(int(c.total / bar_len) + 2):
        t0 = bar * bar_len; root = CH[bar % 4]
        # 808: long sine with slight pitch drop, glide into next bar
        d = bar_len * 0.95; tv = c.tv(d)
        f = _nf(root - 12) * (1 + 0.5 * np.exp(-tv / 0.02))
        x = np.tanh(np.sin(2 * np.pi * np.cumsum(f) / c.sr) * 1.6) * c.env(len(tv), 0.003, 0.9) * 0.32
        c.add(c.bass, x, t0)
        c.add(c.bass, x[:int(0.6 * B * c.sr)] * 0.7, t0 + 2.5 * B)
        c.add(c.drums, _kick(c, 90, 40, 0.3), t0, 0.8)
        c.add(c.drums, _clap(c, 0.7), t0 + 2 * B, 0.9)
        c.add(c.drums, _snare(c, 0.18, 1800, 0.35), t0 + 2 * B, 0.6)
        # hats: 8ths with a 32nd roll at the end of every 2nd bar
        for q in range(8):
            c.add(c.drums, _hat(c, g=0.22), t0 + q * B / 2, 0.7)
        if bar % 2 == 1:
            for r in range(8):
                c.add(c.drums, _hat(c, 0.025, 0.18), t0 + 3 * B + r * B / 8, 0.6)
        # bell melody (sine + inharmonic partial)
        for q, m in enumerate(MEL[bar % 4]):
            d = 0.6; tv = c.tv(d); f = _nf(m)
            bell = (np.sin(2 * np.pi * f * tv) + 0.4 * np.sin(2 * np.pi * f * 2.76 * tv) * np.exp(-tv / 0.08)) * c.env(len(tv), 0.002, 0.25)
            c.add(c.arp, bell * 0.06, t0 + q * B)
    return bpm


def _marimba(c):
    bpm = 96; B = 60 / bpm
    CH = [(48, [60, 64, 67]), (45, [57, 60, 64]), (41, [57, 60, 65]), (43, [59, 62, 67])]  # C Am F G
    bar_len = 4 * B
    pat = [0, 2, 1, 2, 0, 1, 2, 1]
    for bar in range(int(c.total / bar_len) + 2):
        t0 = bar * bar_len; root, tones = CH[bar % 4]
        for q in range(8):
            m = tones[pat[q]] + 12 * (q in (3, 6)); d = 0.35; tv = c.tv(d); f = _nf(m)
            mar = (np.sin(2 * np.pi * f * tv) + 0.3 * np.sin(2 * np.pi * f * 4 * tv) * np.exp(-tv / 0.02)) * c.env(len(tv), 0.001, 0.09)
            c.add(c.arp, mar * 0.09, t0 + q * B / 2)
        for k in range(4):
            t = t0 + k * B
            if k in (0, 2): c.add(c.drums, _kick(c, 130, 55, 0.18), t, 0.75)
            if k == 3 or (k == 1 and bar % 2): c.add(c.drums, _snare(c, 0.1, 2500, 0.35), t + (B / 2 if k == 1 else 0), 0.7)
            for q in range(4):
                c.add(c.drums, _shaker(c), t + q * B / 4, 0.9 if q % 2 else 0.6)
            for h, st in ((0, 0), (0.5, 7)):
                d = B * 0.4; tv = c.tv(d); f = _nf(root - 12 + st)
                c.add(c.bass, np.sin(2 * np.pi * f * tv) * c.env(len(tv), 0.002, 0.12) * 0.3, t + h * B)
    return bpm


_FN = dict(chip=_chip, synthwave=_synthwave, lofi=_lofi, funk=_funk, trap=_trap, marimba=_marimba)
# target RMS per stem so all styles sit at the same level in the existing mixes
_TARGET = dict(drums=0.075, bass=0.07, arp=0.035)


def make_music(total, style, sr=48000, seed=7):
    if style not in _FN:
        raise ValueError(f"unknown style {style}; choose from {STYLES}")
    c = _Ctx(total, sr, seed)
    bpm = _FN[style](c)
    out = {}
    for k in ("drums", "bass", "arp"):
        x = getattr(c, k)[:c.ns]
        r = float(np.sqrt(np.mean(x[: int(min(total, 20) * sr)] ** 2)) + 1e-9)
        out[k] = (x * (_TARGET[k] / r)).astype(np.float32)
    out["bpm"] = bpm
    return out


if __name__ == "__main__":
    # python3 music.py demo  -> music_demo.wav (8 s of every style, back to back)
    import sys, wave
    sr = 48000
    parts = []
    for s in STYLES:
        M = make_music(8.5, s, sr)
        mix = M["drums"] + M["bass"] + M["arp"]
        mix = mix[: int(8 * sr)]
        fade = np.minimum(1, np.minimum(np.arange(len(mix)), len(mix) - np.arange(len(mix))) / (0.15 * sr))
        mix = mix * fade / (np.max(np.abs(mix)) + 1e-9) * 0.8
        parts.append(mix); parts.append(np.zeros(int(0.4 * sr), np.float32))
        print(s, M["bpm"], "bpm")
    y = np.concatenate(parts)
    with wave.open("music_demo.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())


# ------------------------------------------------------------------ in-video music changes at key moments
def _riser(sr, d=0.9, seed=3):
    rng = np.random.default_rng(seed)
    n = int(d * sr); t = np.arange(n) / sr
    x = rng.standard_normal(n).astype(np.float32)
    out = np.zeros(n, np.float32)
    # sweeping band: one-pole low-pass whose cutoff rises 300 Hz -> 9 kHz
    acc = 0.0
    fc = 300 * (30 ** (t / d))
    a = np.exp(-2 * np.pi * fc / sr)
    for i in range(n):
        acc = (1 - a[i]) * x[i] + a[i] * acc
        out[i] = acc
    out = out - _lp(out, 200, sr)
    return (out * (t / d) ** 2 * 0.5).astype(np.float32)


def _impact(sr):
    t = np.arange(int(0.6 * sr)) / sr
    f = 40 + 110 * np.exp(-t / 0.05)
    boom = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t / 0.18)
    return (boom * 0.6).astype(np.float32)


def make_music_sections(total, sections, sr=48000, xfade=0.18, fx=True, seed=7):
    """Music that CHANGES at key moments inside one video.

    sections: list of (start_time, style) sorted by time, first start 0.0, e.g.
        [(0.0, "synthwave"), (SC["problem"], "trap"), (SC["score"], "synthwave"), (SC["verdict"], "funk")]
    Each style restarts on its own downbeat exactly at its start time, so every switch lands "on the one".
    A short riser leads into each switch and a sub impact hits on it (fx=True); both go into M["fx"].
    Returns dict drums/bass/arp/fx stems (same lengths) + "switches" (list of switch times).
    In audio_XX.py:  music = (drums*drums_g + bass*bass_g + arp*arp_g + M["fx"]) * music_all * fades
    """
    ns = int(total * sr) + 1
    out = {k: np.zeros(ns, np.float32) for k in ("drums", "bass", "arp", "fx")}
    tt = np.arange(ns) / sr
    starts = [s for s, _ in sections] + [total + 1]
    for i, (s0, style) in enumerate(sections):
        s1 = starts[i + 1]
        seg_len = min(total, s1 + xfade) - s0
        if seg_len <= 0:
            continue
        M = make_music(seg_len + 0.05, style, sr, seed + i)
        i0 = int(s0 * sr)
        g = np.ones(ns, np.float32)
        g *= np.clip((tt - s0) / xfade + 1.0, 0, 1) if i > 0 else 1.0     # fade in just before start
        g *= np.clip((s1 + xfade - tt) / xfade, 0, 1)                       # fade out just after next start
        for k in ("drums", "bass", "arp"):
            x = M[k]
            j = min(ns, i0 + len(x))
            buf = np.zeros(ns, np.float32); buf[i0:j] = x[:j - i0]
            out[k] += buf * g
    switches = [s for s, _ in sections[1:]]
    if fx:
        r = _riser(sr); b = _impact(sr)
        for s in switches:
            a = int((s - len(r) / sr) * sr)
            if a >= 0:
                out["fx"][a:a + len(r)] += r[:ns - a]
            k = int(s * sr)
            out["fx"][k:k + len(b)] += b[:max(0, ns - k)]
    out["switches"] = switches
    return out


def demo_sections(path="music_sections_demo.wav", sr=48000):
    secs = [(0.0, "synthwave"), (6.0, "trap"), (12.0, "lofi"), (18.0, "funk")]
    M = make_music_sections(24.0, secs, sr)
    mix = M["drums"] + M["bass"] + M["arp"] + M["fx"]
    mix = mix / (np.abs(mix).max() + 1e-9) * 0.85
    import wave
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes())
    return path
