"use client";

import type { NewsItem } from "@/lib/types";
import { relTime } from "@/lib/format";
import { ExternalLink } from "lucide-react";
import Card from "./ui/Card";

interface Props {
  items: NewsItem[];
  loading?: boolean;
}

export default function NewsList({ items, loading }: Props) {
  return (
    <Card title="Live News" subtitle="via Yahoo Finance" chip="Market wire">
      {loading && (
        <div className="space-y-3">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="h-14 rounded-xl bg-bg-elev animate-pulse" />
          ))}
        </div>
      )}
      {!loading && !items.length && (
        <p className="text-sm text-fg-muted">No news available right now.</p>
      )}
      <ul className="space-y-2">
        {items.map((n, i) => (
          <li key={i}>
            <a
              href={n.link || "#"}
              target="_blank"
              rel="noreferrer"
              className="group flex items-start justify-between gap-3 p-3 rounded-xl border border-bg-border hover:border-[color:var(--accent)] hover:bg-bg-elev transition-all"
            >
              <div className="min-w-0">
                <p className="text-sm text-fg leading-snug line-clamp-2 group-hover:text-[color:var(--accent)] transition-colors">
                  {n.title}
                </p>
                <div className="mt-1.5 flex items-center gap-3 text-[11px] font-mono uppercase tracking-[0.12em] text-fg-muted">
                  <span>{n.publisher}</span>
                  {n.published && <span>· {relTime(n.published)}</span>}
                  <span className="text-fg-dim">· {n.ticker}</span>
                </div>
              </div>
              <ExternalLink
                size={14}
                className="mt-1 shrink-0 text-fg-dim group-hover:text-[color:var(--accent)] transition-colors"
              />
            </a>
          </li>
        ))}
      </ul>
    </Card>
  );
}
