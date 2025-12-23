import pandas as pd
import matplotlib.pyplot as plt

# Load sentiment data
df = pd.read_csv("data/processed/geopolitical_news_sentiment.csv")

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Drop rows with invalid dates
df = df.dropna(subset=["date"])

# Simple risk mapping from sentiment
def sentiment_to_risk(s):
    if s == "NEGATIVE":
        return 70
    elif s == "NEUTRAL":
        return 40
    else:
        return 15

df["risk"] = df["sentiment"].apply(sentiment_to_risk)

# Weekly average risk
weekly_risk = df.set_index("date").resample("W")["risk"].mean()

# Plot
plt.figure(figsize=(10, 5))
plt.plot(weekly_risk.index, weekly_risk.values, marker="o")
plt.title("Geopolitical Risk Trend Over Time")
plt.xlabel("Week")
plt.ylabel("Average Risk Score")
plt.grid(True)

# Save plot
plt.savefig("results/geopolitical_risk_trend.png")
plt.show()

print("Risk trend analysis completed and plot saved.")
