"use client";

import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
  ReactNode,
} from "react";
import type { MarketCode, MarketType } from "@/lib/types";

interface MarketContextValue {
  market: MarketCode;
  marketType: MarketType;
  currency: "SAR" | "USD";
  accent: string;
  flag: string;
  flagLabel: string;
  setMarket: (m: MarketCode) => void;
  toggleMarket: () => void;
}

const MarketContext = createContext<MarketContextValue | null>(null);

const META: Record<
  MarketCode,
  { type: MarketType; currency: "SAR" | "USD"; accent: string; flag: string; flagLabel: string }
> = {
  TASI: {
    type: "saudi",
    currency: "SAR",
    accent: "#00D4AA",
    flag: "🇸🇦",
    flagLabel: "Vision 2030",
  },
  US: {
    type: "us",
    currency: "USD",
    accent: "#FF6B35",
    flag: "🇺🇸",
    flagLabel: "Mega-cap",
  },
};

export function MarketProvider({ children }: { children: ReactNode }) {
  const [market, setMarket] = useState<MarketCode>("TASI");

  // Sync <html data-market="..."> so CSS variables update globally.
  useEffect(() => {
    if (typeof document !== "undefined") {
      document.documentElement.setAttribute("data-market", market);
    }
  }, [market]);

  const value = useMemo<MarketContextValue>(() => {
    const meta = META[market];
    return {
      market,
      marketType: meta.type,
      currency: meta.currency,
      accent: meta.accent,
      flag: meta.flag,
      flagLabel: meta.flagLabel,
      setMarket,
      toggleMarket: () => setMarket((m) => (m === "TASI" ? "US" : "TASI")),
    };
  }, [market]);

  return (
    <MarketContext.Provider value={value}>{children}</MarketContext.Provider>
  );
}

export function useMarket(): MarketContextValue {
  const ctx = useContext(MarketContext);
  if (!ctx) throw new Error("useMarket must be used inside <MarketProvider>");
  return ctx;
}
