#!/usr/bin/env python
"""
Diagnostic script to test database connection and configuration
"""

import os
import sys
from dotenv import load_dotenv

print("=" * 60)
print("EdusyncYourSyllabus - Database Connection Diagnostics")
print("=" * 60)

# Load environment variables
load_dotenv()

# Check .env file
print("\n1. Checking .env file...")
env_file_path = ".env"
if os.path.exists(env_file_path):
    print(f"   ✅ .env file found")
    with open(env_file_path, 'r') as f:
        content = f.read()
        print(f"   File size: {len(content)} bytes")
else:
    print(f"   ❌ .env file not found")

# Check environment variables
print("\n2. Checking environment variables...")
vars_to_check = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME', 'FLASK_SECRET', 'YT_API_KEY']
for var in vars_to_check:
    value = os.getenv(var, "NOT SET")
    if value == "NOT SET":
        print(f"   ❌ {var}: NOT SET")
    else:
        # Hide sensitive values
        if 'PASSWORD' in var or 'SECRET' in var or 'KEY' in var:
            print(f"   ✅ {var}: {value[:10]}...{value[-5:] if len(value) > 15 else ''}")
        else:
            print(f"   ✅ {var}: {value}")

# Try to import config
print("\n3. Testing config import...")
try:
    from config import Config
    print("   ✅ Config imported successfully")
    print(f"      DB_HOST:   {Config.DB_HOST}")
    print(f"      DB_USER:   {Config.DB_USER}")
    print(f"      DB_NAME:   {Config.DB_NAME}")
except Exception as e:
    print(f"   ❌ Config import failed: {e}")
    sys.exit(1)

# Try to import mysql.connector
print("\n4. Testing mysql.connector...")
try:
    import mysql.connector
    print("   ✅ mysql.connector imported successfully")
except Exception as e:
    print(f"   ❌ mysql.connector not available: {e}")
    sys.exit(1)

# Try to test connection (with timeout)
print("\n5. Testing MySQL connection...")
print(f"   Attempting to connect to {Config.DB_HOST}:{Config.DB_USER}:{Config.DB_NAME}")
try:
    import mysql.connector
    conn = mysql.connector.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        connection_timeout=5
    )
    print("   ✅ MySQL connection successful!")
    conn.close()
except mysql.connector.Error as err:
    if err.errno == 2003:
        print(f"   ❌ Cannot connect to MySQL server '{Config.DB_HOST}'")
        print("      Reason: MySQL service not running or server is not accessible")
    elif err.errno == 1045:
        print(f"   ❌ Access denied for user '{Config.DB_USER}'@'{Config.DB_HOST}'")
        print(f"      Check your DB_USER and DB_PASSWORD in .env file")
    else:
        print(f"   ❌ MySQL Error: {err}")
except Exception as e:
    print(f"   ❌ Connection error: {e}")

print("\n" + "=" * 60)
print("SUMMARY:")
print("=" * 60)
print("✅ = Working")
print("❌ = Problem")
print("\nNext steps:")
print("1. Ensure MySQL is running: start 'MySQL80' service (Windows)")
print("2. Verify credentials in .env file match your MySQL setup")
print("3. Check if database 'edusync' exists")
print("=" * 60)
