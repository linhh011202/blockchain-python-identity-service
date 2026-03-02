from fastapi import FastAPI
from app.core.config import Configs
from app.db.session import test_db_connection

config = Configs()
app = FastAPI(title=config.PROJECT_NAME)


@app.on_event("startup")
def startup():
    print(f"🚀 Starting {config.PROJECT_NAME}")
    try:
        test_db_connection()
        print("✅ Database connected")
    except Exception as e:
        print(f"⚠️  Database connection warning: {e}")


@app.get("/health")
def health():
    return {"status": "ok", "project": config.PROJECT_NAME}
