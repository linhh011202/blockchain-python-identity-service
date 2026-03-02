from fastapi import FastAPI
from app.core.config import settings
from app.db.session import test_db_connection

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}