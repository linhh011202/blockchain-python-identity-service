from sqlalchemy import create_engine, text
from app.core.config import Configs

config = Configs()

# Build database URL from individual components
database_url = (
    f"postgresql+psycopg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}"
    f"@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}"
    f"?sslmode=require"
)

engine = create_engine(database_url, pool_pre_ping=True)


def test_db_connection():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
