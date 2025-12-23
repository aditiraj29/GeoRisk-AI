import pandas as pd
import re

# Load filtered geopolitical news
df = pd.read_csv("data/processed/geopolitical_news.csv")

def clean_text(text):
    if pd.isna(text):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# Apply cleaning
df["clean_text"] = df["text"].apply(clean_text)

# Save cleaned data
df.to_csv("data/processed/geopolitical_news_cleaned.csv", index=False)

print("Text preprocessing completed successfully.")
