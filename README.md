# ⚖️ Mizan | ميزان
> AI-Powered Saudi Market Intelligence • تحليل ذكي لسوق الأسهم السعودي

Mizan is an open-source dashboard that combines live Tadawul (Saudi Stock Exchange) data with Claude AI to generate bilingual market analysis in English and Arabic.

## Features
- 📈 Live TASI index tracking with interactive charts
- 🏢 Sector performance breakdown (Vision 2030 aligned)
- 🤖 AI-generated market briefs in English + Arabic
- 🕯️ Candlestick charts for individual stock deep dives
- ⚡ Built on real-time data from Yahoo Finance

## Tech Stack
- Python, Streamlit, Plotly
- yfinance for Tadawul data
- Anthropic Claude API for AI analysis

## Setup
```bash
git clone https://github.com/Zyad-Algabeai/Mizan.git
cd Mizan
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Add your API key to `.env`:
ANTHROPIC_API_KEY=your_key_here

Run:
```bash
streamlit run app.py
```

## Data Sources
- Saudi Exchange (Tadawul) via Yahoo Finance
- Anthropic Claude for AI analysis
