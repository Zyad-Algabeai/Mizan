"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { SectorEntry } from "@/lib/types";
import { useMarket } from "@/contexts/MarketContext";
import { formatPct } from "@/lib/format";

interface Props {
  sectors: SectorEntry[];
  height?: number;
}

export default function SectorBar({ sectors, height = 320 }: Props) {
  const { accent } = useMarket();

  const data = sectors.map((s) => ({
    sector: s.sector,
    change: s.avg_change_pct,
  }));

  if (!data.length) {
    return (
      <div className="h-[320px] grid place-items-center text-fg-muted text-sm">
        No sector data
      </div>
    );
  }

  return (
    <div className="mz-chart-wrap" style={{ width: "100%", height }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 4, right: 24, left: 12, bottom: 4 }}
          barSize={18}
        >
          <CartesianGrid stroke="#1f1f24" horizontal={false} />
          <XAxis
            type="number"
            tickLine={false}
            axisLine={false}
            tickFormatter={(v) => `${v}%`}
          />
          <YAxis
            type="category"
            dataKey="sector"
            width={160}
            tickLine={false}
            axisLine={false}
            tick={{ fill: "#e7e7ea", fontSize: 12 }}
          />
          <Tooltip
            cursor={{ fill: "rgba(255,255,255,0.03)" }}
            contentStyle={{
              background: "#111113",
              border: "1px solid #1f1f24",
              borderRadius: 12,
              fontSize: 12,
              padding: "10px 12px",
            }}
            formatter={(value: number) => [formatPct(value), "Avg change"]}
          />
          <Bar dataKey="change" radius={[0, 6, 6, 0]}>
            {data.map((row, i) => (
              <Cell
                key={i}
                fill={row.change >= 0 ? accent : "#FF4444"}
                fillOpacity={0.92}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
