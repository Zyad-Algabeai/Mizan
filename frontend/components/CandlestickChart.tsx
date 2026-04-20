"use client";

// A lightweight candlestick chart built on top of Recharts' ComposedChart,
// using a <Customized> layer to draw OHLC candles. Keeps the bundle small
// and matches the dark/accent theme perfectly.

import {
  CartesianGrid,
  ComposedChart,
  Customized,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { OHLCPoint } from "@/lib/types";
import { formatNumber, shortDate } from "@/lib/format";

interface Props {
  series: OHLCPoint[];
  height?: number;
}

const UP = "#00D4AA";
const DOWN = "#FF4444";

export default function CandlestickChart({ series, height = 360 }: Props) {
  const data = series
    .filter(
      (p) =>
        p.open !== null && p.high !== null && p.low !== null && p.close !== null,
    )
    .map((p) => ({
      date: p.date,
      open: p.open as number,
      high: p.high as number,
      low: p.low as number,
      close: p.close as number,
    }));

  if (!data.length) {
    return (
      <div
        className="grid place-items-center text-fg-muted text-sm"
        style={{ height }}
      >
        No data
      </div>
    );
  }

  const lows = data.map((d) => d.low);
  const highs = data.map((d) => d.high);
  const yMin = Math.min(...lows);
  const yMax = Math.max(...highs);
  const pad = (yMax - yMin) * 0.08 || 1;

  return (
    <div className="mz-chart-wrap" style={{ width: "100%", height }}>
      <ResponsiveContainer width="100%" height="100%">
        <ComposedChart
          data={data}
          margin={{ top: 8, right: 4, left: -20, bottom: 0 }}
        >
          <CartesianGrid stroke="#1f1f24" vertical={false} />
          <XAxis
            dataKey="date"
            tickLine={false}
            axisLine={false}
            tickFormatter={(v) => shortDate(v)}
            minTickGap={40}
          />
          <YAxis
            domain={[yMin - pad, yMax + pad]}
            tickLine={false}
            axisLine={false}
            tickFormatter={(v) => formatNumber(Number(v), 2)}
            width={70}
          />
          <Tooltip
            cursor={{ stroke: "#3a3a43", strokeOpacity: 0.4, strokeWidth: 1 }}
            contentStyle={{
              background: "#111113",
              border: "1px solid #1f1f24",
              borderRadius: 12,
              fontSize: 12,
              padding: "10px 12px",
            }}
            labelStyle={{ color: "#8a8a94", fontFamily: "monospace" }}
            itemStyle={{ color: "#e7e7ea" }}
            formatter={(value: number, name: string) => [
              formatNumber(value, 2),
              name.toUpperCase(),
            ]}
            labelFormatter={(v) => shortDate(String(v))}
          />
          <Customized component={<Candles />} />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}

/**
 * Custom candle renderer. Recharts passes `xAxisMap`, `yAxisMap`, and the
 * chart's graphical bounds to a <Customized> component. We use those scales
 * to place each candle at the right x-position.
 */
function Candles(props: any) {
  const { xAxisMap, yAxisMap, formattedGraphicalItems } = props;
  if (!xAxisMap || !yAxisMap) return null;

  // Pull the first (and only) axis from the maps.
  const xAxis = (xAxisMap as any)[Object.keys(xAxisMap)[0]];
  const yAxis = (yAxisMap as any)[Object.keys(yAxisMap)[0]];

  // Recharts wraps our data in formattedGraphicalItems when there's a chart
  // series; otherwise we fall back to the axis data.
  const items: any[] =
    (formattedGraphicalItems?.[0]?.props?.data as any[]) ??
    (xAxis?.categoricalDomain?.map((date: string, i: number) => ({
      ...((props.data as any[])?.[i] ?? {}),
      date,
    })) as any[]) ??
    (props.data as any[]) ??
    [];

  // Use axis `scale` function if available; otherwise approximate with width.
  const xScale = xAxis?.scale;
  const yScale = yAxis?.scale;
  if (!xScale || !yScale) return null;

  // Bandwidth: spacing between category ticks.
  const step =
    (xAxis?.width ?? 0) / Math.max(items.length, 1);
  const candleWidth = Math.max(2, Math.min(10, step * 0.6));

  return (
    <g>
      {items.map((d, i) => {
        if (
          d.open === undefined ||
          d.close === undefined ||
          d.high === undefined ||
          d.low === undefined
        ) {
          return null;
        }
        const x =
          typeof xScale === "function"
            ? xScale(d.date) + (xScale.bandwidth?.() ?? 0) / 2
            : (xAxis.x ?? 0) + step * i + step / 2;

        const yHigh = yScale(d.high);
        const yLow = yScale(d.low);
        const yOpen = yScale(d.open);
        const yClose = yScale(d.close);

        const up = d.close >= d.open;
        const color = up ? UP : DOWN;

        const top = Math.min(yOpen, yClose);
        const bodyH = Math.max(1, Math.abs(yClose - yOpen));

        return (
          <g key={i}>
            {/* Wick */}
            <line
              x1={x}
              x2={x}
              y1={yHigh}
              y2={yLow}
              stroke={color}
              strokeWidth={1}
              strokeOpacity={0.85}
            />
            {/* Body */}
            <rect
              x={x - candleWidth / 2}
              y={top}
              width={candleWidth}
              height={bodyH}
              fill={color}
              fillOpacity={up ? 0.9 : 0.95}
              rx={1}
            />
          </g>
        );
      })}
    </g>
  );
}
