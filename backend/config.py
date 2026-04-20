# backend/config.py
# Market registry — copied from legacy Streamlit config.
# Keep this file in sync with any sector changes.

# --- Index symbols (Yahoo Finance) ---
TASI_INDEX = "^TASI.SR"
US_INDEX = "^GSPC"  # S&P 500

# --- TASI Main Market sectors ---
TASI_SECTORS = {
    "🏦 Banking & Finance": {
        "tickers": ["1120.SR", "1180.SR", "1010.SR", "1150.SR"],
        "names": ["Al Rajhi Bank", "Al Jazira Bank", "Riyad Bank", "Alinma Bank"],
        "vision2030": True,
    },
    "⚡ Energy & Utilities": {
        "tickers": ["2222.SR", "5110.SR"],
        "names": ["Saudi Aramco", "Saudi Electricity"],
        "vision2030": True,
    },
    "📡 Telecom & Tech": {
        "tickers": ["7010.SR", "7020.SR", "7030.SR"],
        "names": ["STC", "Mobily", "Zain Saudi"],
        "vision2030": True,
    },
    "⛏️ Mining & Materials": {
        "tickers": ["1211.SR", "2010.SR"],
        "names": ["Ma'aden", "SABIC"],
        "vision2030": True,
    },
    "🏥 Healthcare": {
        "tickers": ["4002.SR", "4007.SR"],
        "names": ["Al Hammadi", "Saudi German Health"],
        "vision2030": True,
    },
    "🛒 Retail & Consumer": {
        "tickers": ["4190.SR", "4240.SR"],
        "names": ["Jarir Marketing", "Aldrees Petroleum"],
        "vision2030": False,
    },
}

# --- US Market sectors (S&P 500 + friends) ---
US_SECTORS = {
    "💻 Technology": {
        "tickers": ["AAPL", "MSFT", "NVDA", "GOOGL", "META"],
        "names": ["Apple", "Microsoft", "NVIDIA", "Alphabet", "Meta"],
        "megacap": True,
    },
    "🏦 Financials": {
        "tickers": ["JPM", "BAC", "GS", "MS", "WFC"],
        "names": ["JPMorgan", "Bank of America", "Goldman Sachs", "Morgan Stanley", "Wells Fargo"],
        "megacap": True,
    },
    "⚡ Energy": {
        "tickers": ["XOM", "CVX", "COP"],
        "names": ["ExxonMobil", "Chevron", "ConocoPhillips"],
        "megacap": False,
    },
    "🏥 Healthcare": {
        "tickers": ["JNJ", "UNH", "LLY", "PFE"],
        "names": ["Johnson & Johnson", "UnitedHealth", "Eli Lilly", "Pfizer"],
        "megacap": True,
    },
    "🛒 Consumer": {
        "tickers": ["AMZN", "WMT", "HD", "MCD", "NKE"],
        "names": ["Amazon", "Walmart", "Home Depot", "McDonald's", "Nike"],
        "megacap": True,
    },
    "🏗️ Industrial": {
        "tickers": ["CAT", "BA", "HON"],
        "names": ["Caterpillar", "Boeing", "Honeywell"],
        "megacap": False,
    },
}

MARKETS = {
    "TASI": {
        "label": "TASI (Main Market)",
        "index": TASI_INDEX,
        "sectors": TASI_SECTORS,
        "flag_key": "vision2030",
        "flag_label": "Vision 2030",
        "market_type": "saudi",
        "currency": "SAR",
    },
    "US": {
        "label": "S&P 500 (US Market)",
        "index": US_INDEX,
        "sectors": US_SECTORS,
        "flag_key": "megacap",
        "flag_label": "Mega-cap",
        "market_type": "us",
        "currency": "USD",
    },
}
