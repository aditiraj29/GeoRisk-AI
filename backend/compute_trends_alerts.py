import pandas as pd

# Load weekly country risk
df = pd.read_csv("data/processed/country_weekly_risk.csv")
df["date"] = pd.to_datetime(df["date"])

trend_rows = []
alert_rows = []

RISK_THRESHOLD = 65      # escalation threshold
SPIKE_DELTA = 15         # sudden spike threshold

for country, group in df.groupby("country"):
    group = group.sort_values("date")

    if len(group) < 3:
        continue

    last = group.iloc[-1]["risk"]
    prev = group.iloc[-2]["risk"]
    prev2 = group.iloc[-3]["risk"]

    # -------- Trend Direction --------
    if last > prev > prev2:
        trend = "INCREASING 📈"
    elif last < prev < prev2:
        trend = "DECREASING 📉"
    else:
        trend = "STABLE ➖"

    trend_rows.append({
        "country": country,
        "trend": trend,
        "latest_risk": round(last, 2)
    })

    # -------- Alerts --------
    if last >= RISK_THRESHOLD:
        alert_rows.append({
            "country": country,
            "alert_type": "THRESHOLD_BREACH",
            "message": f"Risk crossed threshold ({last:.1f})"
        })

    if last - prev >= SPIKE_DELTA:
        alert_rows.append({
            "country": country,
            "alert_type": "SUDDEN_SPIKE",
            "message": f"Sudden risk spike of {last - prev:.1f}"
        })

# Save outputs
trend_df = pd.DataFrame(trend_rows)
alert_df = pd.DataFrame(alert_rows)

trend_df.to_csv("data/processed/country_trend_direction.csv", index=False)
alert_df.to_csv("data/processed/country_alerts.csv", index=False)

print("✅ Trend direction and alerts computed successfully")
