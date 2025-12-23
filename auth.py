from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from database import get_db

SECRET_KEY = "georisk-secret-key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

def create_user(email: str, password: str):
    conn = get_db()
    cursor = conn.cursor()
    hashed = hash_password(password)
    cursor.execute(
        "INSERT INTO users (email, hashed_password) VALUES (?, ?)",
        (email, hashed)
    )
    conn.commit()
    conn.close()

def authenticate_user(email: str, password: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

def create_token(email: str):
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
