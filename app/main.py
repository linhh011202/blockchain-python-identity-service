from fastapi import FastAPI
from app.core.config import Configs
from app.db.session import test_db_connection

config = Configs()
app = FastAPI(title=config.PROJECT_NAME)



@app.get("/health")
def health():
    return {"status": "ok", "project": config.PROJECT_NAME}
