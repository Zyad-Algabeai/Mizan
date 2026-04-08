# app.py
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from data.fetcher import get_tasi_overview, get_sector_data, get_stock_history
from ai.analyst import analyze_market, analyze_stock

# --- Page Config ---
st.set_page_config(
    page_title="Mizan | ميزان",
    page_icon="⚖️",
    layout="wide"
)

# --- Header ---
st.title("⚖️ Mizan | ميزان")
st.caption("AI-Powered Saudi Market Intelligence • تحليل ذكي لسوق الأسهم السعودي")
st.divider()

# --- Load Data ---
with st.spinner("Fetching Tadawul data..."):
    tasi_hist, tasi_info = get_tasi_overview(period="1mo")
    sector_data = get_sector_data(period="1mo")

# --- TASI Overview ---
col1, col2, col3 = st.columns(3)

latest = tasi_hist["Close"].iloc[-1]
prev = tasi_hist["Close"].iloc[-2]
change = ((latest - prev) / prev) * 100
monthly_change = ((latest - tasi_hist["Close"].iloc[0]) / tasi_hist["Close"].iloc[0]) * 100

with col1:
    st.metric("TASI Index", f"{latest:,.2f}", f"{change:+.2f}% today")
with col2:
    st.metric("Monthly Change", f"{monthly_change:+.2f}%")
with col3:
    st.metric("Volume", f"{tasi_hist['Volume'].iloc[-1]:,.0f}")

# --- TASI Chart ---
st.subheader("📈 TASI Performance")
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=tasi_hist.index,
    y=tasi_hist["Close"],
    mode="lines",
    name="TASI",
    line=dict(color="#00D4AA", width=2),
    fill="tozeroy",
    fillcolor="rgba(0, 212, 170, 0.1)"
))
fig.update_layout(
    height=300,
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)")
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- Sector Performance ---
st.subheader("🏢 Sector Performance")

sector_rows = []
for sector, stocks in sector_data.items():
    if stocks:
        avg_change = sum(s["change_pct"] for s in stocks) / len(stocks)
        sector_rows.append({
            "Sector": sector,
            "Avg Change (1M)": round(avg_change, 1),
            "Vision 2030": "✅" if stocks[0]["vision2030"] else "—"
            })

sector_df = pd.DataFrame(sector_rows).sort_values("Avg Change (1M)", ascending=False)

fig2 = px.bar(
    sector_df,
    x="Sector",
    y="Avg Change (1M)",
    color="Avg Change (1M)",
    color_continuous_scale=["#FF4444", "#FF8800", "#00D4AA"],
    text="Avg Change (1M)"
)
fig2.update_traces(texttemplate="%{text:+.1f}%", textposition="outside")
fig2.update_layout(
    height=350,
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    coloraxis_showscale=False,
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False, visible=False)
)
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# --- AI Market Brief ---
st.subheader("🤖 AI Market Brief")
if st.button("Generate Market Analysis ✨", type="primary"):
    with st.spinner("Mizan is analyzing the market..."):
        analysis = analyze_market(tasi_hist, sector_data)
    st.markdown(analysis)

st.divider()

# --- Stock Deep Dive ---
st.subheader("🔍 Stock Deep Dive")

all_stocks = []
for sector, stocks in sector_data.items():
    for s in stocks:
        all_stocks.append(s)

selected = st.selectbox(
    "Select a stock",
    options=[s["name"] for s in all_stocks],
    format_func=lambda x: x
)

selected_stock = next(s for s in all_stocks if s["name"] == selected)

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("Price", f"{selected_stock['price']} SAR")
with col_b:
    st.metric("1M Change", f"{selected_stock['change_pct']:+.2f}%")
with col_c:
    st.metric("Vision 2030", "✅ Aligned" if selected_stock["vision2030"] else "—")

stock_hist = get_stock_history(selected_stock["ticker"], period="3mo")
if not stock_hist.empty:
    fig3 = go.Figure()
    fig3.add_trace(go.Candlestick(
        x=stock_hist.index,
        open=stock_hist["Open"],
        high=stock_hist["High"],
        low=stock_hist["Low"],
        close=stock_hist["Close"],
        name=selected
    ))
    fig3.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_rangeslider_visible=False
    )
    st.plotly_chart(fig3, use_container_width=True)

if st.button("Analyze This Stock 🤖", type="primary"):
    with st.spinner(f"Analyzing {selected}..."):
        stock_analysis = analyze_stock(
            selected_stock["ticker"],
            selected_stock["name"],
            stock_hist
        )
        st.markdown(stock_analysis)