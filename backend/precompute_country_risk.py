import pandas as pd
import pycountry

# Load sentiment data
df = pd.read_csv("data/processed/geopolitical_news_sentiment.csv")
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])

# Sentiment → risk mapping
df["risk"] = df["sentiment"].map({
    "NEGATIVE": 70,
    "NEUTRAL": 40,
    "POSITIVE": 15
})

# Detect country names (one-time expensive step)
country_names = [c.name for c in pycountry.countries]

def extract_country(text):
    if not isinstance(text, str):
        return None
    text = text.lower()
    for c in country_names:
        if c.lower() in text:
            return c
    return None

df["country"] = df["text"].apply(extract_country)
df = df.dropna(subset=["country"])

# Weekly aggregation
weekly = (
    df
    .set_index("date")
    .groupby("country")
    .resample("W")["risk"]
    .mean()
    .reset_index()
)

# Save weekly risk
weekly.to_csv("data/processed/country_weekly_risk.csv", index=False)

# Latest risk per country
latest = (
    weekly
    .sort_values("date")
    .groupby("country")
    .tail(1)
)

latest.to_csv("data/processed/country_latest_risk.csv", index=False)

print("✅ Country risk precomputation completed")
