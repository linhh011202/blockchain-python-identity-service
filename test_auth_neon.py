#!/usr/bin/env python3
"""
Test file for user authentication using actual Neon database
Run: uv run python test_auth_neon.py
"""

import sys
from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlmodel import SQLModel

# Add project to path
sys.path.insert(0, "/home/linh012/workspace/BlockChain-Project-Python")

from app.core.config import Configs
from app.service.user_service import UserService
from app.repository.user_repository import UserRepository
from app.model.user_model import UserModel

# Load configuration from config.yaml
config = Configs()
print(f"📦 Using database: {config.POSTGRES_DB} at {config.POSTGRES_HOST}")

# Build database URL from actual config
database_url = (
    f"postgresql+psycopg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}"
    f"@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}"
    f"?sslmode=require"
)

# Create engine connected to Neon
engine = create_engine(database_url, echo=False)
SessionLocal = sessionmaker(bind=engine)

# Create all tables
print("🔧 Creating tables in Neon...")
SQLModel.metadata.create_all(engine)


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# Initialize repository and service
user_repo = UserRepository(get_session)
user_service = UserService(user_repo)

print("=" * 60)
print("TESTING USER AUTHENTICATION ON NEON")
print("=" * 60)

# Test 1: Register a new user
print("\n1️⃣  TEST REGISTER NEW USER")
print("-" * 60)
user, error = user_service.register_user("test_user_001@example.com", "password123")
if error:
    print(f"❌ FAILED: {error.message}")
else:
    print(f"✅ SUCCESS: User '{user.email}' registered")
    print(f"   ID: {user.id}")
    print(f"   Password Hash: {user.password[:50]}...")

# Test 2: Get user by email
print("\n2️⃣  TEST GET USER BY EMAIL")
print("-" * 60)
user, error = user_service.get_user_by_email("test_user_001@example.com")
if error:
    print(f"❌ FAILED: {error.message}")
else:
    print(f"✅ SUCCESS: Found user '{user.email}'")
    print(f"   ID: {user.id}")

# Test 3: Login with correct password
print("\n3️⃣  TEST LOGIN WITH CORRECT PASSWORD")
print("-" * 60)
user, error = user_service.login("test_user_001@example.com", "password123")
if error:
    print(f"❌ FAILED: {error.message}")
else:
    print(f"✅ SUCCESS: User '{user.email}' logged in successfully")
    print(f"   ID: {user.id}")

# Test 4: Login with wrong password
print("\n4️⃣  TEST LOGIN WITH WRONG PASSWORD")
print("-" * 60)
user, error = user_service.login("test_user_001@example.com", "wrongpassword")
if error:
    print(f"✅ SUCCESS (Expected Error): {error.message}")
else:
    print(f"❌ FAILED: Login should have failed with wrong password")

# Test 5: Login with non-existent user
print("\n5️⃣  TEST LOGIN WITH NON-EXISTENT USER")
print("-" * 60)
user, error = user_service.login("non_existent@example.com", "password123")
if error:
    print(f"✅ SUCCESS (Expected Error): {error.message}")
else:
    print(f"❌ FAILED: Login should have failed for non-existent user")

# Test 6: Register with duplicate email
print("\n6️⃣  TEST REGISTER WITH DUPLICATE EMAIL")
print("-" * 60)
user, error = user_service.register_user("test_user_001@example.com", "anotherpassword")
if error:
    print(f"✅ SUCCESS (Expected Error): {error.message}")
else:
    print(f"❌ FAILED: Should not allow duplicate email")

# Test 7: Register another user
print("\n7️⃣  TEST REGISTER ANOTHER USER")
print("-" * 60)
user, error = user_service.register_user("test_user_002@example.com", "securepass456")
if error:
    print(f"❌ FAILED: {error.message}")
else:
    print(f"✅ SUCCESS: User '{user.email}' registered")

# Test 8: Login with second user
print("\n8️⃣  TEST LOGIN SECOND USER")
print("-" * 60)
user, error = user_service.login("test_user_002@example.com", "securepass456")
if error:
    print(f"❌ FAILED: {error.message}")
else:
    print(f"✅ SUCCESS: User '{user.email}' logged in successfully")

# Verify data in database
print("\n" + "=" * 60)
print("VERIFY DATA IN NEON DATABASE")
print("=" * 60)
with engine.connect() as conn:
    result = conn.execute(
        text("SELECT id, email FROM tb_users ORDER BY id DESC LIMIT 5")
    )
    rows = result.fetchall()
    print(f"📊 Last 5 users in database:")
    for row in rows:
        print(f"   ID: {row[0]}, Email: {row[1]}")
    conn.commit()

print("\n" + "=" * 60)
print("TEST COMPLETE - Data should be saved in your Neon database!")
print("=" * 60)
