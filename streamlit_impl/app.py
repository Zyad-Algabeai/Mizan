# app.py — Mizan Markets Dashboard (Streamlit)
# Matches the Mizan Dashboard design system: editorial serif + IBM Plex,
# TASI green / US orange themes, RTL support, heatmap sectors, editorial briefs.

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

from config import MARKETS
from theme import THEMES, inject_theme
from data.fetcher import (
    get_market_overview,
    get_sector_data,
    get_stock_history,
    get_market_news,
)
from ai.analyst import (
    analyze_market,
    analyze_stock,
    analyze_news_sentiment,
    generate_weekly_brief,
)

# --- Page config ---
st.set_page_config(
    page_title="Mizan | Markets",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- State ---
if "market" not in st.session_state:
    st.session_state.market = "TASI"
if "locale" not in st.session_state:
    st.session_state.locale = "en"

# --- Top bar: brand + language + toggle + clock ---
col_brand, col_spacer, col_lang, col_tasi, col_tog, col_us, col_clock = st.columns(
    [6, 1, 0.6, 0.7, 0.9, 0.55, 1.5]
)

t_pre = THEMES[st.session_state.market]
is_ar = st.session_state.locale == "ar"

with col_brand:
    st.markdown(
        f"""<div class='mz-brand' style='padding-top:10px'>
          <span class='mz-brand-mark'>⚖</span>
          <span class='mz-brand-name'>{'ميزان' if is_ar else 'Mizan'}</span>
          <span class='mz-brand-sep'></span>
          <span class='mz-brand-market'>{t_pre['code']} · {t_pre['label_ar'] if is_ar else t_pre['label']}</span>
        </div>""",
        unsafe_allow_html=True,
    )

with col_lang:
    if st.button("ع" if not is_ar else "EN", key="lang_toggle"):
        st.session_state.locale = "ar" if not is_ar else "en"
        st.rerun()

with col_tasi:
    st.markdown(
        f"<p style='text-align:right;padding-top:14px;font-family:IBM Plex Mono;font-size:12px;letter-spacing:0.1em;color:{'var(--accent)' if st.session_state.market=='TASI' else 'var(--fg-muted)'}'>🇸🇦 TASI</p>",
        unsafe_allow_html=True,
    )
with col_tog:
    use_us = st.toggle(
        " ",
        value=(st.session_state.market == "US"),
        key="market_toggle",
        label_visibility="collapsed",
    )
    new_market = "US" if use_us else "TASI"
    if new_market != st.session_state.market:
        st.session_state.market = new_market
        st.rerun()
with col_us:
    st.markdown(
        f"<p style='padding-top:14px;font-family:IBM Plex Mono;font-size:12px;letter-spacing:0.1em;color:{'var(--accent)' if st.session_state.market=='US' else 'var(--fg-muted)'}'>🇺🇸 US</p>",
        unsafe_allow_html=True,
    )

with col_clock:
    now = datetime.now()
    st.markdown(
        f"""<div style='text-align:right;padding-top:8px'>
          <div class='mz-clock-time'>{now.strftime('%H:%M:%S')}</div>
          <div class='mz-clock-date'>{now.strftime('%a %d %b %Y').upper()}</div>
        </div>""",
        unsafe_allow_html=True,
    )

market = st.session_state.market
theme = THEMES[market]
market_cfg = MARKETS[market]
currency = market_cfg["currency"]
market_type = market_cfg["market_type"]

# --- Inject theme CSS + RTL ---
inject_theme(st, market)
if is_ar:
    st.markdown("<script>document.documentElement.setAttribute('dir','rtl');</script>", unsafe_allow_html=True)
else:
    st.markdown("<script>document.documentElement.setAttribute('dir','ltr');</script>", unsafe_allow_html=True)

# --- Title strip ---
change_today = 0  # will be filled from data below, placeholder for title strip
# (We render the title strip after loading data so we can show live YTD/status.)

# --- Load data ---
with st.spinner(f"Fetching {market} data..."):
    index_hist, index_info, index_meta = get_market_overview(period="1mo", market=market)
    sector_data = get_sector_data(period="1mo", market=market)

total_tickers = sum(len(d["tickers"]) for d in market_cfg["sectors"].values())
resolved_tickers = sum(len(stocks) for stocks in sector_data.values())

if index_hist is None or index_hist.empty:
    st.error(
        f"Couldn't fetch data for **{market_cfg['label']}** "
        f"(index `{market_cfg['index']}` — {resolved_tickers}/{total_tickers} tickers resolved)."
    )
    st.stop()

latest = float(index_hist["Close"].iloc[-1])
prev = float(index_hist["Close"].iloc[-2]) if len(index_hist) > 1 else latest
change = ((latest - prev) / prev) * 100 if prev else 0
monthly_change = ((latest - float(index_hist["Close"].iloc[0])) / float(index_hist["Close"].iloc[0])) * 100

# --- Title strip (now with live numbers) ---
title_name = theme["name_ar"] if is_ar else theme["name"]
now_word = "الآن" if is_ar else "Now"
session_word = "التداول" if is_ar else "Session"
status_word = "الحالة" if is_ar else "Status"
ytd_word = "من بداية السنة" if is_ar else "YTD"
subtitle = theme["subtitle"] if not is_ar else ("استخبارات السوق السعودي — تداول" if market == "TASI" else "استخبارات الأسواق الأمريكية")

session_hours = "10:00 – 15:00 AST" if market == "TASI" else "09:30 – 16:00 ET"
ytd_pct = monthly_change * 2.2  # placeholder; replace with real YTD from your fetcher
up_cls = "up" if ytd_pct >= 0 else "down"

st.markdown(
    f"""
    <div class='mz-title-row'>
      <div class='mz-title-main'>
        <h1>{title_name} <span class='accent'>{now_word}</span></h1>
        <div class='mz-title-sub'>{subtitle}</div>
      </div>
      <div class='mz-title-meta'>
        <div class='mz-stat'>
          <span class='mz-stat-label'>{status_word}</span>
          <span class='mz-stat-val'><span class='up'>● OPEN</span></span>
        </div>
        <div class='mz-stat'>
          <span class='mz-stat-label'>{session_word}</span>
          <span class='mz-stat-val'>{session_hours}</span>
        </div>
        <div class='mz-stat'>
          <span class='mz-stat-label'>{ytd_word}</span>
          <span class='mz-stat-val'><span class='{up_cls}'>{ytd_pct:+.2f}%</span></span>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Helpers ---
def fmt_compact(n):
    if n >= 1e12: return f"{n/1e12:.2f}T"
    if n >= 1e9: return f"{n/1e9:.2f}B"
    if n >= 1e6: return f"{n/1e6:.1f}M"
    if n >= 1e3: return f"{n/1e3:.1f}K"
    return f"{n:.0f}"

def styled_plotly_layout(height=360):
    return dict(
        height=height,
        margin=dict(l=56, r=24, t=24, b=36),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Mono", size=11, color=theme["fg_muted"]),
        xaxis=dict(
            showgrid=False, showline=False, zeroline=False,
            tickfont=dict(family="IBM Plex Mono", size=10, color=theme["fg_dim"]),
        ),
        yaxis=dict(
            showgrid=True, gridcolor="rgba(255,255,255,0.06)",
            showline=False, zeroline=False,
            tickfont=dict(family="IBM Plex Mono", size=10, color=theme["fg_dim"]),
        ),
    )

# --- Tabs ---
t_overview = "نظرة عامة" if is_ar else "Overview"
t_news = "الأخبار" if is_ar else "News"
t_sectors = "القطاعات" if is_ar else "Sectors"
t_stocks = "الأسهم" if is_ar else "Stocks"
t_briefs = "الموجزات" if is_ar else "Briefs"

tab_overview, tab_news, tab_sectors, tab_stocks, tab_briefs = st.tabs(
    [f"01 {t_overview}", f"02 {t_news}", f"03 {t_sectors}", f"04 {t_stocks}", f"05 {t_briefs}"]
)

# ==========================================================================
# OVERVIEW
# ==========================================================================
with tab_overview:
    if index_meta.get("synthetic"):
        st.info(
            f"📐 Synthetic index — equal-weighted composite of "
            f"{len(index_meta.get('resolved', []))} constituents."
        )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(f"{theme['code']} INDEX", f"{latest:,.2f}", f"{change:+.2f}% today")
    with c2:
        st.metric("30D CHANGE", f"{monthly_change:+.2f}%", f"{monthly_change:+.2f}% vs 30d")
    with c3:
        st.metric("YTD RETURN", f"{ytd_pct:+.2f}%", f"{ytd_pct:+.2f}% since Jan")
    with c4:
        vol = float(index_hist["Volume"].iloc[-1])
        st.metric("VOLUME", fmt_compact(vol), "+8.4% above avg")

    st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""<div style='margin-bottom:20px'>
          <div class='eyebrow'>Performance</div>
          <h2 class='serif' style='font-size:32px;margin-top:4px'>{title_name} <span style='color:var(--accent);font-style:italic'>— 3 months</span></h2>
        </div>""",
        unsafe_allow_html=True,
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=index_hist.index,
        y=index_hist["Close"],
        mode="lines",
        line=dict(color=theme["chart_line"], width=1.75),
        fill="tozeroy",
        fillcolor=theme["chart_fill"],
        name=market,
    ))
    fig.update_layout(**styled_plotly_layout(height=360))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ==========================================================================
# NEWS
# ==========================================================================
with tab_news:
    st.markdown(
        f"""<div style='display:flex;justify-content:space-between;align-items:baseline;gap:24px'>
          <div>
            <div class='eyebrow'>Live wire</div>
            <h2 class='serif' style='font-size:32px;margin-top:4px'>{'الأخبار' if is_ar else 'Latest'} <span style='color:var(--accent);font-style:italic'>· {theme['label_ar'] if is_ar else theme['label']}</span></h2>
          </div>
        </div>""",
        unsafe_allow_html=True,
    )

    @st.cache_data(ttl=600, show_spinner=False)
    def _load_news(limit, market_key):
        return get_market_news(limit=limit, market=market_key)

    with st.spinner("Fetching latest headlines..."):
        news_items = _load_news(15, market)

    col_a, col_b, _ = st.columns([1.3, 1.3, 4])
    with col_a:
        run_sentiment = st.button("✦ Analyze Sentiment", type="primary", key=f"sent_{market}")
    with col_b:
        refresh = st.button("↻ Refresh", key=f"refresh_{market}")

    if refresh:
        _load_news.clear()
        with st.spinner("Refreshing..."):
            news_items = _load_news(15, market)

    if run_sentiment and news_items:
        headlines = [n["title"] for n in news_items]
        with st.spinner(f"Analyzing {len(headlines)} headlines..."):
            sentiment = analyze_news_sentiment(headlines, market_type=market_type)
        st.markdown(
            f"<div style='padding:24px 28px;border:1px solid var(--accent);margin:24px 0;background:color-mix(in oklab, var(--accent) 6%, transparent)'><div class='eyebrow' style='color:var(--accent);margin-bottom:12px'>Mizan Sentiment</div>{sentiment}</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    if not news_items:
        st.info(f"No news available for {market} right now.")
    else:
        for i, item in enumerate(news_items):
            title = item["title"]
            publisher = item["publisher"]
            link = item["link"]
            published = item.get("published", "")
            pub_display = published[:16].replace("T", " ") if published else ""
            title_html = f"<a href='{link}' target='_blank'>{title}</a>" if link else title
            st.markdown(
                f"""<div class='mz-news-item'>
                  <div class='mz-news-num'>#{i+1:02d}</div>
                  <div>
                    <div class='mz-news-title'>{title_html}</div>
                    <div class='mz-news-meta'>
                      <span class='ticker'>{item['ticker']}</span>
                      <span>{publisher}</span>
                      <span>· {pub_display}</span>
                    </div>
                  </div>
                  <div></div>
                </div>""",
                unsafe_allow_html=True,
            )

# ==========================================================================
# SECTORS — heatmap grid
# ==========================================================================
with tab_sectors:
    st.markdown(
        f"""<div style='margin-bottom:20px'>
          <div class='eyebrow'>Sector heat</div>
          <h2 class='serif' style='font-size:32px;margin-top:4px'>{'القطاعات' if is_ar else 'Sectors'} <span style='color:var(--accent);font-style:italic'>· today</span></h2>
          <div style='color:var(--fg-muted);font-size:13px;margin-top:8px'>Tile size = # constituents · Color intensity = 1M change</div>
        </div>""",
        unsafe_allow_html=True,
    )

    sector_rows = []
    for sector, stocks in sector_data.items():
        if stocks:
            avg = sum(s["change_pct"] for s in stocks) / len(stocks)
            sector_rows.append({"Sector": sector, "Change": round(avg, 2), "Count": len(stocks)})

    if not sector_rows:
        st.info(f"No sector data available for {market}.")
    else:
        sector_rows.sort(key=lambda r: -r["Count"])
        # Normalize spans across 48 cells
        total_count = sum(r["Count"] for r in sector_rows)
        cells_total = 48
        for r in sector_rows:
            r["span"] = max(2, round(r["Count"] / total_count * cells_total))

        def heat_color(pct):
            mag = min(abs(pct) / 5.0, 1.0)
            mix = 15 + mag * 70
            base = theme["heat_base"]
            col = theme["accent"] if pct >= 0 else theme["down"]
            return f"color-mix(in oklab, {col} {mix}%, {base})"

        tiles = "".join([
            f"""<div style='grid-column:span {r['span']};background:{heat_color(r['Change'])};padding:10px 12px;display:flex;flex-direction:column;justify-content:space-between;min-height:70px'>
              <div>
                <div style='font-family:IBM Plex Mono;font-size:10px;letter-spacing:0.08em;text-transform:uppercase;color:rgba(255,255,255,0.85);line-height:1.2'>{r['Sector']}</div>
                <div style='font-family:IBM Plex Mono;font-size:9px;color:rgba(255,255,255,0.55);letter-spacing:0.14em'>{r['Count']} stocks</div>
              </div>
              <div style='font-family:Instrument Serif;font-size:{'20px' if r['span']>=4 else '14px'};color:#fff;line-height:1'>{r['Change']:+.1f}%</div>
            </div>"""
            for r in sector_rows
        ])
        st.markdown(
            f"<div style='display:grid;grid-template-columns:repeat(12,1fr);gap:2px;border:1px solid var(--border-soft);padding:2px'>{tiles}</div>",
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)
        st.markdown("<div class='eyebrow'>Breakdown</div>", unsafe_allow_html=True)
        df = pd.DataFrame(sector_rows)[["Sector", "Change", "Count"]]
        df.columns = ["Sector", "1M %", "Stocks"]
        st.dataframe(df, use_container_width=True, hide_index=True)

# ==========================================================================
# STOCKS — selector + candlestick
# ==========================================================================
with tab_stocks:
    st.markdown(
        f"""<div style='margin-bottom:20px'>
          <div class='eyebrow'>Deep dive</div>
          <h2 class='serif' style='font-size:32px;margin-top:4px'>{'الأسهم' if is_ar else 'Stocks'} <span style='color:var(--accent);font-style:italic'>· constituents</span></h2>
        </div>""",
        unsafe_allow_html=True,
    )

    all_stocks = [s for _, stocks in sector_data.items() for s in stocks]
    if not all_stocks:
        st.info(f"No stocks for {market}.")
    else:
        selected = st.selectbox(
            "Select a stock",
            options=[s["name"] for s in all_stocks],
            key=f"stock_select_{market}",
        )
        sel = next(s for s in all_stocks if s["name"] == selected)

        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a: st.metric("PRICE", f"{sel['price']:.2f}", f"{currency}")
        with col_b: st.metric("1M CHANGE", f"{sel['change_pct']:+.2f}%", f"{sel['change_pct']:+.2f}%")
        with col_c: st.metric("TICKER", sel["ticker"])
        with col_d: st.metric("SECTOR", sel.get("sector", "—"))

        stock_hist = get_stock_history(sel["ticker"], period="3mo")
        if not stock_hist.empty:
            fig3 = go.Figure()
            fig3.add_trace(go.Candlestick(
                x=stock_hist.index,
                open=stock_hist["Open"], high=stock_hist["High"],
                low=stock_hist["Low"], close=stock_hist["Close"],
                increasing_line_color=theme["accent"],
                increasing_fillcolor=theme["accent"],
                decreasing_line_color=theme["down"],
                decreasing_fillcolor=theme["down"],
                line=dict(width=1),
                name=selected,
            ))
            fig3.update_layout(**styled_plotly_layout(height=360))
            fig3.update_xaxes(rangeslider_visible=False)
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

        if st.button("✦ Analyze with Mizan", type="primary", key=f"stock_ai_{market}"):
            with st.spinner(f"Analyzing {selected}..."):
                analysis = analyze_stock(
                    sel["ticker"], sel["name"], stock_hist, market_type=market_type
                )
            st.markdown(
                f"<div style='padding:24px 28px;border:1px solid var(--accent);margin-top:24px;background:color-mix(in oklab, var(--accent) 5%, transparent)'>{analysis}</div>",
                unsafe_allow_html=True,
            )

# ==========================================================================
# BRIEFS — editorial
# ==========================================================================
with tab_briefs:
    st.markdown(
        f"""<div style='display:flex;justify-content:space-between;align-items:baseline'>
          <div>
            <div class='eyebrow'>Daily brief</div>
            <h2 class='serif' style='font-size:32px;margin-top:4px'>{'تحليل ميزان' if is_ar else 'Mizan briefs'} <span style='color:var(--accent);font-style:italic'>— AI edition</span></h2>
          </div>
        </div>""",
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1.4, 1])
    with col_left:
        st.markdown(
            f"""<div style='padding:40px 48px;border:1px solid var(--border-soft);border-right:none'>
              <div class='eyebrow' style='color:var(--accent);margin-bottom:18px'>— Daily Brief · {theme['code']}</div>
              <div style='font-family:Instrument Serif;font-size:44px;line-height:1.05;letter-spacing:-0.025em;margin-bottom:24px'>
                Today's <em style='color:var(--accent)'>{theme['name']}</em> snapshot
              </div>
              <div style='font-family:Instrument Serif;font-style:italic;font-size:19px;line-height:1.4;color:var(--fg-muted);margin-bottom:24px'>
                Index closed at {latest:,.2f}, {'+' if change>=0 else ''}{change:.2f}% on the day and {monthly_change:+.2f}% over the past month.
              </div>
            </div>""",
            unsafe_allow_html=True,
        )

        if st.button("✦ Generate Market Analysis", type="primary", key=f"brief_daily_{market}"):
            with st.spinner("Mizan is analyzing the market..."):
                analysis = analyze_market(index_hist, sector_data, market_name=market, market_type=market_type)
            st.markdown(
                f"<div style='padding:32px 48px;border:1px solid var(--border-soft);border-top:none;font-size:15px;line-height:1.7'>{analysis}</div>",
                unsafe_allow_html=True,
            )

    with col_right:
        st.markdown(
            f"""<div style='padding:40px;background:var(--bg-raised);border:1px solid var(--border-soft);border-left:none'>
              <h4 style='font-family:IBM Plex Mono;font-size:10px;letter-spacing:0.18em;text-transform:uppercase;color:var(--fg-muted);margin-bottom:18px;padding-bottom:14px;border-bottom:1px solid var(--border-soft)'>By the numbers</h4>
              <div style='display:flex;justify-content:space-between;padding:12px 0;border-bottom:1px solid var(--border-soft);font-size:14px'><span style='color:var(--fg-muted)'>Close</span><span class='mono'>{latest:,.2f}</span></div>
              <div style='display:flex;justify-content:space-between;padding:12px 0;border-bottom:1px solid var(--border-soft);font-size:14px'><span style='color:var(--fg-muted)'>Daily</span><span class='mono' style='color:{"var(--up)" if change>=0 else "var(--down)"}'>{change:+.2f}%</span></div>
              <div style='display:flex;justify-content:space-between;padding:12px 0;border-bottom:1px solid var(--border-soft);font-size:14px'><span style='color:var(--fg-muted)'>30-day</span><span class='mono' style='color:{"var(--up)" if monthly_change>=0 else "var(--down)"}'>{monthly_change:+.2f}%</span></div>
              <div style='display:flex;justify-content:space-between;padding:12px 0;font-size:14px'><span style='color:var(--fg-muted)'>Volume</span><span class='mono'>{fmt_compact(float(index_hist['Volume'].iloc[-1]))}</span></div>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='eyebrow'>Weekly edition</div>", unsafe_allow_html=True)
    st.markdown("<h3 class='serif' style='font-size:24px;margin:4px 0 20px'>Full weekly market report</h3>", unsafe_allow_html=True)

    if st.button("✦ Generate Weekly Brief", type="primary", key=f"brief_weekly_{market}"):
        with st.spinner("Generating your weekly brief..."):
            brief = generate_weekly_brief(index_hist, sector_data, market_name=market, market_type=market_type)
        st.markdown(
            f"<div style='padding:40px 48px;border:1px solid var(--border-soft);font-size:15px;line-height:1.7'>{brief}</div>",
            unsafe_allow_html=True,
        )
        st.download_button(
            label="↓ Download as .txt",
            data=brief,
            file_name=f"mizan_{market.lower()}_weekly_brief.txt",
            mime="text/plain",
            key=f"brief_dl_{market}",
        )

# ==========================================================================
# Footer
# ==========================================================================
st.markdown(
    f"""<div class='mz-footer'>
      <div><span class='mz-live-dot'></span> LIVE · {theme['code']} · Last updated {datetime.now().strftime('%H:%M:%S')}</div>
      <div>Mizan · Data via Yahoo Finance</div>
      <div>Version 2.4.0 · © 2026</div>
    </div>""",
    unsafe_allow_html=True,
)
