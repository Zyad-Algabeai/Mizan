"use client";

import { useState } from "react";
import { Sparkles } from "lucide-react";
import Card from "./ui/Card";
import Button from "./ui/Button";
import { api } from "@/lib/api";
import { useMarket } from "@/contexts/MarketContext";
import { ErrorBanner } from "./LoadingState";

const SAMPLE = `Aramco beats Q1 earnings estimates on higher oil prices
SABIC announces new petrochemical expansion
Central bank holds benchmark rate steady for third consecutive meeting`;

export default function NewsSentiment() {
  const { marketType } = useMarket();
  const [input, setInput] = useState("");
  const [text, setText] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function run() {
    const headlines = input
      .split("\n")
      .map((s) => s.trim())
      .filter(Boolean);
    if (!headlines.length) {
      setError("Paste at least one headline");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await api.newsSentiment(headlines, marketType);
      setText(res.text);
    } catch (e: any) {
      setError(e?.message ?? "Sentiment analysis failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card
      title="News Sentiment"
      chip="Claude"
      subtitle="Paste headlines, get a sentiment score"
    >
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder={SAMPLE}
        rows={6}
        className="w-full bg-bg-elev border border-bg-border rounded-xl px-3 py-3 text-sm font-mono leading-relaxed placeholder:text-fg-dim focus:outline-none focus:border-[color:var(--accent)] resize-y"
      />
      <div className="mt-3 flex items-center justify-between gap-3 flex-wrap">
        <p className="text-[11px] text-fg-muted font-mono uppercase tracking-[0.14em]">
          One headline per line
        </p>
        <Button
          onClick={run}
          loading={loading}
          icon={<Sparkles size={14} />}
          size="sm"
        >
          Analyze sentiment
        </Button>
      </div>

      {error && <div className="mt-4"><ErrorBanner message={error} /></div>}

      {text && (
        <article className="mt-5 text-sm leading-relaxed whitespace-pre-wrap border-t border-bg-border pt-4">
          {text}
        </article>
      )}
    </Card>
  );
}
