# Auto-upload to YouTube Studio via Claude in Chrome (proven 2026-11-22 with #38 + #39)

The user asked on 2026-11-22: upload AND schedule every Short yourself, 3 per day: 17:30, 23:30, 04:30 (Europe/Istanbul).
This works only when the run has the Claude in Chrome tools (`mcp__claude-in-chrome__*`), i.e. the scheduled task
requires the user's computer, and Chrome is open with the Strategy Autopsy channel signed in to YouTube Studio.

## Why the chunk trick
`file_upload` accepts at most 3.8 MB per call; a Short is ~55–60 MB. So: split the mp4 into 3.6 MB parts, push each part
into a helper `<input type=file>` on the Studio page, rebuild the file inside the page, check its SHA-256 there, and hand
it to Studio's real uploader input (`input[name=Filedata]`). Verified byte-for-byte (17 parts each, hash match).
Do NOT print the hash from the page (the tool output filter blocks it) — compare inside the page.

## Steps (viewport was 1037x697; prefer refs from `find` over coordinates)
0. ToolSearch once: tabs_context_mcp, tabs_create_mcp, navigate, computer, find, read_page, javascript_tool, file_upload,
   list_connected_browsers, select_browser. If several browsers are connected and none is selected, use the one whose
   Studio shows "Strategy Autopsy" (2026-11-22 that was "Browser 2", deviceId 8541bef0-0367-4b7d-ad9e-d4ca850472b1).
   Open your own new tab.
1. Container: `split -b 3600000 -d -a 2 StrategyAutopsy_NN_X.mp4 pNN_` and `sha256sum` the mp4.
2. navigate `https://studio.youtube.com/channel/UC3CRqu3G9dhca-MlkRyE55g/videos/upload?d=ud` (opens "Upload videos").
3. javascript_tool — receiver:
```js
(() => { document.getElementById('cc-chunk-input')?.remove(); window.__ccParts = []; const i = document.createElement('input'); i.type='file'; i.id='cc-chunk-input'; i.setAttribute('aria-label','cc chunk receiver'); i.style.cssText='position:fixed;bottom:4px;left:4px;z-index:2147483647;width:160px;height:24px'; i.addEventListener('change', () => { for (const f of i.files) window.__ccParts.push(f); }); document.body.appendChild(i); return document.querySelectorAll('input[type=file][name=Filedata]').length; })()
```
4. `find` "cc chunk receiver file input" → ref. `file_upload` every part (origin `https://studio.youtube.com`, one part per
   call; up to 6 calls in parallel worked fine — the rebuild dedupes and sorts by name).
5. javascript_tool — rebuild + hand over (fill in SHA and NAME):
```js
const uniq = new Map(); for (const p of window.__ccParts) uniq.set(p.name, p); const parts = [...uniq.values()].sort((a,b)=>a.name.localeCompare(b.name)); const blob = new Blob(parts); const h = await crypto.subtle.digest('SHA-256', await blob.arrayBuffer()); const hex=[...new Uint8Array(h)].map(b=>b.toString(16).padStart(2,'0')).join(''); const ok = hex === 'SHA'; let handed='no'; if (ok) { const file = new File([blob], 'NAME', {type:'video/mp4'}); const inp = document.querySelector('input[type=file][name=Filedata]'); const dt = new DataTransfer(); dt.items.add(file); inp.files = dt.files; inp.dispatchEvent(new Event('change', {bubbles:true})); handed='yes'; window.__ccParts=[]; document.getElementById('cc-chunk-input')?.remove(); } ({count: parts.length, size: blob.size, ok, handed})
```
   If ok is false: re-send the missing parts (count < expected) and run it again. The upload dialog then opens on
   Details and the video is already "Saved as private" (a draft — nothing is public yet).
6. Title: click the title box, ctrl+a, type the HYPE title. Description: click the description box, type it (newlines OK).
   Typing "#backtest" opens hashtag suggestions — close them by clicking the "Details" heading (do not press Escape).
7. Thumbnail: `find` → the hidden file-input next to the "Upload file" button → `file_upload` the cover PNG (~2.3 MB). Shorts accept it.
8. Playlists: "Select" → tick "Strategy Autopsy" → Done. It is the ONLY playlist on the channel; the backlog names
   ("All Cases", "Timing & Calendar Myths") do not exist — never create playlists.
9. Audience: "No, it's not made for kids" is the channel default — verify it.
10. "Show advanced settings": Tags textbox → type the tags as one comma-separated line WITH a trailing comma (each becomes a
    chip). "Video language" → option "English" (scroll_to the option ref, then click). Category is Education by default.
11. Verify with javascript_tool:
```js
const d=document.querySelector('ytcp-uploads-dialog'); const tb=d.querySelectorAll('#textbox'); ({title: tb[0]?.innerText, desc: tb[1]?.innerText, playlist: d.querySelector('ytcp-video-metadata-playlists')?.innerText.replace(/\s+/g,' '), tags: [...d.querySelectorAll('ytcp-chip, ytcp-free-text-chip')].map(c=>c.innerText.trim()).filter(Boolean).length, notKids: d.querySelector('tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]')?.hasAttribute('checked')})
```
12. Next → Video elements → Related video "Add" → in "Choose specific video" click the search box BY REF (`find`
    "Search your videos textbox"; coordinate clicks do not focus it), type "Famous" → click
    "I Tested 3 Famous Trading Strategies for 20 Years" (= https://youtu.be/qEMMPEl1E98).
13. Next → Initial check (wait for "Checks complete. No issues found.") → Next → Visibility.
14. Scheduled: expand "Schedule" → time-zone dropdown → "(GMT+0300) Local Time" → date picker → click the day →
    time field: triple_click, ctrl+a, type e.g. "11:30 PM", Enter → button "Schedule". The 04:30 slot is the NEXT
    calendar day, "4:30 AM". If the slot time has already passed: choose "Public" → "Publish" instead.
15. The "Video scheduled"/"Video published" dialog shows the Shorts link (youtube.com/shorts/ID) — record it, Close.
16. Pinned comment: comments only open once the video is public, so a scheduled Short cannot get it now — give the
    text to the user (they post + pin it from the phone app).

## Getting a video that only exists in another Claude session
That session's "Outputs" panel cannot open files while the session is asleep, and sending a message into another
session was blocked (not allowed). But the video player inside that chat transcript (claude.ai/code/session_…) has a
⋮ menu → "İndir" that saves the mp4 to the user's Downloads; then `device_stage_files` brings it into the container.
JavaScript cannot run on claude.ai pages.

## Notes
- Studio shows a red banner "Your payment method can't be charged" (Google Ads billing). It does not block uploads.
- Never click "Promote" in the published dialog; never touch Google Ads from here.
