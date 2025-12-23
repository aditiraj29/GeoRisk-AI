import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="GeoRisk AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM DARK UI + FONT ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(180deg, #020617, #020617);
    color: #e5e7eb;
}

.kpi {
    background: linear-gradient(135deg, #1e293b, #020617);
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #1e293b;
    text-align: center;
    animation: fadeIn 0.6s ease-in;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(8px);}
    to {opacity: 1; transform: translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR BRANDING ----------------
st.sidebar.markdown("""
## 🌍 **GeoRisk AI**
### *An AI-Driven Geopolitical Risk Prediction Platform*
---
""")

# ---------------- LOAD PRECOMPUTED DATA ----------------
latest = pd.read_csv("data/processed/country_latest_risk.csv")
trends = pd.read_csv("data/processed/country_trend_direction.csv")
alerts = pd.read_csv("data/processed/country_alerts.csv")
windows = pd.read_csv("data/processed/country_time_windows.csv")
weekly = pd.read_csv("data/processed/country_weekly_risk.csv")

weekly["date"] = pd.to_datetime(weekly["date"])

# ---------------- SIDEBAR CONTROLS ----------------
st.sidebar.subheader("⚙️ Analysis Controls")

countries = sorted(latest["country"].unique())
selected_countries = st.sidebar.multiselect(
    "Select Countries (max 3)",
    countries,
    default=countries[:2],
    max_selections=3
)

time_window = st.sidebar.selectbox(
    "Time Window",
    ["7_DAYS", "30_DAYS", "90_DAYS"]
)

threshold = st.sidebar.slider("Risk Sensitivity", 20, 80, 55)
run = st.sidebar.button("🚀 Run Analysis")

# ---------------- HEADER ----------------
st.title("GeoRisk AI")
st.caption("Enterprise-grade AI system for geopolitical risk intelligence")

st.markdown("---")

if run and selected_countries:

    # ================= KPI CARDS =================
    st.subheader("📊 Key Risk Indicators")
    cols = st.columns(len(selected_countries))

    for i, country in enumerate(selected_countries):
        r = latest[latest["country"] == country]["risk"].values[0]
        t = trends[trends["country"] == country]["trend"].values[0]

        cols[i].markdown(
            f"<div class='kpi'><h2>{r:.1f}</h2><p>{country}</p><small>{t}</small></div>",
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ================= WORLD MAP =================
    st.subheader("🗺️ Country-Level Risk Map")

    map_rows = []
    for c in selected_countries:
        iso = pycountry.countries.lookup(c).alpha_3
        risk = latest[latest["country"] == c]["risk"].values[0]
        map_rows.append({"iso": iso, "country": c, "risk": risk})

    map_df = pd.DataFrame(map_rows)

    fig_map = px.choropleth(
        map_df,
        locations="iso",
        color="risk",
        hover_name="country",
        color_continuous_scale="RdYlGn_r",
        range_color=(0, 100)
    )

    fig_map.update_layout(
        paper_bgcolor="#020617",
        plot_bgcolor="#020617",
        font_color="white"
    )

    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("---")

    # ================= TIME WINDOW COMPARISON =================
    st.subheader(f"📈 Risk Comparison — {time_window.replace('_', ' ')}")

    window_data = windows[
        (windows["window"] == time_window) &
        (windows["country"].isin(selected_countries))
    ]

    fig_bar = px.bar(
        window_data,
        x="country",
        y="avg_risk",
        range_y=[0, 100],
        color="country"
    )

    fig_bar.update_layout(
        paper_bgcolor="#020617",
        plot_bgcolor="#020617",
        font_color="white"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # ================= TREND =================
    st.subheader("📉 Risk Trend")

    trend_df = weekly[weekly["country"].isin(selected_countries)]
    fig_trend = px.line(
        trend_df,
        x="date",
        y="risk",
        color="country",
        markers=True
    )

    fig_trend.update_layout(
        paper_bgcolor="#020617",
        plot_bgcolor="#020617",
        font_color="white"
    )

    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")

    # ================= ALERTS =================
    st.subheader("🚨 Early-Warning Alerts")

    alert_df = alerts[alerts["country"].isin(selected_countries)]
    if alert_df.empty:
        st.success("No active alerts detected.")
    else:
        for _, a in alert_df.iterrows():
            st.warning(f"{a['country']}: {a['message']}")

    st.markdown("---")

    # ================= AI EXPLANATION =================
    st.subheader("🧠Risk Explanation")

    st.markdown("""
    This risk assessment is driven by:
    - Sustained negative geopolitical sentiment  
    - Trend acceleration across recent time windows  
    - Alert triggers indicating instability signals  

    **Note:** This is an early-warning intelligence signal, not a deterministic forecast.
    """)

else:
    st.info("👈 Select countries and click **Run Analysis**")
