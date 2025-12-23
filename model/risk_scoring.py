import pandas as pd

# Load sentiment data
df = pd.read_csv("data/processed/geopolitical_news_sentiment.csv")

def compute_risk(row):
    risk = 0

    # Sentiment-based risk
    if row["sentiment"] == "NEGATIVE":
        risk += 60
    elif row["sentiment"] == "NEUTRAL":
        risk += 30
    else:
        risk += 10

    # Category-based risk
    if row["category"] == "WORLD":
        risk += 25
    elif row["category"] == "POLITICS":
        risk += 20
    elif row["category"] == "U.S. NEWS":
        risk += 15
    elif row["category"] == "BUSINESS":
        risk += 10
    elif row["category"] == "ENVIRONMENT":
        risk += 10

    return min(risk, 100)

# Apply risk scoring
df["risk_score"] = df.apply(compute_risk, axis=1)

# Aggregate average risk by category
category_risk = df.groupby("category")["risk_score"].mean().reset_index()

# Save results
category_risk.to_csv("results/geopolitical_risk_scores.csv", index=False)

print("Geopolitical risk scoring completed successfully.")
