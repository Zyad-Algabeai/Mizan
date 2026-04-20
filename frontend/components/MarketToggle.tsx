"use client";

import clsx from "clsx";
import { useMarket } from "@/contexts/MarketContext";

export default function MarketToggle() {
  const { market, setMarket } = useMarket();

  return (
    <div
      role="tablist"
      aria-label="Market selector"
      className="relative inline-flex items-center p-1 rounded-full bg-bg-elev border border-bg-border text-xs font-mono uppercase tracking-[0.16em]"
    >
      {/* Animated thumb */}
      <span
        aria-hidden
        className={clsx(
          "absolute top-1 bottom-1 w-[calc(50%-4px)] rounded-full transition-all duration-300 ease-out accent-bg-soft accent-glow",
          market === "TASI" ? "left-1" : "left-[calc(50%+3px)]",
        )}
        style={{ borderColor: "var(--accent)" }}
      />

      <button
        role="tab"
        aria-selected={market === "TASI"}
        onClick={() => setMarket("TASI")}
        className={clsx(
          "relative z-10 px-4 sm:px-5 py-1.5 rounded-full transition-colors",
          market === "TASI" ? "accent-text" : "text-fg-muted hover:text-fg",
        )}
      >
        <span aria-hidden className="mr-1.5">🇸🇦</span>
        TASI
      </button>

      <button
        role="tab"
        aria-selected={market === "US"}
        onClick={() => setMarket("US")}
        className={clsx(
          "relative z-10 px-4 sm:px-5 py-1.5 rounded-full transition-colors",
          market === "US" ? "accent-text" : "text-fg-muted hover:text-fg",
        )}
      >
        <span aria-hidden className="mr-1.5">🇺🇸</span>
        US
      </button>
    </div>
  );
}
