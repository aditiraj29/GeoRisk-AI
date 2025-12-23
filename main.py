
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import create_users_table
from auth import create_user, authenticate_user, create_token
import feedparser
app = FastAPI(title="GeoRisk AI API")

create_users_table()

class User(BaseModel):
    email: str
    password: str

@app.get("/")
def root():
    return {"status": "GeoRisk AI backend running"}

@app.post("/signup")
def signup(user: User):
    try:
        create_user(user.email, user.password)
        return {"message": "User created successfully"}
    except:
        raise HTTPException(status_code=400, detail="User already exists")

@app.post("/login")
def login(user: User):
    auth_user = authenticate_user(user.email, user.password)
    if not auth_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(user.email)
    return {"access_token": token}
def fetch_geopolitical_news(query="geopolitical risk"):
    feed_url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(feed_url)

    articles = []
    for entry in feed.entries[:10]:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published
        })

    return articles


from datetime import datetime
import random

@app.get("/risk/summary")
def risk_summary(country: str = "Global"):
    return {
        "country": country,
        "risk_score": round(random.uniform(60, 85), 2),
        "trend": random.choice(["up", "down"]),
        "volatility": round(random.uniform(1.5, 4.5), 2),
        "updated": datetime.utcnow().isoformat()
    }

@app.get("/news")
def get_latest_news(country: str = "Global"):
    query = f"{country} geopolitical risk"
    return fetch_geopolitical_news(query)


