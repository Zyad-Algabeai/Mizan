// Shared types for the Mizan dashboard.

export type MarketCode = "TASI" | "US";
export type MarketType = "saudi" | "us";

export interface MarketInfo {
  label: string;
  index: string;
  currency: "SAR" | "USD";
  market_type: MarketType;
  flag_label: string;
  sectors: string[];
}

export interface MarketsResponse {
  [key: string]: MarketInfo;
}

export interface OHLCPoint {
  date: string;
  open: number | null;
  high: number | null;
  low: number | null;
  close: number | null;
  volume: number;
}

export interface MarketOverview {
  market: MarketCode;
  period: string;
  index_symbol: string;
  synthetic: boolean;
  resolved: string[];
  currency: string;
  series: OHLCPoint[];
  latest: number | null;
  previous: number | null;
  daily_change_pct: number | null;
  monthly_change_pct: number | null;
  info: { longName?: string; symbol?: string };
}

export interface SectorStock {
  ticker: string;
  name: string;
  price: number;
  change_pct: number;
  flag: boolean;
  vision2030: boolean;
}

export interface SectorEntry {
  sector: string;
  avg_change_pct: number;
  stocks: SectorStock[];
}

export interface SectorsResponse {
  market: MarketCode;
  period: string;
  flag_label: string;
  sectors: SectorEntry[];
}

export interface NewsItem {
  title: string;
  publisher: string;
  link: string;
  published: string;
  ticker: string;
}

export interface NewsResponse {
  market: MarketCode;
  items: NewsItem[];
}

export interface StockHistory {
  ticker: string;
  period: string;
  series: OHLCPoint[];
  latest: number | null;
  start: number | null;
  change_pct: number | null;
  high: number | null;
  low: number | null;
  avg_volume: number | null;
}
