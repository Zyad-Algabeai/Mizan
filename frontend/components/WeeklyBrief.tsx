"use client";

import { useState } from "react";
import { Download, FileText, Sparkles } from "lucide-react";
import Card from "./ui/Card";
import Button from "./ui/Button";
import { api } from "@/lib/api";
import { useMarket } from "@/contexts/MarketContext";
import { ErrorBanner } from "./LoadingState";

export default function WeeklyBrief() {
  const { market } = useMarket();
  const [text, setText] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function run() {
    setLoading(true);
    setError(null);
    try {
      const res = await api.weeklyBrief(market);
      setText(res.text);
    } catch (e: any) {
      setError(e?.message ?? "Weekly brief failed");
    } finally {
      setLoading(false);
    }
  }

  function download() {
    if (!text) return;
    const filename = `mizan-${market.toLowerCase()}-weekly-brief-${new Date()
      .toISOString()
      .slice(0, 10)}.md`;
    const header = `# Mizan Weekly Brief — ${market}\n_Generated ${new Date().toLocaleString()}_\n\n---\n\n`;
    const blob = new Blob([header + text], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  return (
    <Card
      title="Weekly Market Brief"
      chip="Claude"
      subtitle="Full editorial brief with sector breakdown"
      action={
        <div className="flex items-center gap-2">
          {text && (
            <Button
              onClick={download}
              variant="outline"
              size="sm"
              icon={<Download size={14} />}
            >
              Download .md
            </Button>
          )}
          <Button
            onClick={run}
            loading={loading}
            icon={<Sparkles size={14} />}
            size="sm"
          >
            {text ? "Regenerate" : "Generate"}
          </Button>
        </div>
      }
    >
      {error && <ErrorBanner message={error} />}
      {!text && !loading && !error && (
        <div className="flex items-start gap-3 p-4 bg-bg-elev border border-bg-border rounded-xl">
          <FileText size={18} className="mt-0.5 accent-text shrink-0" />
          <p className="text-sm text-fg-muted leading-relaxed">
            Generate a full weekly brief: exec summary, performance analysis,
            top/bottom sectors, {market === "TASI" ? "Vision 2030 pulse" : "Fed & macro pulse"},
            the week ahead, and a bottom-line takeaway.
          </p>
        </div>
      )}
      {loading && (
        <div className="space-y-2">
          {Array.from({ length: 6 }).map((_, i) => (
            <div
              key={i}
              className="h-3 rounded bg-bg-elev animate-pulse"
              style={{ width: `${75 + Math.random() * 20}%` }}
            />
          ))}
        </div>
      )}
      {text && (
        <article className="text-sm leading-relaxed whitespace-pre-wrap">
          {text}
        </article>
      )}
    </Card>
  );
}
