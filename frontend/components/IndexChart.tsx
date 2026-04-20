"use client";

import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useMarket } from "@/contexts/MarketContext";
import { formatNumber, shortDate } from "@/lib/format";
import type { OHLCPoint } from "@/lib/types";

interface Props {
  series: OHLCPoint[];
  height?: number;
}

export default function IndexChart({ series, height = 320 }: Props) {
  const { accent } = useMarket();
  const data = series.filter((p) => p.close !== null);

  if (!data.length) {
    return (
      <div className="h-[320px] grid place-items-center text-fg-muted text-sm">
        No data available
      </div>
    );
  }

  const closes = data.map((d) => d.close as number);
  const min = Math.min(...closes);
  const max = Math.max(...closes);
  const pad = (max - min) * 0.08 || 1;

  return (
    <div className="mz-chart-wrap" style={{ width: "100%", height }}>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 8, right: 4, left: -20, bottom: 0 }}>
          <defs>
            <linearGradient id="mz-index-grad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={accent} stopOpacity={0.35} />
              <stop offset="100%" stopColor={accent} stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid
            stroke="#1f1f24"
            strokeDasharray="0"
            vertical={false}
          />
          <XAxis
            dataKey="date"
            tickLine={false}
            axisLine={false}
            tickFormatter={(v) => shortDate(v)}
            minTickGap={40}
          />
          <YAxis
            domain={[min - pad, max + pad]}
            tickLine={false}
            axisLine={false}
            tickFormatter={(v) => formatNumber(Number(v), 0)}
            width={60}
          />
          <Tooltip
            cursor={{ stroke: accent, strokeOpacity: 0.3, strokeWidth: 1 }}
            contentStyle={{
              background: "#111113",
              border: "1px solid #1f1f24",
              borderRadius: 12,
              fontSize: 12,
              padding: "10px 12px",
            }}
            labelStyle={{ color: "#8a8a94", fontFamily: "monospace" }}
            itemStyle={{ color: "#e7e7ea" }}
            formatter={(value: number) => [formatNumber(value, 2), "Close"]}
            labelFormatter={(v) => shortDate(String(v))}
          />
          <Area
            type="monotone"
            dataKey="close"
            stroke={accent}
            strokeWidth={2}
            fill="url(#mz-index-grad)"
            activeDot={{ r: 4, fill: accent, stroke: "#0a0a0b", strokeWidth: 2 }}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
