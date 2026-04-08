# data/fetcher.py
import yfinance as yf
from config import TASI_INDEX, SECTORS

def get_tasi_overview(period="1mo"):
    tasi = yf.Ticker(TASI_INDEX)
    hist = tasi.history(period=period)
    info = tasi.info
    return hist, info

def get_sector_data(period="1mo"):
    results = {}
    for sector, details in SECTORS.items():
        sector_stocks = []
        for ticker, name in zip(details["tickers"], details["names"]):
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period=period)
                if not hist.empty:
                    latest = hist["Close"].iloc[-1]
                    start = hist["Close"].iloc[0]
                    change_pct = ((latest - start) / start) * 100
                    sector_stocks.append({
                        "ticker": ticker,
                        "name": name,
                        "price": round(latest, 2),
                        "change_pct": round(change_pct, 1),
                        "vision2030": details["vision2030"]
                    })
            except Exception as e:
                print(f"Error fetching {ticker}: {e}")
        results[sector] = sector_stocks
    return results

def get_stock_history(ticker, period="3mo"):
    stock = yf.Ticker(ticker)
    return stock.history(period=period)