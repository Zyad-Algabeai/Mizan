# backend/ai/analyst.py
# Claude-powered analysis. Copied verbatim from the Streamlit version.

import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

_MARKET_CONTEXT = {
    "saudi": {
        "persona": "You are Mizan, an AI financial analyst specialized in the Saudi stock market (Tadawul) and Vision 2030.",
        "currency": "SAR",
        "framework_hint": "Vision 2030 alignment",
        "framework_section": "Vision 2030 Pulse",
        "require_arabic": True,
        "arabic_label": "ملخص السوق",
    },
    "us": {
        "persona": "You are Mizan, an AI financial analyst specialized in the US stock market (S&P 500, Nasdaq, Dow) and macro trends.",
        "currency": "USD",
        "framework_hint": "Federal Reserve policy, earnings momentum, and mega-cap leadership",
        "framework_section": "Fed & Macro Pulse",
        "require_arabic": False,
        "arabic_label": "",
    },
}


def _ctx(market_type):
    return _MARKET_CONTEXT.get(market_type, _MARKET_CONTEXT["saudi"])


def analyze_market(index_hist, sector_data, market_name="TASI", market_type="saudi"):
    ctx = _ctx(market_type)

    latest_close = index_hist["Close"].iloc[-1]
    prev_close = index_hist["Close"].iloc[-2]
    daily_change = ((latest_close - prev_close) / prev_close) * 100

    sector_summary = []
    for sector, stocks in sector_data.items():
        if stocks:
            avg = sum(s["change_pct"] for s in stocks) / len(stocks)
            sector_summary.append(f"{sector}: {avg:+.2f}% avg change")
    sector_text = "\n".join(sector_summary)

    arabic_line = "4. The same summary in Arabic (ملخص السوق)" if ctx["require_arabic"] else ""

    prompt = f"""{ctx['persona']}

Here is today's market data for the {market_name} market:

{market_name} Index:
- Latest Close: {latest_close:.2f} {ctx['currency']}
- Daily Change: {daily_change:+.2f}%

Sector Performance (1 month):
{sector_text}

Please provide:
1. A concise market summary in English (3-4 sentences)
2. Key insight about {ctx['framework_hint']}
3. One risk factor to watch
{arabic_line}

Be direct, professional, and data-driven. No disclaimers."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def analyze_stock(ticker, name, hist, market_type="saudi"):
    ctx = _ctx(market_type)

    latest = hist["Close"].iloc[-1]
    start = hist["Close"].iloc[0]
    change = ((latest - start) / start) * 100
    high = hist["High"].max()
    low = hist["Low"].min()
    avg_volume = hist["Volume"].mean()

    arabic_line = (
        "End with a one-line Arabic summary (التحليل)."
        if ctx["require_arabic"]
        else "Keep the tone tight and US-market-savvy."
    )

    prompt = f"""{ctx['persona']}

Analyze this stock briefly:
- Company: {name} ({ticker})
- Current Price: {latest:.2f} {ctx['currency']}
- 3-Month Change: {change:+.2f}%
- 3-Month High: {high:.2f} {ctx['currency']}
- 3-Month Low: {low:.2f} {ctx['currency']}
- Avg Daily Volume: {avg_volume:,.0f}

Give a 3-sentence analysis: trend, momentum, and one thing to watch.
{arabic_line}"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def analyze_news_sentiment(headlines, market_type="saudi"):
    ctx = _ctx(market_type)
    headlines_text = "\n".join([f"- {h}" for h in headlines])

    arabic_block = (
        "\n\n**التحليل بالعربي:** [2 sentences in Arabic]"
        if ctx["require_arabic"]
        else ""
    )

    prompt = f"""{ctx['persona']}

Analyze the sentiment of these financial headlines:

{headlines_text}

Return your analysis in this exact format:

**Overall Sentiment:** [Bullish 🟢 / Neutral 🟡 / Bearish 🔴]
**Confidence:** [High / Medium / Low]
**Score:** [+1 to -1, e.g. +0.72]

**Key Themes:**
- [theme 1]
- [theme 2]
- [theme 3]

**English Summary:** [2 sentences max]{arabic_block}"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def generate_weekly_brief(index_hist, sector_data, market_name="TASI", market_type="saudi"):
    ctx = _ctx(market_type)

    latest = index_hist["Close"].iloc[-1]
    weekly_change = ((latest - index_hist["Close"].iloc[-6]) / index_hist["Close"].iloc[-6]) * 100
    monthly_change = ((latest - index_hist["Close"].iloc[0]) / index_hist["Close"].iloc[0]) * 100

    sector_summary = []
    for sector, stocks in sector_data.items():
        if stocks:
            avg = sum(s["change_pct"] for s in stocks) / len(stocks)
            sector_summary.append(f"{sector}: {avg:+.1f}%")
    sector_text = "\n".join(sector_summary)

    arabic_section = (
        "7. ملخص الأسبوع (full Arabic summary of all the above)"
        if ctx["require_arabic"]
        else "7. Bottom Line — a 2-sentence trader's takeaway"
    )

    prompt = f"""{ctx['persona']}

Generate a professional weekly market brief for the {market_name} market with this data:

{market_name}: {latest:.2f} {ctx['currency']}
Weekly Change: {weekly_change:+.1f}%
Monthly Change: {monthly_change:+.1f}%

Sector Performance:
{sector_text}

Write a full weekly brief with these sections:
1. Executive Summary (3 sentences)
2. {market_name} Performance Analysis
3. Top Performing Sectors
4. Underperforming Sectors
5. {ctx['framework_section']}
6. Week Ahead — What to Watch
{arabic_section}

Be professional, data-driven, and concise."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text
