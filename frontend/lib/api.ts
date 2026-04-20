// lib/api.ts — thin fetch wrapper around the FastAPI backend.

import type {
  MarketsResponse,
  MarketOverview,
  SectorsResponse,
  NewsResponse,
  StockHistory,
  MarketCode,
  MarketType,
} from "./types";

const BASE =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ||
  "http://localhost:8000";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`, { cache: "no-store" });
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`GET ${path} → ${res.status} ${body}`);
  }
  return res.json() as Promise<T>;
}

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`POST ${path} → ${res.status} ${text}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  markets: () => get<MarketsResponse>("/api/markets"),
  overview: (market: MarketCode, period = "1mo") =>
    get<MarketOverview>(`/api/markets/${market}/overview?period=${period}`),
  sectors: (market: MarketCode, period = "1mo") =>
    get<SectorsResponse>(`/api/markets/${market}/sectors?period=${period}`),
  news: (market: MarketCode, limit = 12) =>
    get<NewsResponse>(`/api/markets/${market}/news?limit=${limit}`),
  stock: (ticker: string, period = "3mo") =>
    get<StockHistory>(`/api/stocks/${encodeURIComponent(ticker)}/history?period=${period}`),

  marketBrief: (market: MarketCode, period = "1mo") =>
    post<{ market: MarketCode; text: string }>("/api/ai/market-brief", {
      market,
      period,
    }),
  stockAnalysis: (payload: {
    ticker: string;
    name: string;
    period?: string;
    market_type: MarketType;
  }) => post<{ ticker: string; text: string }>("/api/ai/stock-analysis", payload),
  newsSentiment: (headlines: string[], market_type: MarketType) =>
    post<{ text: string }>("/api/ai/news-sentiment", { headlines, market_type }),
  weeklyBrief: (market: MarketCode, period = "1mo") =>
    post<{ market: MarketCode; text: string }>("/api/ai/weekly-brief", {
      market,
      period,
    }),
};

export const API_BASE = BASE;
