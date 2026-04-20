# theme.py — Mizan design tokens & CSS injection for Streamlit
# Drop this next to app.py and import `inject_theme`.

THEMES = {
    "TASI": {
        "name": "Tadawul",
        "name_ar": "تداول",
        "code": "TASI",
        "flag": "🇸🇦",
        "label": "Saudi Market",
        "label_ar": "السوق السعودي",
        "subtitle": "Saudi Stock Exchange Intelligence · التحليل الذكي",
        "emoji": "⚖️",
        "primary": "#00D4AA",
        "accent": "#00D4AA",
        "up": "#00D4AA",
        "down": "#FF5C7A",
        "bg": "oklch(0.12 0.015 165)",
        "bg_raised": "oklch(0.15 0.018 165)",
        "bg_card": "oklch(0.17 0.02 165)",
        "border": "oklch(0.24 0.02 165)",
        "border_soft": "oklch(0.20 0.015 165)",
        "fg": "oklch(0.98 0.005 165)",
        "fg_muted": "oklch(0.68 0.01 165)",
        "fg_dim": "oklch(0.48 0.015 165)",
        "heat_base": "oklch(0.20 0.02 165)",
        "header_tint": "linear-gradient(180deg, oklch(0.20 0.06 165 / 0.6), oklch(0.12 0.015 165 / 0))",
        "chart_line": "#00D4AA",
        "chart_fill": "rgba(0,212,170,0.18)",
        "btn_fg": "#07110e",
    },
    "US": {
        "name": "Wall Street",
        "name_ar": "وول ستريت",
        "code": "SPX",
        "flag": "🇺🇸",
        "label": "US Markets",
        "label_ar": "الأسواق الأمريكية",
        "subtitle": "S&P 500 · Nasdaq · Dow Jones — Live Intelligence",
        "emoji": "⚖️",
        "primary": "#FF6B35",
        "accent": "#FF6B35",
        "up": "#4ADE80",
        "down": "#FF5C7A",
        "bg": "oklch(0.13 0.02 255)",
        "bg_raised": "oklch(0.16 0.025 255)",
        "bg_card": "oklch(0.18 0.028 255)",
        "border": "oklch(0.26 0.03 255)",
        "border_soft": "oklch(0.22 0.025 255)",
        "fg": "oklch(0.98 0.005 255)",
        "fg_muted": "oklch(0.68 0.02 255)",
        "fg_dim": "oklch(0.48 0.02 255)",
        "heat_base": "oklch(0.20 0.025 255)",
        "header_tint": "linear-gradient(180deg, oklch(0.22 0.08 255 / 0.7), oklch(0.13 0.02 255 / 0))",
        "chart_line": "#FF6B35",
        "chart_fill": "rgba(255,107,53,0.18)",
        "btn_fg": "#1a0a04",
    },
}


def inject_theme(st, market: str):
    """Inject the full Mizan design system CSS for the given market."""
    t = THEMES[market]
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&display=swap');

    :root {{
      --bg: {t['bg']};
      --bg-raised: {t['bg_raised']};
      --bg-card: {t['bg_card']};
      --border: {t['border']};
      --border-soft: {t['border_soft']};
      --fg: {t['fg']};
      --fg-muted: {t['fg_muted']};
      --fg-dim: {t['fg_dim']};
      --accent: {t['accent']};
      --up: {t['up']};
      --down: {t['down']};
      --heat-base: {t['heat_base']};
      --header-tint: {t['header_tint']};
      --btn-fg: {t['btn_fg']};
    }}

    /* Hide Streamlit chrome */
    [data-testid="stSidebar"], [data-testid="collapsedControl"],
    header[data-testid="stHeader"] {{ display: none !important; }}
    footer {{ visibility: hidden; }}

    html, body, .stApp {{
      background: var(--bg) !important;
      color: var(--fg);
      font-family: 'IBM Plex Sans', 'IBM Plex Sans Arabic', -apple-system, sans-serif !important;
      font-size: 15px;
    }}
    .stApp > header {{ background: transparent; }}

    .block-container {{
      max-width: 1440px !important;
      padding: 28px 48px 80px !important;
      position: relative;
    }}
    .block-container::before {{
      content: '';
      position: absolute; top: 0; left: 0; right: 0;
      height: 320px;
      background: var(--header-tint);
      pointer-events: none;
      z-index: 0;
    }}
    .block-container > * {{ position: relative; z-index: 1; }}

    /* Typography */
    .serif {{ font-family: 'Instrument Serif', serif; letter-spacing: -0.01em; }}
    .mono {{ font-family: 'IBM Plex Mono', monospace; }}
    .num {{ font-family: 'Instrument Serif', serif; font-feature-settings: "tnum" 1, "lnum" 1; letter-spacing: -0.02em; }}
    .eyebrow {{
      font-family: 'IBM Plex Mono', monospace;
      font-size: 11px; font-weight: 500;
      letter-spacing: 0.14em; text-transform: uppercase;
      color: var(--fg-muted);
    }}
    h1, h2, h3, h4 {{ margin: 0; font-weight: 500; letter-spacing: -0.01em; }}

    /* Brand / header */
    .mz-topbar {{
      display: flex; align-items: center; justify-content: space-between;
      padding: 0 0 20px; gap: 24px;
    }}
    .mz-brand {{ display: flex; align-items: baseline; gap: 14px; }}
    .mz-brand-mark {{ font-family: 'Instrument Serif', serif; font-size: 32px; font-style: italic; color: var(--accent); line-height: 1; }}
    .mz-brand-name {{ font-family: 'Instrument Serif', serif; font-size: 28px; }}
    .mz-brand-sep {{ width: 1px; height: 20px; background: var(--border); margin: 0 4px; }}
    .mz-brand-market {{ font-family: 'IBM Plex Mono', monospace; font-size: 12px; letter-spacing: 0.18em; color: var(--fg-muted); text-transform: uppercase; }}
    .mz-clock-time {{ font-family: 'IBM Plex Mono', monospace; font-size: 13px; letter-spacing: 0.05em; color: var(--fg); }}
    .mz-clock-date {{ font-family: 'IBM Plex Mono', monospace; font-size: 10px; letter-spacing: 0.14em; color: var(--fg-dim); text-transform: uppercase; }}

    /* Title strip */
    .mz-title-row {{
      display: flex; justify-content: space-between; align-items: flex-end;
      padding: 40px 0 28px; border-bottom: 1px solid var(--border-soft); gap: 40px;
    }}
    .mz-title-main h1 {{
      font-family: 'Instrument Serif', serif;
      font-size: 64px; font-weight: 400; line-height: 1.05;
      letter-spacing: -0.03em; white-space: nowrap;
    }}
    .mz-title-main h1 .accent {{ color: var(--accent); font-style: italic; }}
    .mz-title-sub {{ margin-top: 16px; color: var(--fg-muted); font-size: 15px; max-width: 520px; }}
    .mz-title-meta {{ display: flex; gap: 28px; align-items: flex-end; }}
    .mz-stat {{ display: flex; flex-direction: column; gap: 6px; min-width: 96px; }}
    .mz-stat-label {{ font-family: 'IBM Plex Mono', monospace; font-size: 10px; letter-spacing: 0.14em; color: var(--fg-dim); text-transform: uppercase; }}
    .mz-stat-val {{ font-family: 'IBM Plex Mono', monospace; font-size: 14px; color: var(--fg); }}
    .mz-stat-val .up {{ color: var(--up); }} .mz-stat-val .down {{ color: var(--down); }}

    /* Native Streamlit toggle restyle — becomes our market pill */
    [data-testid="stToggle"] label {{
      background: var(--bg-raised);
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 4px 8px;
    }}

    /* Tabs — editorial underline */
    .stTabs [data-baseweb="tab-list"] {{
      gap: 4px;
      border-bottom: 1px solid var(--border-soft);
      background: transparent;
    }}
    .stTabs [data-baseweb="tab"] {{
      background: transparent !important;
      border: none !important;
      border-bottom: 2px solid transparent !important;
      border-radius: 0 !important;
      padding: 14px 22px 16px !important;
      font-family: 'IBM Plex Mono', monospace !important;
      font-size: 11px !important; font-weight: 500 !important;
      letter-spacing: 0.16em !important; text-transform: uppercase !important;
      color: var(--fg-muted) !important;
    }}
    .stTabs [data-baseweb="tab"]:hover {{ color: var(--fg) !important; background: transparent !important; transform: none !important; box-shadow: none !important; }}
    .stTabs [aria-selected="true"] {{
      color: var(--fg) !important;
      border-bottom-color: var(--accent) !important;
      background: transparent !important;
    }}

    /* Metrics */
    [data-testid="stMetric"] {{
      background: transparent;
      border: 1px solid var(--border-soft);
      border-radius: 2px;
      padding: 24px 28px 26px !important;
      min-height: 148px;
      transition: none;
    }}
    [data-testid="stMetric"]:hover {{ transform: none; background: transparent !important; box-shadow: none; }}
    [data-testid="stMetricLabel"] {{
      font-family: 'IBM Plex Mono', monospace !important;
      font-size: 10px !important; font-weight: 500 !important;
      letter-spacing: 0.16em !important; text-transform: uppercase !important;
      color: var(--fg-dim) !important;
    }}
    [data-testid="stMetricLabel"]::before {{
      content: ''; display: inline-block;
      width: 8px; height: 8px; background: var(--accent);
      margin-right: 8px; vertical-align: middle;
    }}
    [data-testid="stMetricValue"] {{
      font-family: 'Instrument Serif', serif !important;
      font-size: 44px !important; line-height: 1 !important;
      letter-spacing: -0.02em !important;
      margin-top: 14px !important;
    }}
    [data-testid="stMetricDelta"] {{
      font-family: 'IBM Plex Mono', monospace !important;
      font-size: 12px !important;
    }}

    /* Buttons */
    .stButton > button, .stDownloadButton > button {{
      font-family: 'IBM Plex Mono', monospace !important;
      font-size: 11px !important; font-weight: 500 !important;
      letter-spacing: 0.14em !important; text-transform: uppercase !important;
      padding: 12px 22px !important;
      border: 1px solid var(--border) !important;
      background: transparent !important;
      color: var(--fg) !important;
      border-radius: 2px !important;
      transition: all 0.2s ease !important;
    }}
    .stButton > button:hover, .stDownloadButton > button:hover {{
      border-color: var(--accent) !important;
      color: var(--accent) !important;
      transform: none !important;
      box-shadow: none !important;
    }}
    .stButton > button[kind="primary"], .stDownloadButton > button[kind="primary"] {{
      background: var(--accent) !important;
      border-color: var(--accent) !important;
      color: var(--btn-fg) !important;
    }}
    .stButton > button[kind="primary"]:hover {{
      filter: brightness(1.1);
      color: var(--btn-fg) !important;
    }}

    /* Selectbox */
    [data-baseweb="select"] > div {{
      background: var(--bg-raised) !important;
      border: 1px solid var(--border-soft) !important;
      border-radius: 2px !important;
    }}

    /* Dataframe */
    [data-testid="stDataFrame"] {{
      font-family: 'IBM Plex Mono', monospace !important;
      font-size: 13px !important;
      border: 1px solid var(--border-soft);
    }}

    /* Plotly chart container */
    [data-testid="stPlotlyChart"] {{
      border: 1px solid var(--border-soft);
      padding: 24px;
      background: transparent;
    }}

    /* Divider */
    hr, [data-testid="stDivider"] {{ border-color: var(--border-soft) !important; margin: 32px 0 !important; }}

    /* Footer */
    .mz-footer {{
      margin-top: 80px; padding-top: 28px;
      border-top: 1px solid var(--border-soft);
      display: flex; justify-content: space-between; align-items: center;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 11px; color: var(--fg-dim);
      letter-spacing: 0.1em; text-transform: uppercase;
    }}
    .mz-live-dot {{
      display: inline-block; width: 6px; height: 6px; border-radius: 50%;
      background: var(--accent); margin-right: 8px;
      box-shadow: 0 0 12px var(--accent);
      animation: mz-pulse 2s ease-in-out infinite;
    }}
    @keyframes mz-pulse {{ 0%,100% {{opacity:1}} 50% {{opacity:.35}} }}

    /* News card */
    .mz-news-item {{
      padding: 28px 0; border-bottom: 1px solid var(--border-soft);
      display: grid; grid-template-columns: 64px 1fr auto; gap: 24px;
    }}
    .mz-news-num {{ font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: var(--fg-dim); padding-top: 6px; letter-spacing: 0.1em; }}
    .mz-news-title {{ font-family: 'Instrument Serif', serif; font-size: 24px; line-height: 1.2; color: var(--fg); margin-bottom: 8px; }}
    .mz-news-title a {{ color: var(--fg); text-decoration: none; }}
    .mz-news-title a:hover {{ color: var(--accent); }}
    .mz-news-meta {{ font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: var(--fg-dim); letter-spacing: 0.08em; display: flex; gap: 16px; align-items: center; }}
    .mz-news-meta .ticker {{ color: var(--accent); padding: 2px 6px; border: 1px solid var(--accent); border-radius: 2px; }}

    /* RTL */
    [dir="rtl"] .block-container {{ direction: rtl; }}
    [dir="rtl"] * {{ font-family: 'IBM Plex Sans Arabic', 'IBM Plex Sans', sans-serif; }}
    [dir="rtl"] .serif, [dir="rtl"] .num, [dir="rtl"] h1, [dir="rtl"] h2 {{ font-family: 'Instrument Serif', 'IBM Plex Sans Arabic', serif; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
