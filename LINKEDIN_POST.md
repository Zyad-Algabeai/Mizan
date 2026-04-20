# LinkedIn post — Mizan launch

> **Copy-paste the version you like below.** Character counts are approximate.
> LinkedIn hard-caps posts at ~3,000 characters.

---

## 🔥 Version 1 — The portfolio shipping post (recommended)

Just shipped **Mizan** ⚖️ — a full-stack market intelligence dashboard I built for the Saudi (TASI) and US markets.

It started as a Streamlit prototype. I kept outgrowing it, so I rebuilt it as a real full-stack app — the kind of thing a fintech would actually deploy.

**The stack:**
→ Next.js 14 + Tailwind on the frontend
→ FastAPI + pydantic on the backend
→ yfinance with curl_cffi for reliable market data
→ Anthropic's Claude (Sonnet 4.6) for all AI outputs
→ Recharts, including a hand-rolled candlestick layer

**What it does:**
• Live TASI and S&P 500 coverage with a 🇸🇦 ↔ 🇺🇸 toggle that auto-themes the entire UI (green for TASI, orange for US)
• Big bold metric cards for index level, 1-month return, top/weakest sectors
• Interactive index chart + sector performance heatmap
• Stock deep dives with 3-month candlestick charts
• AI-generated market briefs with a Vision 2030 lens for TASI and a Fed/macro lens for US
• News sentiment analysis — paste headlines, get a bullish/bearish score
• Weekly market brief generator with one-click markdown export
• Bilingual output layer — Claude writes TASI summaries in English *and* Arabic (ملخص السوق)
• Fully responsive, dark-first, mobile-friendly

**A few design calls I'm proud of:**
→ CSS variables on `<html data-market>` let the entire app re-theme without a single React re-render
→ Custom Recharts candlestick instead of importing a 3MB charting library — kept the bundle lean
→ Synthetic index fallback so the UI never goes blank when Yahoo drops a symbol
→ In-memory TTL cache on the backend so the UI stays snappy without hammering Yahoo

It's been a minute since I felt this locked in on a personal project. Shoutout to everyone I was nagging about `curl_cffi` TLS fingerprinting last week — turns out that was the whole game for Yahoo data 😅

Full repo and setup docs below 👇
🔗 https://github.com/Zyad-Algabeai/mizan

Feedback welcome — especially from anyone working in Saudi fintech or trading tools.

#fullstack #nextjs #fastapi #fintech #tadawul #tasi #vision2030 #saudiarabia #claudeai #typescript #python #webdev #datascience

---

## ✨ Version 2 — The shorter, punchier one

Shipped **Mizan** ⚖️ — a Saudi + US market dashboard with live data and AI-generated briefs.

Started as a Streamlit prototype, rebuilt as a full-stack app:
▸ Next.js 14 + Tailwind
▸ FastAPI + pydantic
▸ yfinance + curl_cffi
▸ Claude Sonnet 4.6 for analysis
▸ Custom Recharts candlesticks

**Features:**
• 🇸🇦 ↔ 🇺🇸 market toggle with auto theme swap (TASI green / US orange)
• Index overview, sector heatmap, stock deep dive
• AI market brief + news sentiment + downloadable weekly brief
• Bilingual English / العربية outputs
• Fully responsive dark UI

Biggest lesson: modern Yahoo Finance needs TLS fingerprinting (curl_cffi) to get past Cloudflare. Took me a minute to figure that out.

Code + docs 👉 https://github.com/Zyad-Algabeai/mizan

#fullstack #nextjs #fastapi #fintech #saudi #tasi #vision2030 #claudeai

---

## 🧠 Version 3 — The "what I learned" angle

I just finished **Mizan** ⚖️ — a full-stack market dashboard covering the Saudi (TASI) and US markets, with live data and Claude-generated analysis.

Rebuilding a Streamlit prototype into a real Next.js + FastAPI app taught me more than any tutorial ever did. Three things stuck:

**1. Theming isn't a `useState` job — it's a CSS job.**
Flipping `<html data-market="TASI|US">` updates a single `--accent` CSS variable. The whole app re-themes instantly: cards, charts, chips, glows. Zero React re-render.

**2. Third-party data always finds a way to betray you.**
yfinance was quietly broken against modern Yahoo endpoints. The fix wasn't a different library — it was `curl_cffi` impersonating a Chrome TLS handshake to get past Cloudflare. If your data layer feels flaky, check the network layer first.

**3. Ship the Streamlit version first.**
Streamlit let me validate the product logic in a weekend. Doing the "proper" full-stack rebuild *after* meant every decision — the AI prompts, the sector groupings, the Arabic layer — was already battle-tested.

**Features of the final app:**
• Live TASI & S&P 500 coverage with a market toggle that auto-themes
• Big bold metric cards, area chart index overview, sector heatmap
• Custom candlestick deep dives + Claude-written analysis
• News sentiment scoring + downloadable weekly briefs
• Bilingual English / العربية outputs (ملخص السوق)
• Mobile-responsive dark UI

Built with Next.js 14, Tailwind, FastAPI, pydantic, yfinance, curl_cffi, Recharts, and Claude Sonnet 4.6.

Repo: https://github.com/Zyad-Algabeai/mizan

#fullstack #fintech #webdev #nextjs #fastapi #tasi #vision2030 #claudeai

---

## 📸 Post tips

- **Add a screenshot or short screen-recording.** Posts with visuals get 2-3× engagement. Two frames of the TASI → US toggle animation would slap.
- **Tag people.** @ anyone who helped, any mentors, any Saudi fintech founders / dev relations.
- **Post timing.** Sunday–Tuesday, 9-11am Riyadh time is the sweet spot for MENA tech.
- **First comment = link drop.** LinkedIn suppresses external links in the post body. Put the GitHub link in the first comment instead, then edit the post to say "repo in comments 👇".
