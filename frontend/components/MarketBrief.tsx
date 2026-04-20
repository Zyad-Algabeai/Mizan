"use client";

import { useState } from "react";
import { Sparkles } from "lucide-react";
import Card from "./ui/Card";
import Button from "./ui/Button";
import { api } from "@/lib/api";
import { useMarket } from "@/contexts/MarketContext";
import { ErrorBanner } from "./LoadingState";

export default function MarketBrief() {
  const { market } = useMarket();
  const [text, setText] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function run() {
    setLoading(true);
    setError(null);
    try {
      const res = await api.marketBrief(market);
      setText(res.text);
    } catch (e: any) {
      setError(e?.message ?? "Failed to generate brief");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card
      title="AI Market Brief"
      chip="Claude"
      subtitle="A concise analyst take, grounded in today's data"
      action={
        <Button onClick={run} loading={loading} icon={<Sparkles size={14} />}>
          {text ? "Regenerate" : "Generate brief"}
        </Button>
      }
    >
      {error && <ErrorBanner message={error} />}
      {!text && !error && !loading && (
        <p className="text-sm text-fg-muted leading-relaxed">
          Hit <em>Generate brief</em> to get a Claude-authored read on the{" "}
          <span className="accent-text font-medium">{market}</span> market — trend,
          framework call-out, and one risk to watch.
        </p>
      )}
      {loading && (
        <div className="space-y-2">
          <div className="h-3 rounded bg-bg-elev animate-pulse w-[95%]" />
          <div className="h-3 rounded bg-bg-elev animate-pulse w-[88%]" />
          <div className="h-3 rounded bg-bg-elev animate-pulse w-[72%]" />
        </div>
      )}
      {text && (
        <article className="prose-mz text-sm text-fg leading-relaxed whitespace-pre-wrap">
          {text}
        </article>
      )}
    </Card>
  );
}
