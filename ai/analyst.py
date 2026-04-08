# ai/analyst.py
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def analyze_market(tasi_hist, sector_data):
    """Generate AI market analysis in English + Arabic."""

    # Build a summary of the data to send to Claude
    latest_close = tasi_hist["Close"].iloc[-1]
    prev_close = tasi_hist["Close"].iloc[-2]
    tasi_change = ((latest_close - prev_close) / prev_close) * 100

    # Summarize sector performance
    sector_summary = []
    for sector, stocks in sector_data.items():
        if stocks:
            avg_change = sum(s["change_pct"] for s in stocks) / len(stocks)
            sector_summary.append(f"{sector}: {avg_change:+.2f}% avg change")

    sector_text = "\n".join(sector_summary)

    prompt = f"""You are Mizan, an AI financial analyst specialized in the Saudi stock market (Tadawul) and Vision 2030.

Here is today's market data:

TASI Index:
- Latest Close: {latest_close:.2f} SAR
- Daily Change: {tasi_change:+.2f}%

Sector Performance (1 month):
{sector_text}

Please provide:
1. A concise market summary in English (3-4 sentences)
2. Key insight about Vision 2030 sector performance
3. One risk factor to watch
4. The same summary in Arabic (ملخص السوق)

Be direct, professional, and data-driven. No disclaimers."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text


def analyze_stock(ticker, name, hist):
    """Generate AI analysis for a single stock."""

    latest = hist["Close"].iloc[-1]
    start = hist["Close"].iloc[0]
    change = ((latest - start) / start) * 100
    high = hist["High"].max()
    low = hist["Low"].min()
    avg_volume = hist["Volume"].mean()

    prompt = f"""You are Mizan, an AI analyst for the Saudi stock market.

Analyze this stock briefly:
- Company: {name} ({ticker})
- Current Price: {latest:.2f} SAR
- 3-Month Change: {change:+.2f}%
- 3-Month High: {high:.2f} SAR
- 3-Month Low: {low:.2f} SAR
- Avg Daily Volume: {avg_volume:,.0f}

Give a 3-sentence analysis: trend, momentum, and one thing to watch.
End with a one-line Arabic summary (التحليل)."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text