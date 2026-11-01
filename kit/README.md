# Strategy Autopsy — Short production kit (for scheduled daily runs)

Get the kit: `git clone --depth 1 -b strategy-autopsy-kit https://github.com/AtlKyr/testingstuff /home/claude/sa` (public repo; if the clone is refused, call add_repo owner=AtlKyr repo=testingstuff first). Work in a copy: `mkdir -p /home/claude/short && cp /home/claude/sa/kit/* /home/claude/short/`.

Files:
- `spy.csv` — SPY daily (Date, Adj Close, Close, High, Low, Open, Volume), 2005-01-03 → 2024-12-31 from yfinance. Only market data available offline (Yahoo etc. are blocked). Scale Open/High/Low by Adj Close/Close.
- `rocco.py` — Rocco pixel raccoon sprite: `draw_rocco(ctx, x, y, px, expr, costume)`.
  expr: neutral, talk, shock, smug, blink, sleep, sad. costume: none, grad, lab, race, detective, night, party, fire, tophat (+ crown, doctor added in `_engine.py`).
- `_engine.py` — 1080x1920 @30fps cairo engine template with placeholders `#@@DATA@@`, `#@@MOTION@@`, `#@@SCENES@@`, `#@@EVENTS@@`.
  It already contains: bunting(title), captions (word chips), flip_counter, card, tag, poly/series_xy charts, props (flag, magnifier, umbrella, coin),
  god_rays, heart_line, snail, skyline, ticker_band, wipe transitions, bursts, punch zoom, flash, vignette, paper grain, render().
  It reads `words_r2.json` — rename to your words file with sed.
- `_dip_helpers.py` — extra helpers: rain_bg, grid_bg, big_card, piggy, coin, star, clock, sx_of/sy_of, year_axis, money_k, stadium.
- Complete worked example (Autopsy #4, 2-day RSI) to copy patterns from:
  `r2.py` (backtest → conn.csv, trades.json), `r2_data.py`, `r2_timing.py` (T anchors, SCENES, motion), `r2_scenes.py` (10 scenes), `r2_events.py` (bursts/punch/flash), `audio_r2.py` (procedural SFX + chiptune + ducking mix).
- `tighten.py` + `mapwords.py` — shorten pauses in the voiceover, speed up (atempo) and remap word timestamps.

## One-time setup in a fresh container
```
pip install --break-system-packages pycairo pandas numpy scipy pillow fonttools brotli
mkdir -p ~/.fonts && cd /tmp && npm pack @fontsource/space-grotesk @fontsource/jetbrains-mono
for f in fontsource-space-grotesk-*.tgz fontsource-jetbrains-mono-*.tgz; do tar xzf $f; done
python3 - <<'PY'
import glob, os
from fontTools.ttLib import TTFont
for p in glob.glob('/tmp/package/files/*latin-[47]00-normal.woff2') + glob.glob('/tmp/package*/files/*latin-[47]00-normal.woff2'):
    f = TTFont(p); f.flavor = None; f.save(os.path.expanduser('~/.fonts/' + os.path.basename(p).replace('.woff2', '.ttf')))
PY
fc-cache -f
```
(npm pack extracts each into `package/` — extract one at a time and convert before the next, or rename the folder.) Inter is usually preinstalled; check with `fc-list | grep -i grotesk`.
ffmpeg is preinstalled.

## Pipeline (one Short, ~60 s)
1. **Backtest** the chosen strategy on `spy.csv` (2005–2024). House rules: long only, signal at close → fill at NEXT OPEN,
   0.05% cost per side, cash earns 0, $10,000 start, benchmark buy & hold ($70,985, max DD -55%). Use Adj Close (scale Open by Adj/Close).
   Exclude indicator warm-up bars. Compute: final $, CAGR, max DD, time in market, round trips, win rate, plus 1–2 surprising facts. Be honest.
2. **Script** (~140–160 words, English): first sentence = the most surprising true result (hook in <3 s), then "This is Strategy Autopsy. On the table: …",
   rules, test, results, the twist, final score vs buy & hold, verdict (short stamp phrase), outro "Follow…".
   Use eleven_v4 audio tags sparingly ([intense], [confident], [dry], [curious], [firm]). Write numbers as words.
3. **Voice**: ElevenLabs `creative_generate_speech`, voice_id `7WggD3IoWTIPT19PNyrW` (Jarnathan Cross), model `eleven_v4`,
   flow_id `Cw93HCnCGvppggZlnoyO`, **generations_count 1** (credits!). Poll status, download the mp3 from `content_url` with curl.
4. **Word timestamps**: `creative_transcribe_audio` (model eleven_scribe_v1, flow same, connect_from = the TTS node_id).
   The status result can be huge — download `words_download_url` with curl instead of reading words inline when possible.
5. **Tighten**: edit tighten.py/mapwords.py file names; target final VO ≤ 58 s (atempo 1.03–1.09).
6. **Render**: write data/timing/scenes/events modules for the new topic (8–11 scenes, a new scene every 3–7 s, Rocco changes costume per scene,
   chart/counter/tag reveals on word anchors), assemble into `_engine.py` placeholders, preview frames (snap a contact sheet at ~15 times and LOOK at it,
   fix overlaps with captions at y≈1240), then render: `python3 render_X.py out.mp4`.
7. **Audio**: adapt audio_r2.py (events + music gains), loudnorm two-pass to -14 LUFS / -1 dBTP (linear=true), re-render or mux.
8. **QA**: ffprobe duration ≤ 60 s, 1080x1920, check -14 LUFS, extract ~10 frames and look at them.
9. **Deliver**: send the mp4 + cover frame png (the hook frame with the big number) with SendUserFile, then the upload text.
