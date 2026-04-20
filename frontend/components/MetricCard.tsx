import clsx from "clsx";
import { ReactNode } from "react";

interface Props {
  label: string;
  value: string;
  delta?: number | null;
  hint?: ReactNode;
  accent?: boolean;
  className?: string;
}

export default function MetricCard({
  label,
  value,
  delta,
  hint,
  accent,
  className,
}: Props) {
  const deltaClass =
    delta === null || delta === undefined
      ? "text-fg-muted"
      : delta >= 0
        ? "delta-pos"
        : "delta-neg";

  return (
    <div
      className={clsx(
        "mz-card p-5 sm:p-6 mz-fade",
        accent && "border-[color:var(--accent)]/30",
        className,
      )}
      style={accent ? { boxShadow: "0 0 0 1px var(--accent-soft) inset, 0 8px 32px var(--accent-glow)" } : undefined}
    >
      <p className="text-[10px] sm:text-[11px] uppercase tracking-[0.22em] font-mono text-fg-muted">
        {label}
      </p>
      <p className="mt-2 text-3xl sm:text-4xl font-semibold tracking-tight tabular-nums">
        {value}
      </p>
      {(delta !== undefined && delta !== null) && (
        <p className={clsx("mt-2 text-sm font-mono tabular-nums", deltaClass)}>
          {delta > 0 ? "▲" : delta < 0 ? "▼" : "•"}{" "}
          {delta > 0 ? "+" : ""}
          {delta.toFixed(2)}%
        </p>
      )}
      {hint && (
        <p className="mt-1 text-xs text-fg-muted font-mono tracking-[0.08em]">
          {hint}
        </p>
      )}
    </div>
  );
}
