import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="GeoRisk AI",
    layout="wide"
)

st.title("🌍 GeoRisk AI")
st.subheader("AI-Driven Geopolitical Risk Analytics Dashboard")

# Sidebar
st.sidebar.header("Filters")
country = st.sidebar.selectbox(
    "Select Country / Region",
    ["Global", "USA", "China", "Russia", "Middle East"]
)

years = np.arange(2012, 2023)
risk_scores = np.cumsum(np.random.randn(len(years))) + 60

data = pd.DataFrame({
    "Year": years,
    "Risk Score": risk_scores
})

# Main layout
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📈 Geopolitical Risk Trend Over Time")
    fig, ax = plt.subplots()
    ax.plot(data["Year"], data["Risk Score"], marker="o")
    ax.set_xlabel("Year")
    ax.set_ylabel("Risk Score")
    ax.grid(True)
    st.pyplot(fig)

with col2:
    st.markdown("### 📊 Current Risk Snapshot")
    st.metric(
        label=f"{country} Risk Level",
        value=f"{risk_scores[-1]:.1f}",
        delta=f"{risk_scores[-1] - risk_scores[-2]:.2f}"
    )

st.markdown("### 🧠 Analytical Insight")
st.write(
    f"""
The geopolitical risk trend for **{country}** indicates fluctuating risk levels
driven by political instability, economic pressures, and international conflicts.
Recent values suggest a sustained elevated risk environment.
"""
)
