import pandas as pd
from transformers import pipeline

# Load cleaned data
df = pd.read_csv("data/processed/geopolitical_news_cleaned.csv")

# Load sentiment model
sentiment_pipeline = pipeline("sentiment-analysis")

sentiments = []

for i, text in enumerate(df["clean_text"]):
    if i % 500 == 0:
        print(f"Processing row {i} / {len(df)}")

    if not isinstance(text, str) or text.strip() == "":
        sentiments.append("NEUTRAL")
        continue

    result = sentiment_pipeline(text[:512])[0]["label"]
    sentiments.append(result)

df["sentiment"] = sentiments

# Save output
df.to_csv("data/processed/geopolitical_news_sentiment.csv", index=False)

print("Sentiment analysis completed successfully.")

