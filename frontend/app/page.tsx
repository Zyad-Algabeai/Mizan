"use client";

import { useEffect, useState } from "react";
import { useMarket } from "@/contexts/MarketContext";
import { api } from "@/lib/api";
import type {
  MarketOverview,
  SectorsResponse,
  NewsResponse,
} from "@/lib/types";
import MetricCard from "@/components/MetricCard";
import IndexChart from "@/components/IndexChart";
import SectorBar from "@/components/SectorBar";
import Card from "@/components/ui/Card";
import MarketBrief from "@/components/MarketBrief";
import StockDeepDive from "@/components/StockDeepDive";
import NewsSentiment from "@/components/NewsSentiment";
import WeeklyBrief from "@/components/WeeklyBrief";
import NewsList from "@/components/NewsList";
import { Skeleton, ErrorBanner } from "@/components/LoadingState";
import { formatNumber, formatPct } from "@/lib/format";

export default function HomePage() {
  const { market, currency, flag, flagLabel } = useMarket();

  const [overview, setOverview] = useState<MarketOverview | null>(null);
  const [sectorsData, setSectorsData] = useState<SectorsResponse | null>(null);
  const [news, setNews] = useState<NewsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [newsLoading, setNewsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let aborted = false;
    setLoading(true);
    setError(null);

    Promise.all([
      api.overview(market, "1mo"),
      api.sectors(market, "1mo"),
    ])
      .then(([ov, sec]) => {
        if (aborted) return;
        setOverview(ov);
        setSectorsData(sec);
      })
      .catch((e) => {
        if (aborted) return;
        setError(e?.message ?? "Failed to load market data");
      })
      .finally(() => {
        if (!aborted) setLoading(false);
      });

    return () => {
      aborted = true;
    };
  }, [market]);

  // News loads independently — slower and less critical.
  useEffect(() => {
    let aborted = false;
    setNewsLoading(true);
    api
      .news(market, 10)
      .then((res) => {
        if (!aborted) setNews(res);
      })
      .catch(() => {
        // Non-fatal: just show empty state.
        if (!aborted) setNews({ market, items: [] });
      })
      .finally(() => {
        if (!aborted) setNewsLoading(false);
      });
    return () => {
      aborted = true;
    };
  }, [market]);

  const sectors = sectorsData?.sectors ?? [];

  const topSector = sectors[0];
  const bottomSector = sectors[sectors.length - 1];

  return (
    <div className="py-6 sm:py-10 space-y-6 sm:space-y-8">
      {/* ---------- Hero metrics ---------- */}
      <section>
        <div className="mb-4 flex items-end justify-between gap-4">
          <div>
            <p className="text-[11px] font-mono uppercase tracking-[0.22em] text-fg-muted">
              {flag} {market === "TASI" ? "Tadawul All-Share Index" : "S&P 500"}
              <span className="mx-2 text-fg-dim">·</span>
              {overview?.index_symbol ?? "—"}
              {overview?.synthetic && (
                <span className="ml-2 text-warn">· Synthetic</span>
              )}
            </p>
            <h2 className="text-2xl sm:text-3xl font-semibold tracking-tight mt-1">
              Market Overview
            </h2>
          </div>
          <span className="mz-chip">{flagLabel}</span>
        </div>

        {error && <ErrorBanner message={error} />}

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
          <MetricCard
            label={`Level (${currency})`}
            value={
              loading
                ? "—"
                : formatNumber(overview?.latest ?? null, 2)
            }
            delta={overview?.daily_change_pct ?? null}
            hint="vs. previous close"
            accent
          />
          <MetricCard
            label="1-month"
            value={formatPct(overview?.monthly_change_pct ?? null)}
            delta={overview?.monthly_change_pct ?? null}
            hint="period return"
          />
          <MetricCard
            label="Top sector"
            value={
              topSector
                ? `${topSector.sector}`
                : "—"
            }
            delta={topSector?.avg_change_pct ?? null}
            hint="avg change · 1mo"
          />
          <MetricCard
            label="Weakest sector"
            value={bottomSector ? `${bottomSector.sector}` : "—"}
            delta={bottomSector?.avg_change_pct ?? null}
            hint="avg change · 1mo"
          />
        </div>
      </section>

      {/* ---------- Index chart + AI brief side-by-side on desktop ---------- */}
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
        <div className="lg:col-span-2">
          <Card
            title="Index Performance"
            subtitle="1-month close · daily"
            chip={overview?.index_symbol ?? ""}
          >
            {loading ? (
              <Skeleton className="h-[320px]" />
            ) : (
              <IndexChart series={overview?.series ?? []} />
            )}
          </Card>
        </div>
        <div>
          <MarketBrief />
        </div>
      </section>

      {/* ---------- Sector bar + News ---------- */}
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
        <div className="lg:col-span-2">
          <Card
            title="Sector Performance"
            subtitle="Average 1-month change per sector"
            chip="Heatmap"
          >
            {loading ? (
              <Skeleton className="h-[320px]" />
            ) : (
              <SectorBar sectors={sectors} />
            )}
          </Card>
        </div>
        <div>
          <NewsList items={news?.items ?? []} loading={newsLoading} />
        </div>
      </section>

      {/* ---------- Stock Deep Dive ---------- */}
      <section>
        {loading ? (
          <Card title="Stock Deep Dive">
            <Skeleton className="h-[420px]" />
          </Card>
        ) : (
          <StockDeepDive sectors={sectors} />
        )}
      </section>

      {/* ---------- Sentiment + Weekly brief ---------- */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        <NewsSentiment />
        <WeeklyBrief />
      </section>
    </div>
  );
}
