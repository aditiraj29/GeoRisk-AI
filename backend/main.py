from fastapi import Depends
from datetime import datetime
import random

@app.get("/risk/summary")
def risk_summary(country: str = "Global"):
    return {
        "country": country,
        "risk_score": round(random.uniform(55, 82), 2),
        "trend": random.choice(["up", "down"]),
        "volatility": round(random.uniform(1.2, 4.6), 2),
        "updated": datetime.utcnow()
    }
