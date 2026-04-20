import type { Metadata, Viewport } from "next";
import "./globals.css";
import { MarketProvider } from "@/contexts/MarketContext";
import Header from "@/components/Header";

export const metadata: Metadata = {
  title: "Mizan | Market Intelligence",
  description:
    "Live TASI & US market intelligence with Claude-powered briefs, sector heatmaps, and sentiment analysis.",
  icons: { icon: "/favicon.ico" },
};

export const viewport: Viewport = {
  themeColor: "#0a0a0b",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" data-market="TASI" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Naskh+Arabic:wght@400;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>
        <MarketProvider>
          <div className="min-h-[100dvh] flex flex-col">
            <Header />
            <main className="flex-1 px-4 sm:px-6 lg:px-10 max-w-[1400px] w-full mx-auto pb-16">
              {children}
            </main>
            <footer className="px-4 sm:px-6 lg:px-10 max-w-[1400px] w-full mx-auto py-8 text-fg-dim text-xs font-mono uppercase tracking-[0.16em] flex items-center justify-between border-t border-bg-border">
              <span>Mizan · ⚖ Market Intelligence</span>
              <span>Built with Next.js · FastAPI · Claude</span>
            </footer>
          </div>
        </MarketProvider>
      </body>
    </html>
  );
}
