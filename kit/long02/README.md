# Long #2 — The Nasdaq Just Crashed. What Happens Next? (2026-11-08)
16:9 long-form, 5:27. Build (from a work dir that also has spy.csv, rocco.py, music.py and kit-long _helpers.py/long_ui.py/_sfx.py from long #1):
1. `python3 bt_l2.py` → l2.json, eq_panic21.npy, eq_bh.npy
2. TTS per chapter (script.json, ElevenLabs Jarnathan Cross, eleven_v4) → ch0..ch7.mp3, words_raw.json (scribe)
3. `python3 build_vo.py` → vo_long.wav, words_long.json
4. `cat head2.py _helpers.py long_ui.py scenes2.py main2.py > long2_render.py`; `python3 sheet.py` for contact sheets
5. audio: `(head of audio_long.py; _sfx.py; audio2_body.py) > audio2.py` → premix → 2-pass loudnorm -14 LUFS → final_mix_long.wav
6. 4 segments `python3 long2_render.py segN.mp4 a b` → concat + mux
Music sections: trap → marimba (guess) → synthwave (ch1) → chip (ch2) → lofi (ch3) → funk (ch4) → trap (twist) → synthwave (ch5) → funk (ch6) → lofi (honest part) → marimba (verdict).
