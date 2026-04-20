# backend/main.py
# FastAPI wrapper around the existing Mizan Python logic.
# Run: uvicorn main:app --reload --port 8000

from __future__ import annotations

from typing import List, Optional
from functools import lru_cache
import math
import time

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from config import MARKETS
from data.fetcher import (
    get_market_overview,
    get_sector_data,
    get_stock_history,
    get_market_news,
)
from ai.analyst import (
    analyze_market,
    analyze_stock,
    analyze_news_sentiment,
    generate_weekly_brief,
)

# ---------------------------------------------------------------------------

app = FastAPI(
    title="Mizan Markets API",
    description="Live TASI & US market data + Claude-powered analysis.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock down to your frontend domain in prod
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Tiny in-memory cache so the frontend doesn't hammer Yahoo on every re-render.
# Keyed by (fn_name, *args). TTL in seconds.

_CACHE: dict = {}

def _cached(key: tuple, ttl: int, producer):
    now = time.time()
    hit = _CACHE.get(key)
    if hit and (now - hit[0]) < ttl:
        return hit[1]
    value = producer()
    _CACHE[key] = (now, value)
    return value


def _clean_float(x):
    """Drop NaN/Inf so the JSON serializer doesn't choke."""
    try:
        f = float(x)
        if math.isnan(f) or math.isinf(f):
            return None
        return f
    except (TypeError, ValueError):
        return None


def _df_to_records(df):
    """Convert an OHLC DataFrame to JSON-safe records."""
    if df is None or df.empty:
        return []
    out = df.reset_index().copy()
    # Normalize the date column name
    date_col = out.columns[0]
    out = out.rename(columns={date_col: "date"})
    out["date"] = out["date"].astype(str)

    records = []
    for row in out.to_dict(orient="records"):
        records.append({
            "date": row.get("date"),
            "open": _clean_float(row.get("Open")),
            "high": _clean_float(row.get("High")),
            "low": _clean_float(row.get("Low")),
            "close": _clean_float(row.get("Close")),
            "volume": _clean_float(row.get("Volume")) or 0,
        })
    return records


def _ensure_market(market: str) -> str:
    market = market.upper()
    if market not in MARKETS:
        raise HTTPException(status_code=404, detail=f"Unknown market: {market}")
    return market


# ---------------------------------------------------------------------------
# Schemas

class MarketBriefRequest(BaseModel):
    market: str = Field(default="TASI")
    period: str = Field(default="1mo")


class StockAnalysisRequest(BaseModel):
    ticker: str
    name: str
    period: str = Field(default="3mo")
    market_type: str = Field(default="saudi")


class NewsSentimentRequest(BaseModel):
    headlines: List[str]
    market_type: str = Field(default="saudi")


class WeeklyBriefRequest(BaseModel):
    market: str = Field(default="TASI")
    period: str = Field(default="1mo")


# ---------------------------------------------------------------------------
# Meta

@app.get("/")
def root():
    return {
        "name": "Mizan Markets API",
        "markets": list(MARKETS.keys()),
        "docs": "/docs",
    }


@app.get("/api/markets")
def list_markets():
    """Expose market registry (without heavy sector lookups) for the frontend."""
    return {
        code: {
            "label": cfg["label"],
            "index": cfg["index"],
            "currency": cfg["currency"],
            "market_type": cfg["market_type"],
            "flag_label": cfg["flag_label"],
            "sectors": list(cfg["sectors"].keys()),
        }
        for code, cfg in MARKETS.items()
    }


# ---------------------------------------------------------------------------
# Market data

@app.get("/api/markets/{market}/overview")
def market_overview(market: str, period: str = Query("1mo")):
    market = _ensure_market(market)

    def produce():
        hist, info, meta = get_market_overview(period=period, market=market)
        series = _df_to_records(hist)

        latest = series[-1]["close"] if series else None
        prev = series[-2]["close"] if len(series) > 1 else None
        daily_change_pct = None
        if latest is not None and prev not in (None, 0):
            daily_change_pct = ((latest - prev) / prev) * 100

        month_start = series[0]["close"] if series else None
        monthly_change_pct = None
        if latest is not None and month_start not in (None, 0):
            monthly_change_pct = ((latest - month_start) / month_start) * 100

        return {
            "market": market,
            "period": period,
            "index_symbol": meta.get("index_symbol"),
            "synthetic": meta.get("synthetic", False),
            "resolved": meta.get("resolved", []),
            "currency": MARKETS[market]["currency"],
            "series": series,
            "latest": _clean_float(latest),
            "previous": _clean_float(prev),
            "daily_change_pct": _clean_float(daily_change_pct),
            "monthly_change_pct": _clean_float(monthly_change_pct),
            "info": {
                "longName": info.get("longName") if info else None,
                "symbol": info.get("symbol") if info else None,
            } if info else {},
        }

    return _cached(("overview", market, period), ttl=60, producer=produce)


@app.get("/api/markets/{market}/sectors")
def market_sectors(market: str, period: str = Query("1mo")):
    market = _ensure_market(market)

    def produce():
        raw = get_sector_data(period=period, market=market)
        sectors = []
        for sector_name, stocks in raw.items():
            if not stocks:
                continue
            avg_change = sum(s["change_pct"] for s in stocks) / len(stocks)
            sectors.append({
                "sector": sector_name,
                "avg_change_pct": round(float(avg_change), 2),
                "stocks": stocks,
            })
        # Sort: strongest sector first
        sectors.sort(key=lambda s: s["avg_change_pct"], reverse=True)
        return {
            "market": market,
            "period": period,
            "flag_label": MARKETS[market]["flag_label"],
            "sectors": sectors,
        }

    return _cached(("sectors", market, period), ttl=120, producer=produce)


@app.get("/api/markets/{market}/news")
def market_news(market: str, limit: int = Query(15, ge=1, le=50)):
    market = _ensure_market(market)
    def produce():
        return {"market": market, "items": get_market_news(limit=limit, market=market)}
    return _cached(("news", market, limit), ttl=300, producer=produce)


@app.get("/api/stocks/{ticker}/history")
def stock_history(ticker: str, period: str = Query("3mo")):
    def produce():
        try:
            hist = get_stock_history(ticker, period=period)
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Fetch failed: {e}")

        if hist is None or hist.empty:
            raise HTTPException(status_code=404, detail=f"No data for {ticker}")

        series = _df_to_records(hist)
        latest = series[-1]["close"] if series else None
        start = series[0]["close"] if series else None
        change_pct = None
        if latest is not None and start not in (None, 0):
            change_pct = ((latest - start) / start) * 100

        highs = [r["high"] for r in series if r["high"] is not None]
        lows = [r["low"] for r in series if r["low"] is not None]
        vols = [r["volume"] for r in series if r["volume"] is not None]

        return {
            "ticker": ticker,
            "period": period,
            "series": series,
            "latest": _clean_float(latest),
            "start": _clean_float(start),
            "change_pct": _clean_float(change_pct),
            "high": _clean_float(max(highs)) if highs else None,
            "low": _clean_float(min(lows)) if lows else None,
            "avg_volume": _clean_float(sum(vols) / len(vols)) if vols else None,
        }

    return _cached(("stock", ticker, period), ttl=120, producer=produce)


# ---------------------------------------------------------------------------
# AI endpoints

@app.post("/api/ai/market-brief")
def ai_market_brief(req: MarketBriefRequest):
    market = _ensure_market(req.market)
    try:
        hist, _info, _meta = get_market_overview(period=req.period, market=market)
        if hist is None or hist.empty:
            raise HTTPException(status_code=503, detail="No market data available")
        sectors = get_sector_data(period=req.period, market=market)
        text = analyze_market(
            hist,
            sectors,
            market_name=market,
            market_type=MARKETS[market]["market_type"],
        )
        return {"market": market, "text": text}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI brief failed: {e}")


@app.post("/api/ai/stock-analysis")
def ai_stock_analysis(req: StockAnalysisRequest):
    try:
        hist = get_stock_history(req.ticker, period=req.period)
        if hist is None or hist.empty:
            raise HTTPException(status_code=404, detail=f"No data for {req.ticker}")
        text = analyze_stock(req.ticker, req.name, hist, market_type=req.market_type)
        return {"ticker": req.ticker, "text": text}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI stock analysis failed: {e}")


@app.post("/api/ai/news-sentiment")
def ai_news_sentiment(req: NewsSentimentRequest):
    if not req.headlines or not any(h.strip() for h in req.headlines):
        raise HTTPException(status_code=400, detail="Provide at least one headline")
    try:
        text = analyze_news_sentiment(req.headlines, market_type=req.market_type)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {e}")


@app.post("/api/ai/weekly-brief")
def ai_weekly_brief(req: WeeklyBriefRequest):
    market = _ensure_market(req.market)
    try:
        hist, _info, _meta = get_market_overview(period=req.period, market=market)
        if hist is None or hist.empty:
            raise HTTPException(status_code=503, detail="No market data available")
        sectors = get_sector_data(period=req.period, market=market)
        text = generate_weekly_brief(
            hist,
            sectors,
            market_name=market,
            market_type=MARKETS[market]["market_type"],
        )
        return {"market": market, "text": text}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weekly brief failed: {e}")
