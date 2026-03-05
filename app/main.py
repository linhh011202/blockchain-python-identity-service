from fastapi import FastAPI
from app.core.config import Configs
from app.core.container import Container
from app.api.v1.routes import routers
from app.db.session import test_db_connection

config = Configs()
app = FastAPI(title=config.PROJECT_NAME)

# Setup dependency injection container
container = Container()
app.container = container

# Include API routes
app.include_router(routers, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok", "project": config.PROJECT_NAME}
