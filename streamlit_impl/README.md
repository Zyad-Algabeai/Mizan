# Mizan — Streamlit implementation of the redesign

Drop these two files into your existing project alongside your `config.py`, `data/`, and `ai/` modules:

- **`app.py`** — replaces your current top-level `app.py`.
- **`theme.py`** — new file. Holds the Mizan design tokens (`THEMES` dict) and the `inject_theme()` function that injects the full CSS.

## Install order

1. Place `theme.py` next to `config.py`.
2. Replace your current `app.py` with the one here.
3. Your existing imports stay the same:
   - `from config import MARKETS`
   - `from data.fetcher import get_market_overview, get_sector_data, get_stock_history, get_market_news`
   - `from ai.analyst import analyze_market, analyze_stock, analyze_news_sentiment, generate_weekly_brief`
4. Run: `streamlit run app.py`

## What's new

- **Editorial type system** — Instrument Serif (headlines/numbers) + IBM Plex Sans/Mono + IBM Plex Sans Arabic for RTL. Loaded via Google Fonts in `inject_theme()`.
- **Two themes, one toggle** — TASI (emerald-on-deep-green, `#00D4AA`) / US (orange-on-navy, `#FF6B35`). Toggle in the header triggers `st.rerun()` with new CSS.
- **Language toggle** — `ع` / `EN` button in the header. Flips direction and swaps headings / section labels to Arabic.
- **Title strip** — big serif headline with live `● OPEN` status, session hours, and YTD.
- **Metric cards** — restyled native `st.metric` (outlined, mono label with accent square, big serif numbers).
- **Editorial news list** — serif headlines with ticker chips, linked titles, AI sentiment panel.
- **Sector heatmap** — weighted grid using `color-mix(in oklab, …)` (the `oklab` part is important; `oklch` cycles through purple when mixing orange with navy).
- **Editorial briefs layout** — two-column with a main body and a "By the numbers" aside.
- **Live footer** — pulsing dot + `Last updated HH:MM:SS`.

## Notes / follow-ups

- The title strip renders `ytd_pct` as `monthly_change * 2.2` as a placeholder — **wire this to your real YTD calc in `get_market_overview`** when you're ready.
- The sector heatmap sizes tiles by # of resolved constituents. If your `config.py` exposes index weights, swap `r['Count']` for weight to match the HTML prototype exactly.
- If you want the theme swap to feel instant (no full rerun), you could keep the CSS in a single `inject_theme` block and drive variant colors via `data-market` on `.block-container` — but Streamlit's rerun model means the current approach is simpler and still smooth.
- The language toggle currently only translates a handful of labels. Extend with a small `i18n.py` dict if you want full Arabic coverage.
