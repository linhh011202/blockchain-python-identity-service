from fastapi import FastAPI
from app.core.config import settings
from app.db.session import test_db_connection

app = FastAPI()

@app.on_event("startup")
def start():
    print(f"Starting {settings.app.name} in {settings.app.env}")
    test_db_connection()
    print("✅ DB connected")

@app.get("/health")
def health():
    return {"status": "ok"}