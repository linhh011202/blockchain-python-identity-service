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
    # Use localhost:5433 for testing from host machine
    # Docker containers use db:5432 internally
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "5433")
    DB_USER = os.environ.get("DB_USER", "postgres")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
    DB_NAME = os.environ.get("DB_NAME", "blockchain_db")

    db_url = f"postgresql+psycopg://{DB_USER}:***@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    engine = create_engine(
        f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        pool_pre_ping=True,
    )

    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar_one()

    print(f" Hihi, successfully running! DB OK - Query returned: {result}")
    sys.exit(0)
except Exception as e:
    print(f" DB FAIL - {type(e).__name__}: {str(e).split(chr(10))[0]}")
    sys.exit(1)
