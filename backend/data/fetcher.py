# backend/data/fetcher.py
# Live market data via yfinance, with a curl_cffi browser session so Yahoo's
# anti-bot blocks don't kill every request.

import pandas as pd
import yfinance as yf
from config import MARKETS

# Set up a browser-impersonating session. curl_cffi mimics a real Chrome TLS
# fingerprint, which is currently what yfinance needs to get past Yahoo's
# Cloudflare protection. Falls back to plain requests if unavailable.
try:
    from curl_cffi import requests as curl_requests
    _SESSION = curl_requests.Session(impersonate="chrome")
except Exception:  # curl_cffi missing or broken
    _SESSION = None


def _ticker(symbol: str):
    """yf.Ticker with our impersonating session when available."""
    if _SESSION is not None:
        return yf.Ticker(symbol, session=_SESSION)
    return yf.Ticker(symbol)


def _build_synthetic_index(sectors, period="1mo"):
    """Build a synthetic equal-weighted index from constituent tickers."""
    closes, volumes, resolved = [], [], []
    for details in sectors.values():
        for ticker in details["tickers"]:
            try:
                h = _ticker(ticker).history(period=period)
                if h is not None and not h.empty and "Close" in h.columns:
                    closes.append(h["Close"].rename(ticker))
                    volumes.append(h["Volume"].rename(ticker))
                    resolved.append(ticker)
            except Exception as e:
                print(f"[synthetic-index] skipping {ticker}: {e}")

    if not closes:
        return pd.DataFrame(), resolved

    close_df = pd.concat(closes, axis=1).ffill()
    vol_df = pd.concat(volumes, axis=1).fillna(0)
    first_row = close_df.bfill().iloc[0]
    normalized = close_df.div(first_row) * 100
    idx_close = normalized.mean(axis=1)

    synthetic = pd.DataFrame({
        "Open": idx_close,
        "High": normalized.max(axis=1),
        "Low": normalized.min(axis=1),
        "Close": idx_close,
        "Volume": vol_df.sum(axis=1).astype("int64"),
    }).dropna(how="all")

    return synthetic, resolved


def get_market_overview(period="1mo", market="TASI"):
    """Fetch index history + info for the selected market."""
    index_symbol = MARKETS[market]["index"]
    meta = {"synthetic": False, "resolved": [], "index_symbol": index_symbol}

    idx = _ticker(index_symbol)
    try:
        hist = idx.history(period=period)
    except Exception as e:
        print(f"[overview] index fetch failed for {index_symbol}: {e}")
        hist = pd.DataFrame()

    try:
        info = idx.info if hist is not None and not hist.empty else {}
    except Exception:
        info = {}

    if hist is None or hist.empty:
        hist, resolved = _build_synthetic_index(MARKETS[market]["sectors"], period=period)
        meta["synthetic"] = True
        meta["resolved"] = resolved

    return hist, info, meta


def get_sector_data(period="1mo", market="TASI"):
    """Return per-sector stock data for the selected market."""
    market_cfg = MARKETS[market]
    sectors = market_cfg["sectors"]
    flag_key = market_cfg["flag_key"]

    results = {}
    for sector, details in sectors.items():
        sector_stocks = []
        flag_value = details.get(flag_key, False)
        for ticker, name in zip(details["tickers"], details["names"]):
            try:
                stock = _ticker(ticker)
                hist = stock.history(period=period)
                if not hist.empty:
                    latest = hist["Close"].iloc[-1]
                    start = hist["Close"].iloc[0]
                    change_pct = ((latest - start) / start) * 100
                    sector_stocks.append({
                        "ticker": ticker,
                        "name": name,
                        "price": round(float(latest), 2),
                        "change_pct": round(float(change_pct), 1),
                        "flag": bool(flag_value),
                        "vision2030": bool(flag_value),
                    })
            except Exception as e:
                print(f"Error fetching {ticker}: {e}")
        results[sector] = sector_stocks
    return results


def get_stock_history(ticker, period="3mo"):
    stock = _ticker(ticker)
    return stock.history(period=period)


def get_market_news(limit=15, market="TASI"):
    """Fetch latest market news via yfinance for the selected market."""
    from datetime import datetime

    market_cfg = MARKETS[market]
    news_sources = [market_cfg["index"]] + [
        details["tickers"][0]
        for details in market_cfg["sectors"].values()
        if details["tickers"]
    ]

    seen, items = set(), []
    for ticker_symbol in news_sources:
        try:
            news = _ticker(ticker_symbol).news or []
        except Exception as e:
            print(f"Error fetching news for {ticker_symbol}: {e}")
            continue

        for n in news:
            content = n.get("content", n)
            title = content.get("title") or n.get("title")
            if not title or title in seen:
                continue
            seen.add(title)

            publisher = (
                content.get("provider", {}).get("displayName")
                or n.get("publisher")
                or "Unknown"
            )
            link = (
                content.get("canonicalUrl", {}).get("url")
                or content.get("clickThroughUrl", {}).get("url")
                or n.get("link")
                or ""
            )
            pub_date = content.get("pubDate") or n.get("providerPublishTime")
            if isinstance(pub_date, (int, float)):
                pub_date = datetime.fromtimestamp(pub_date).isoformat()

            items.append({
                "title": title,
                "publisher": publisher,
                "link": link,
                "published": pub_date or "",
                "ticker": ticker_symbol,
            })

    items.sort(key=lambda x: x["published"] or "", reverse=True)
    return items[:limit]
