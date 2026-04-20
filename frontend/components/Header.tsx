"use client";

import MarketToggle from "./MarketToggle";
import { useMarket } from "@/contexts/MarketContext";

export default function Header() {
  const { market } = useMarket();

  return (
    <header className="sticky top-0 z-30 backdrop-blur-md bg-bg/70 border-b border-bg-border">
      <div className="max-w-[1400px] w-full mx-auto px-4 sm:px-6 lg:px-10 py-3.5 flex items-center justify-between gap-3">
        {/* Brand */}
        <div className="flex items-center gap-3 min-w-0">
          <div
            className="w-9 h-9 rounded-xl flex items-center justify-center text-lg font-bold"
            style={{
              background: "var(--accent-soft)",
              color: "var(--accent)",
              border: "1px solid var(--accent-soft)",
            }}
            aria-hidden
          >
            ⚖
          </div>
          <div className="min-w-0">
            <div className="flex items-baseline gap-2">
              <h1 className="text-[15px] sm:text-base font-semibold tracking-tight">
                Mizan
              </h1>
              <span className="ar text-fg-muted text-sm hidden sm:inline">
                ميزان
              </span>
            </div>
            <p className="text-[10px] sm:text-[11px] text-fg-muted font-mono uppercase tracking-[0.18em]">
              {market === "TASI"
                ? "Saudi Market Intelligence"
                : "US Market Intelligence"}
            </p>
          </div>
        </div>

        <MarketToggle />
      </div>
    </header>
  );
}
