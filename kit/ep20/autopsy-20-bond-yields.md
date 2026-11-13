# Autopsy #20 — "Bond yields hit 5%. Sell stocks?" (slot A 17:30, 2026-11-13) — TREND

## Trend kaynağı
- 12 Kasım 2026: ABD 10 yıllık tahvil faizi %5,12'ye çıktı (Salı %4,98'den; Çarşamba Veterans Day tatili). S&P 500 -%0,4 → 7.592,40 (AP / Boston Globe "Wall Street shakes with swings for Nvidia and oil prices…", 12 Kas 2026). 13 Kasım: 10y ~%5,13, CME FedWatch Aralık'ta 50 bp artırım ihtimali %12 (Le Private Banker, 13 Kas 2026; Rio Times "US 10-Year Yield Tops 5%").
- 1 yıl önce: FRED DGS10 2025-11-12 = %4,08 → +1,04 puan ("up a full point in one year").
- Subscribr: "stock market this week / what to do now" (14 gün, ≤90 sn, outlier ≥2,5) 10/10 kazanan: "Investing at All-Time Highs: Bill Ackman's Advice" (Equity Mates, 47 sn, 21K, 4,3×), "WTF Just Happened: the TRUTH about Semiconductor Stocks Tanking" (155K, 3,5×). "bond yields 5% stocks" (30 gün): tek sonuç Howard Marks "The S&P 500 isn't a good bet right now" (51 sn, 267K, 3,3×) — faiz/değerleme korkusu ilgi çekiyor.

## Kural (backtest)
- Veri: SPY 2005–2024 (kit/spy.csv) + 10y faiz FRED DGS10 (günlük kapanış, ffill; kit/ep20/dgs10.csv).
- Kural: 10y faiz 252 işlem günü öncesine göre ≥ +1,00 puan yukarıdaysa nakit (0%), değilse SPY. Sinyal kapanışta → ertesi açılışta dolum, %0,05/taraf, $10.000. Isınma 252 bar → başlangıç 2006-01-04; al-tut aynı tarihten.
- Sonuç: kural $58.226 (CAGR %9,72, max DD -%55,2, piyasada %89,4, 40 işlem, %60 kazanan) vs al-tut $66.114 (CAGR %10,46, max DD -%55,2). Ücret stresi: %0,10 → $55.913, %0,20 → $51.557, ücretsiz $60.633.
- Yıllar: 2008 -%36,2 vs -%36,2 (faizler düştü, kural içerideydi); 2013 +%12,9 vs +%29,0; 2022 -%6,8 vs -%18,6 (Nisan 2022 → Nisan 2023 nakitte); 2022 sonu $41.290 vs $41.957 (neredeyse yakaladı); 2023 +%14,2 vs +%26,7.
- DÜRÜSTLÜK / parametre hassasiyeti: eşik +0,5 → $34.687, +0,75 → $46.120, +1,0 → $58.226, +1,25 → $73.271 (kazanır), +1,5 → $75.172 (kazanır), +2,0 → $69.866. → Videoda ekranda dipnot + son cümle "Nudge the trigger, and the winner can flip."

## Senaryo (135 kelime, 49,5 sn; "Final" öncesi %84; Remember %55; yarış "B"de 10,0 sn = %20)
[intense] The ten-year Treasury yield just topped five percent. It's up a full point in one year. So, do you sell stocks when yields spike? A: sell and hide. B: just hold. But one year hides the real answer. The rule: when the yield jumps a full point in a year, go to cash. Two thousand eight: yields fell, so the rule stayed in and crashed with everyone. Twenty thirteen: yields jump, it sells, and catches less than half the rally. [curious] Remember that one year? Twenty twenty-two. Yields exploded. The rule hid in cash and lost seven percent. Holders lost nineteen. It almost caught up. Then twenty twenty-three: out again, with half the rally. [dramatic] Final score. Yield rule: fifty-eight thousand two hundred. Just holding: sixty-six thousand one hundred. Nudge the trigger, and the winner can flip.

- Hook: ilk cümle haber + "It's up a full point in one year." · Gizli unsur: "one year" → 2022.
- Frame 0: "5%" dev + "SELL?" + 10-YEAR TREASURY YIELD etiketi + basınç göstergesi, Rocco dedektif şok.
- Sahneler: hook → +1 puan çubukları (4,08% → 5,12%) → soru → A/B + yarış → ipucu (EVIDENCE: THE YEAR 20??) → kural kartları → 2008 → 2013 (nakit bantları) → Remember/2022 + gerçek faiz çizgisi → 2022 çubukları -7/-19 → "almost caught up" + 2023 → final skor (dipnot: +0,5 / +1,25 eşik) → hüküm damgaları → loop.
- Müzik: lofi → trap ("Remember that one year?") → synthwave (final skor).
- Kapak başlığı: "THEN RATES EXPLODED." · alt soru "SELL OR HOLD?"
- Başlıklar: [HYPE] Bond Yields Just Hit 5%. Should You SELL Stocks? · [SAFE] Do You Sell Stocks When Bond Yields Spike?
- Ses: -14,1 LUFS / -1,7 dBTP; 1080x1920; 49,5 sn.

## Yükleme metinleri
- Açıklama: The 10-year Treasury yield closed at 5.12% on Nov 12, 2026 — up about a full point in a year. / So do you sell stocks when yields spike? One simple rule says yes. / I ran it on 19 years of SPY. One year hides the real answer. / Backtest: SPY 2006–2024, next-day open fills, 0.05% costs. Yield data: FRED DGS10. Not a recommendation — just an autopsy. #shorts #trading #backtest
- Etiketler: bond yields 5%, 10 year treasury yield, treasury yields, rising yields stocks, should i sell stocks, interest rates stock market, yields spike, bond market selloff, stock market today, sp500, spy, backtest, trading strategy, investing, stock market, strategy autopsy
- Sabitlenmiş yorum: Your guess before the reveal: A) sell when yields spike or B) just hold? Drop A or B 👇 Which market fear should I autopsy next?
- Oynatma listeleri: All Cases + Timing & Calendar Myths
- Reels: The 10-year yield just topped 5%. Do you sell stocks when yields spike? I backtested a simple "yield alarm" rule on 19 years of SPY. Guess A or B before the reveal 👇 #stockmarket #investing #bonds #interestrates #backtest
- Kit: kit/ep20/ (bt20.py + dgs10.csv, s20_* modülleri, audio_20.py, cover20.py).
