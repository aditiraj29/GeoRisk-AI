import pandas as pd

# Load weekly risk data
df = pd.read_csv("data/processed/country_weekly_risk.csv")
df["date"] = pd.to_datetime(df["date"])

WINDOWS = {
    "7_DAYS": 1,
    "30_DAYS": 4,
    "90_DAYS": 12
}

rows = []

for country, group in df.groupby("country"):
    group = group.sort_values("date")

    for window_name, weeks in WINDOWS.items():
        if len(group) < weeks:
            continue

        window_avg = group.tail(weeks)["risk"].mean()

        rows.append({
            "country": country,
            "window": window_name,
            "avg_risk": round(window_avg, 2)
        })

# Save time-window data
result = pd.DataFrame(rows)
result.to_csv("data/processed/country_time_windows.csv", index=False)

print("✅ Time-window scenarios computed successfully")
