#!/usr/bin/env python3
"""
Diagnostic script to identify Edusync deployment issues.
Run this to test all components before deploying.
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported."""
    print("\n=== Testing Imports ===")
    packages = [
        ('flask', 'Flask'),
        ('mysql.connector', 'MySQL Connector'),
        ('python_dotenv', 'python-dotenv'),
        ('docx', 'python-docx'),
        ('requests', 'requests'),
    ]
    
    all_ok = True
    for module, name in packages:
        try:
            __import__(module)
            print(f"[OK] {name}")
        except ImportError as e:
            print(f"[FAIL] {name}: {e}")
            all_ok = False
    
    return all_ok

def test_config():
    """Test if configuration loads correctly."""
    print("\n=== Testing Configuration ===")
    try:
        from config import Config
        print(f"[OK] Config loaded")
        print(f"  - SECRET_KEY: {'SET' if Config.SECRET_KEY else 'NOT SET'}")
        print(f"  - DB_HOST: {Config.DB_HOST or 'NOT SET'}")
        print(f"  - DB_USER: {Config.DB_USER or 'NOT SET'}")
        print(f"  - DB_PASSWORD: {'SET' if Config.DB_PASSWORD else 'NOT SET'}")
        print(f"  - DB_NAME: {Config.DB_NAME or 'NOT SET'}")
        print(f"  - YT_API_KEY: {'SET' if Config.YT_API_KEY else 'NOT SET'}")
        
        if not all([Config.DB_HOST, Config.DB_USER, Config.DB_NAME]):
            print("[FAIL] Missing required database configuration!")
            return False
        
        return True
    except Exception as e:
        print(f"[FAIL] Config error: {e}")
        return False

def test_app_import():
    """Test if the Flask app can be imported."""
    print("\n=== Testing Flask App ===")
    try:
        from app import app
        print(f"[OK] Flask app imported successfully")
        return True
    except Exception as e:
        print(f"[FAIL] Failed to import app: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database():
    """Test database connectivity."""
    print("\n=== Testing Database Connection ===")
    try:
        from db import get_conn
        from config import Config
        
        print(f"Attempting to connect to {Config.DB_HOST}...")
        conn = get_conn()
        print(f"[OK] Database connection successful")
        
        try:
            cur = conn.cursor()
            cur.execute("SELECT VERSION()")
            version = cur.fetchone()
            print(f"[OK] MySQL version: {version[0]}")
            
            # Check if tables exist
            cur.execute("SHOW TABLES")
            tables = [t[0] for t in cur.fetchall()]
            print(f"[OK] Database tables: {', '.join(tables) if tables else 'None found'}")
            
            required_tables = ['users', 'syllabi', 'syllabus_units', 'topics', 'videos']
            missing = [t for t in required_tables if t not in tables]
            if missing:
                print(f"[FAIL] Missing tables: {', '.join(missing)}")
                return False
            
            cur.close()
        finally:
            conn.close()
        
        return True
    except Exception as e:
        print(f"[FAIL] Database connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_templates():
    """Test if all required templates exist."""
    print("\n=== Testing Templates ===")
    required_templates = [
        'landing.html',
        'login.html',
        'register.html',
        'base.html',
        'index.html',
        'results.html',
        'admin_login.html',
        'admin_dashboard.html',
        'error.html',
    ]
    
    template_dir = 'templates'
    all_ok = True
    
    for template in required_templates:
        path = os.path.join(template_dir, template)
        if os.path.exists(path):
            print(f"[OK] {template}")
        else:
            print(f"[FAIL] {template} not found")
            all_ok = False
    
    return all_ok

def test_static_files():
    """Test if required static files exist."""
    print("\n=== Testing Static Files ===")
    required_files = [
        'style.css',
        'app.js',
    ]
    
    static_dir = 'static'
    all_ok = True
    
    for filename in required_files:
        path = os.path.join(static_dir, filename)
        if os.path.exists(path):
            print(f"[OK] {filename}")
        else:
            print(f"[FAIL] {filename} not found")
            all_ok = False
    
    return all_ok

def main():
    """Run all diagnostic tests."""
    print("=" * 50)
    print("EDUSYNC DIAGNOSTIC TEST")
    print("=" * 50)
    
    results = {
        'Imports': test_imports(),
        'Configuration': test_config(),
        'Flask App': test_app_import(),
        'Database': test_database(),
        'Templates': test_templates(),
        'Static Files': test_static_files(),
    }
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    for test_name, passed in results.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 50)
    if all_passed:
        print("[OK] All tests passed! Ready to deploy.")
        return 0
    else:
        print("[FAIL] Some tests failed. See above for details.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
