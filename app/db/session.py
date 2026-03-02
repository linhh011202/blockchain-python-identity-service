from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.database.url, pool_pre_ping=True)

def test_db_connection():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))