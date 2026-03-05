#!/usr/bin/env python3
"""
Test file for user authentication (register and login)
Run: uv run python test_auth.py
"""

import sys
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlmodel import SQLModel

# Add project to path
sys.path.insert(0, "/home/linh012/workspace/BlockChain-Project-Python")

from app.service.user_service import UserService
from app.repository.user_repository import UserRepository
from app.model.user_model import UserModel

# Setup in-memory SQLite database for testing
engine = create_engine("sqlite:///:memory:", echo=False)
SQLModel.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)


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
print("TESTING USER AUTHENTICATION")
print("=" * 60)

# Test 1: Register a new user
print("\n1️⃣  TEST REGISTER NEW USER")
print("-" * 60)
user, error = user_service.register_user("john_doe@example.com", "password123")
if error:
    print(f"❌ FAILED: {error.message}")
else:
    print(f"✅ SUCCESS: User '{user.email}' registered")
    print(f"   ID: {user.id}")
    print(f"   Password Hash: {user.password[:50]}...")

# Test 2: Get user by email
print("\n2️⃣  TEST GET USER BY EMAIL")
print("-" * 60)
user, error = user_service.get_user_by_email("john_doe@example.com")
if error:
    print(f"❌ FAILED: {error.message}")
else:
    print(f"✅ SUCCESS: Found user '{user.email}'")
    print(f"   ID: {user.id}")

# Test 3: Login with correct password
print("\n3️⃣  TEST LOGIN WITH CORRECT PASSWORD")
print("-" * 60)
user, error = user_service.login("john_doe@example.com", "password123")
if error:
    print(f"❌ FAILED: {error.message}")
else:
    print(f"✅ SUCCESS: User '{user.email}' logged in successfully")
    print(f"   ID: {user.id}")

# Test 4: Login with wrong password
print("\n4️⃣  TEST LOGIN WITH WRONG PASSWORD")
print("-" * 60)
user, error = user_service.login("john_doe@example.com", "wrongpassword")
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
user, error = user_service.register_user("john_doe@example.com", "anotherpassword")
if error:
    print(f"✅ SUCCESS (Expected Error): {error.message}")
else:
    print(f"❌ FAILED: Should not allow duplicate email")

# Test 7: Register another user
print("\n7️⃣  TEST REGISTER ANOTHER USER")
print("-" * 60)
user, error = user_service.register_user("jane_smith@example.com", "securepass456")
if error:
    print(f"❌ FAILED: {error.message}")
else:
    print(f"✅ SUCCESS: User '{user.email}' registered")

# Test 8: Login with second user
print("\n8️⃣  TEST LOGIN SECOND USER")
print("-" * 60)
user, error = user_service.login("jane_smith@example.com", "securepass456")
if error:
    print(f"❌ FAILED: {error.message}")
else:
    print(f"✅ SUCCESS: User '{user.email}' logged in successfully")

print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print("All tests completed! Check results above.")
print("=" * 60)
