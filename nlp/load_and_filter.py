import pandas as pd

# Load dataset
df = pd.read_json(
    "data/raw/News_Category_Dataset_v3.json",
    lines=True
)

print("Total articles:", len(df))

# Geopolitical categories
geo_categories = [
    "WORLD",
    "POLITICS",
    "U.S. NEWS",
    "BUSINESS",
    "ENVIRONMENT"
]

df = df[df["category"].isin(geo_categories)]

print("Geopolitical articles:", len(df))

# Combine text
df["text"] = df["headline"] + ". " + df["short_description"]

# Keep required columns
df = df[["date", "category", "text"]]

# Save processed file
df.to_csv("data/processed/geopolitical_news.csv", index=False)

print("Filtered dataset saved successfully.")
