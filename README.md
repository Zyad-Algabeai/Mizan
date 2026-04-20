<div align="center">

# Mizan ⚖️

### Saudi & US Market Intelligence — powered by Claude

**Full-stack financial dashboard** with live market data, AI-generated briefs,
candlestick deep dives, sentiment analysis, and a bilingual (English / العربية) output layer.

[![Next.js](https://img.shields.io/badge/Next.js-14-000?logo=next.js&logoColor=white)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![Tailwind](https://img.shields.io/badge/Tailwind-3-38BDF8?logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![Recharts](https://img.shields.io/badge/Recharts-2-22B5BF)](https://recharts.org)
[![Claude](https://img.shields.io/badge/Anthropic-Claude_Sonnet_4.6-D97757?logo=anthropic&logoColor=white)](https://www.anthropic.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

</div>

---

## ✨ What is Mizan?

**Mizan** (Arabic: *ميزان*, "balance/scales") is a production-grade market intelligence dashboard built to explore two markets side by side:

- 🇸🇦 **TASI** — the Tadawul All-Share Index, with a Vision 2030 lens
- 🇺🇸 **US** — S&P 500 / mega-cap coverage with a Fed & macro lens

It pulls **live data from Yahoo Finance**, feeds it to **Claude** for analyst-style commentary, and renders everything in a dark, mobile-first UI that auto-themes between markets (`#00D4AA` green for TASI, `#FF6B35` orange for US).

Originally shipped as a Streamlit prototype (preserved in `streamlit_impl/`), then rebuilt as a real full-stack app — **Next.js on the frontend, FastAPI on the backend** — to match how modern fintech actually ships.

---

## 🖼️ Preview

> Add your own screenshots here after your first run. A few good angles:
> `docs/screens/tasi-overview.png`, `docs/screens/us-candle.png`, `docs/screens/mobile.png`.

```
┌─────────────────────────────────────────────────────────┐
│  ⚖  Mizan · ميزان       [ 🇸🇦 TASI ] 🟢 [ 🇺🇸 US ]         │
├─────────────────────────────────────────────────────────┤
│  LEVEL (SAR)    1-MONTH     TOP SECTOR   WEAKEST        │
│  11,842.30      +2.14%      🏦 Banking   🛒 Retail       │
│  ▲ +0.42%       period      +3.8%        -1.2%          │
├─────────────────────────────────────────────────────────┤
│                                              ┌────────┐ │
│   INDEX CHART (area)                         │ AI     │ │
│   ╱╲     ╱╲╱╲        ╱──╲                    │ BRIEF  │ │
│  ╱  ╲   ╱    ╲    ╱─╯    ╲                   │        │ │
│ ╱    ╲─╱      ╲──╱                           │ Claude │ │
│                                              └────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Features

| # | Feature | What it does |
|---|---|---|
| 1 | **Market overview** | Live index close, daily change, 1-month return — as **big bold metric cards** |
| 2 | **Market toggle** | Smooth 🇸🇦 ↔ 🇺🇸 switch that swaps accents, tickers, sectors, AI persona |
| 3 | **Index chart** | Responsive Recharts area chart with gradient fill in the active accent |
| 4 | **Sector heatmap** | Horizontal bar chart — strong sectors accent-green, weak ones red |
| 5 | **Stock deep dive** | Select any constituent → custom-built candlestick + 4-stat strip + AI analysis |
| 6 | **AI market brief** | Claude writes a 3-sentence English brief + Vision 2030 / Fed pulse call-out |
| 7 | **News sentiment** | Paste headlines, Claude returns `Bullish/Neutral/Bearish` + score `[-1, +1]` |
| 8 | **Weekly brief** | Full editorial brief with exec summary, sector breakdown, "week ahead" — `.md` download |
| 9 | **Arabic output** | TASI mode asks Claude to append Arabic summaries (`ملخص السوق`, `التحليل`) |
| 10 | **Mobile-first** | Works beautifully on phones; charts reflow, metric cards stack, sticky header |

---

## 🏗️ Architecture

```
                     ┌──────────────────────┐
                     │   Next.js 14 (App)   │
                     │   React + Tailwind   │
                     │   Recharts           │
                     └──────────┬───────────┘
                                │
                      REST (JSON) over fetch
                                │
                     ┌──────────▼───────────┐
                     │   FastAPI backend    │
                     │   pydantic schemas   │
                     │   in-memory cache    │
                     └──────┬────────┬──────┘
                            │        │
                    ┌───────▼──┐  ┌──▼───────────┐
                    │ yfinance │  │ Anthropic    │
                    │ (curl_   │  │ Claude API   │
                    │  cffi)   │  │ (Sonnet 4.6) │
                    └──────────┘  └──────────────┘
```

**Design choices worth calling out:**

- **yfinance with `curl_cffi`** — impersonates Chrome's TLS fingerprint so Yahoo's bot-detection doesn't silently break everything. (The default `requests` stopped working in 2024/25.)
- **Synthetic index fallback** — if a real index symbol goes dark (e.g., Nomu), Mizan builds an equal-weighted composite from the constituent tickers so the UI never goes blank.
- **Custom Recharts candlestick** — no heavy `TradingView` lib; a `<Customized>` layer hand-draws OHLC bodies + wicks in the active theme color, keeping bundle size down.
- **CSS variables for theming** — `<html data-market="TASI|US">` flips `--accent` globally; every chart, chip, and glow re-themes instantly with no React re-render churn.
- **In-memory TTL cache** on backend endpoints (60–300s) so the UI doesn't hammer Yahoo.

---

## 🧱 Monorepo layout

```
mizan/
├── backend/                 FastAPI — Python business logic exposed as HTTP
│   ├── main.py              Endpoints, CORS, cache, pydantic schemas
│   ├── config.py            Market registry (tickers, sectors, themes)
│   ├── data/fetcher.py      yfinance + curl_cffi data layer
│   ├── ai/analyst.py        Claude prompts for 4 AI endpoints
│   └── requirements.txt
├── frontend/                Next.js 14 (App Router)
│   ├── app/
│   │   ├── layout.tsx       Root providers, fonts, theme bootstrap
│   │   ├── page.tsx         Main dashboard
│   │   └── globals.css      Tailwind + CSS variables per market
│   ├── components/
│   │   ├── Header.tsx, MarketToggle.tsx, MetricCard.tsx
│   │   ├── IndexChart.tsx, SectorBar.tsx, CandlestickChart.tsx
│   │   ├── MarketBrief.tsx, StockDeepDive.tsx
│   │   ├── NewsSentiment.tsx, WeeklyBrief.tsx, NewsList.tsx
│   │   └── ui/ (Card, Button)
│   ├── contexts/MarketContext.tsx
│   └── lib/ (api, types, format)
├── streamlit_impl/          Original Streamlit prototype (preserved for posterity)
├── .vscode/                 Workspace tasks, launch configs, recommended exts
└── mizan.code-workspace     Multi-root VS Code workspace
```

---

## ⚡ Quick start

Requires **Python 3.11+** (3.13 tested) and **Node 18+**.

### 1. Backend (port 8000)

```bash
cd backend
python -m venv .venv
# Windows:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env       # add your ANTHROPIC_API_KEY
uvicorn main:app --reload --port 8000
```

Swagger UI will be at `http://localhost:8000/docs`.

### 2. Frontend (port 3000)

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

Open `http://localhost:3000`.

### 3. VS Code one-shot

If you open [`mizan.code-workspace`](./mizan.code-workspace), run:
- `Cmd/Ctrl+Shift+P` → **Tasks: Run Task** → `install everything`
- `Cmd/Ctrl+Shift+P` → **Tasks: Run Task** → `🚀 run both (backend + frontend)`

---

## 🔐 Environment variables

**`backend/.env`**
```ini
ANTHROPIC_API_KEY=sk-ant-...
```

**`frontend/.env.local`**
```ini
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Get a Claude API key from [console.anthropic.com](https://console.anthropic.com/settings/keys).

---

## 📡 API reference

All endpoints return JSON. `{market}` ∈ `TASI | US`.

| Method | Path | Notes |
|---|---|---|
| `GET` | `/api/markets` | Market registry (tickers, labels, sectors) |
| `GET` | `/api/markets/{market}/overview?period=1mo` | Index history + daily/monthly deltas |
| `GET` | `/api/markets/{market}/sectors?period=1mo` | Per-sector constituents + avg change |
| `GET` | `/api/markets/{market}/news?limit=15` | Latest news headlines |
| `GET` | `/api/stocks/{ticker}/history?period=3mo` | OHLC history for a single ticker |
| `POST` | `/api/ai/market-brief` | Claude market summary |
| `POST` | `/api/ai/stock-analysis` | Claude stock deep-dive |
| `POST` | `/api/ai/news-sentiment` | Sentiment score for pasted headlines |
| `POST` | `/api/ai/weekly-brief` | Full weekly brief as markdown |

Interactive docs: `http://localhost:8000/docs`

---

## 🌍 Deployment

**Fastest path — Vercel + Render:**

- **Frontend** → push `frontend/` to Vercel. Set `NEXT_PUBLIC_API_URL` to your backend URL.
- **Backend** → push `backend/` to [Render](https://render.com) / [Railway](https://railway.app) / [Fly.io](https://fly.io). Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`. Add `ANTHROPIC_API_KEY` as a secret.

Tighten CORS in `backend/main.py` before going public — the current `allow_origins=["*"]` is convenient for dev but should be locked to your Vercel domain in production.

---

## 🛠️ Built with

- **[Next.js 14](https://nextjs.org)** (App Router, React Server Components, `"use client"` islands)
- **[Tailwind CSS](https://tailwindcss.com)** — custom dark design tokens + CSS-var theming
- **[Recharts](https://recharts.org)** — including a hand-rolled candlestick layer
- **[FastAPI](https://fastapi.tiangolo.com)** + **pydantic** — type-safe backend
- **[yfinance](https://github.com/ranaroussi/yfinance)** + **[curl_cffi](https://github.com/lexiforest/curl_cffi)** — reliable market data via browser impersonation
- **[Anthropic Claude API](https://www.anthropic.com/api)** — `claude-sonnet-4-6` for all AI outputs
- **[Lucide Icons](https://lucide.dev)** · **[IBM Plex Mono](https://fonts.google.com/specimen/IBM+Plex+Mono)** · **[Noto Naskh Arabic](https://fonts.google.com/specimen/Noto+Naskh+Arabic)**

---

## 🗺️ Roadmap

- [ ] Auth + watchlists (per-user saved tickers)
- [ ] WebSocket streaming for intraday ticks (yfinance polls)
- [ ] Portfolio mode — upload positions, track P&L
- [ ] Nomu (parallel market) first-class support
- [ ] Earnings calendar integration
- [ ] Dark → light mode toggle for the 1% who like light mode

---

## 📄 License

MIT — see [LICENSE](./LICENSE).

---

<div align="center">

**Built with respect for the تداول — and a lot of شاي.**

[Report a bug](https://github.com/Zyad-Algabeai/Mizan/issues) · [LinkedIn](https://www.linkedin.com/in/) · [Email](mailto:zezoo6764@gmail.com)

</div>
