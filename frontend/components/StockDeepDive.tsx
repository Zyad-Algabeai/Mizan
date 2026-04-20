"use client";

import { useEffect, useMemo, useState } from "react";
import { Sparkles } from "lucide-react";
import Card from "./ui/Card";
import Button from "./ui/Button";
import CandlestickChart from "./CandlestickChart";
import { api } from "@/lib/api";
import { useMarket } from "@/contexts/MarketContext";
import { ErrorBanner, Skeleton } from "./LoadingState";
import type { SectorEntry, StockHistory } from "@/lib/types";
import { formatNumber, formatPct, formatCompact } from "@/lib/format";

interface Props {
  sectors: SectorEntry[];
}

export default function StockDeepDive({ sectors }: Props) {
  const { market, marketType, currency } = useMarket();

  // Flatten to a single list of selectable stocks.
  const allStocks = useMemo(() => {
    const out: { ticker: string; name: string; sector: string }[] = [];
    for (const sec of sectors) {
      for (const s of sec.stocks) {
        out.push({ ticker: s.ticker, name: s.name, sector: sec.sector });
      }
    }
    return out;
  }, [sectors]);

  const [selected, setSelected] = useState<string>(allStocks[0]?.ticker ?? "");
  const [history, setHistory] = useState<StockHistory | null>(null);
  const [analysis, setAnalysis] = useState<string | null>(null);
  const [loadingHist, setLoadingHist] = useState(false);
  const [loadingAi, setLoadingAi] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Reset selection when market (and therefore sectors) changes.
  useEffect(() => {
    setSelected(allStocks[0]?.ticker ?? "");
    setHistory(null);
    setAnalysis(null);
  }, [market, allStocks]);

  // Auto-fetch history whenever the ticker changes.
  useEffect(() => {
    if (!selected) return;
    let aborted = false;
    setLoadingHist(true);
    setError(null);
    setAnalysis(null);
    api
      .stock(selected, "3mo")
      .then((h) => {
        if (!aborted) setHistory(h);
      })
      .catch((e) => {
        if (!aborted) setError(e?.message ?? "Failed to load history");
      })
      .finally(() => {
        if (!aborted) setLoadingHist(false);
      });
    return () => {
      aborted = true;
    };
  }, [selected]);

  const selectedMeta = allStocks.find((s) => s.ticker === selected);

  async function runAnalysis() {
    if (!selectedMeta) return;
    setLoadingAi(true);
    setError(null);
    try {
      const res = await api.stockAnalysis({
        ticker: selectedMeta.ticker,
        name: selectedMeta.name,
        period: "3mo",
        market_type: marketType,
      });
      setAnalysis(res.text);
    } catch (e: any) {
      setError(e?.message ?? "AI analysis failed");
    } finally {
      setLoadingAi(false);
    }
  }

  return (
    <Card
      title="Stock Deep Dive"
      subtitle="3-month OHLC + Claude analysis"
      chip="Candlestick"
      action={
        <select
          value={selected}
          onChange={(e) => setSelected(e.target.value)}
          className="bg-bg-elev border border-bg-border rounded-xl text-sm px-3 py-2 font-mono tracking-wide focus:outline-none focus:border-[color:var(--accent)]"
          aria-label="Select stock"
        >
          {sectors.map((sec) => (
            <optgroup key={sec.sector} label={sec.sector}>
              {sec.stocks.map((s) => (
                <option key={s.ticker} value={s.ticker}>
                  {s.ticker} · {s.name}
                </option>
              ))}
            </optgroup>
          ))}
        </select>
      }
    >
      {error && <ErrorBanner message={error} />}

      {/* Stats strip */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4">
        <Stat
          label="Last"
          value={history ? `${formatNumber(history.latest, 2)} ${currency}` : "—"}
          loading={loadingHist}
        />
        <Stat
          label="3-mo change"
          value={formatPct(history?.change_pct)}
          tone={
            history?.change_pct === null || history?.change_pct === undefined
              ? "neutral"
              : history.change_pct >= 0
                ? "pos"
                : "neg"
          }
          loading={loadingHist}
        />
        <Stat
          label="3-mo range"
          value={
            history
              ? `${formatNumber(history.low, 2)} – ${formatNumber(history.high, 2)}`
              : "—"
          }
          loading={loadingHist}
        />
        <Stat
          label="Avg volume"
          value={formatCompact(history?.avg_volume)}
          loading={loadingHist}
        />
      </div>

      {loadingHist ? (
        <Skeleton className="h-[360px]" />
      ) : history ? (
        <CandlestickChart series={history.series} />
      ) : null}

      <div className="mt-5 border-t border-bg-border pt-5">
        <div className="flex items-center justify-between mb-3">
          <div>
            <p className="text-[11px] uppercase tracking-[0.2em] font-mono text-fg-muted">
              AI Analysis
            </p>
            <p className="text-sm text-fg mt-1">
              {selectedMeta?.name} ({selectedMeta?.ticker})
            </p>
          </div>
          <Button
            onClick={runAnalysis}
            loading={loadingAi}
            icon={<Sparkles size={14} />}
            size="sm"
            variant="outline"
          >
            Analyze
          </Button>
        </div>
        {analysis ? (
          <p className="text-sm leading-relaxed whitespace-pre-wrap">{analysis}</p>
        ) : (
          <p className="text-xs text-fg-muted">
            Hit <em>Analyze</em> for trend, momentum, and a watch item.
          </p>
        )}
      </div>
    </Card>
  );
}

function Stat({
  label,
  value,
  tone = "neutral",
  loading,
}: {
  label: string;
  value: string;
  tone?: "pos" | "neg" | "neutral";
  loading?: boolean;
}) {
  const toneClass =
    tone === "pos" ? "delta-pos" : tone === "neg" ? "delta-neg" : "text-fg";
  return (
    <div className="bg-bg-elev border border-bg-border rounded-xl p-3">
      <p className="text-[10px] uppercase tracking-[0.2em] font-mono text-fg-muted">
        {label}
      </p>
      {loading ? (
        <Skeleton className="h-5 mt-2 w-20" />
      ) : (
        <p className={`text-base font-semibold tabular-nums mt-1 ${toneClass}`}>
          {value}
        </p>
      )}
    </div>
  );
}
