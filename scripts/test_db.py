#!/usr/bin/env python
"""Test database connection"""
import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, text

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
os.chdir(project_root)

try:
    from app.core.config import Configs

    config = Configs()

    db_url = (
        f"postgresql+psycopg://{config.POSTGRES_USER}:***"
        f"@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}"
    )
    print(f"Testing DB: {db_url}...")

    engine = create_engine(
        f"postgresql+psycopg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}"
        f"@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}?sslmode=require",
        pool_pre_ping=True,
    )

    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar_one()

    print(f"✅ DB OK - Query returned: {result}")
    sys.exit(0)
except Exception as e:
    print(f"❌ DB FAIL - {type(e).__name__}: {str(e).split(chr(10))[0]}")
    sys.exit(1)
