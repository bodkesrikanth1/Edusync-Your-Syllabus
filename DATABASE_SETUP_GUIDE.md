# Remote MySQL Database Setup for Hugging Face Deployment

## Overview
Your project currently uses a local MySQL database. For Hugging Face Spaces, you need a **remotely accessible MySQL database**. This guide walks through all steps.

---

## Option 1: AWS RDS (Recommended - Easy & Reliable)

### Step 1: Create AWS RDS Instance

1. Go to https://aws.amazon.com
2. Sign up or login to AWS Console
3. Navigate to **RDS** → **Create Database**
4. Choose:
   - **Engine**: MySQL 8.0 (Latest)
   - **DB Instance Identifier**: `edusync-db`
   - **Master Username**: `admin` (or your choice)
   - **Master Password**: Strong password (20+ characters!)
   - **Instance Class**: `db.t3.micro` (Free tier eligible)
   - **Storage**: 20 GB
   - **Public Accessibility**: **YES** (Required for Hugging Face)

5. Click **Create Database**
6. Wait 5-10 minutes for instance to be created

### Step 2: Get Connection Details

Once the database is created:
1. Go to **RDS Databases**
2. Click on your `edusync-db` instance
3. Copy these credentials:
   ```
   DB_HOST: <endpoint-xxx.rds.amazonaws.com>
   DB_USER: admin
   DB_PASSWORD: your-password
   DB_NAME: edusync
   ```

### Step 3: Configure Security Group

1. In RDS Console, click **Connectivity & security**
2. Find **VPC security groups**
3. Click on the security group
4. Add an **Inbound Rule**:
   - **Type**: MySQL/Aurora
   - **Port**: 3306
   - **Source**: `0.0.0.0/0` (Allow all - secure later)
   - Click **Save**

---

## Option 2: DigitalOcean MySQL Cluster (Budget-Friendly)

1. Go to https://www.digitalocean.com
2. Create account
3. Navigate to **Managed Databases** → **Create Database**
4. Choose MySQL
5. Select basic dropdown plan ($15/month)
6. Finalize and create
7. Copy connection details once created

---

## Option 3: Google Cloud SQL (Alternative)

1. Go to https://cloud.google.com
2. Create project
3. Navigate to **SQL** → **Create Instance**
4. Choose MySQL 8.0
5. Set up instance (Standard edition)
6. Create and get connection details
7. Authorize networks: Add `0.0.0.0/0` for Hugging Face

---

## Step 4: Export Local Database

### Using MySQL Command Line

```bash
# Export your local edusync database to a SQL file
mysqldump -h localhost -u root -p edusync > edusync_backup.sql
# Enter your password when prompted
```

This creates a file `edusync_backup.sql` with all your data and schema.

### Using SQLyog (What you're using)

1. In SQLyog, right-click on **edusync** database
2. Choose **Backups** → **Backup Database**
3. Choose **MySQL Dump** format
4. Save as `edusync_backup.sql`

---

## Step 5: Import Database to Remote Server

### Option A: Using MySQL Command Line

```bash
# First, create the database on remote server
mysql -h YOUR_DB_HOST -u admin -p -e "CREATE DATABASE edusync;"

# Then import the dump file
mysql -h YOUR_DB_HOST -u admin -p edusync < edusync_backup.sql
# Enter your password when prompted
```

### Option B: Using SQLyog (Easier)

1. Create new connection to your remote MySQL:
   - **Host**: Your RDS endpoint (or remote host)
   - **Username**: admin
   - **Password**: Your password
2. Create database: `edusync`
3. Right-click on **edusync** → **Restore** → Select your SQL dump file

### Option C: Using phpMyAdmin

1. Access your remote database admin panel
2. Create database `edusync`
3. Go to **Import** tab
4. Upload your `edusync_backup.sql` file
5. Click Import

**Wait for import to complete** (Check progress in the console)

---

## Step 6: Verify Remote Database

### Test Connection Using MySQL CLI

```bash
mysql -h YOUR_DB_HOST -u admin -p edusync -e "SELECT COUNT(*) FROM users;"
```

You should see a count of users (should be 12 based on your export).

### Test in Python (Optional)

```python
import mysql.connector

conn = mysql.connector.connect(
    host="YOUR_DB_HOST",
    user="admin",
    password="YOUR_PASSWORD",
    database="edusync"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM users LIMIT 1;")
print(cursor.fetchone())
cursor.close()
conn.close()
```

---

## Step 7: Configure Hugging Face Spaces

### Add Environment Secrets

In your Hugging Face Space:
1. Go to **Settings** → **Repository secrets**
2. Add each variable:

```
DB_HOST=your-rds-endpoint.rds.amazonaws.com
DB_USER=admin
DB_PASSWORD=your-strong-password
DB_NAME=edusync
FLASK_SECRET=your-random-secret-key-32-chars
YT_API_KEY=your-youtube-api-key
```

### Update config.py (Already done, verify):

Your `config.py` should look like:
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET", "change-this")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "edusync")
    YT_API_KEY = os.getenv("YT_API_KEY", "")
```

✅ This is already configured!

---

## Step 8: Test Hugging Face Connection

Once you push to Hugging Face:

1. Check Space logs in **Settings → Build**
2. You should see connection messages
3. Try using the app:
   - Register a new user
   - Upload a syllabus
   - Parse it

If you get database errors, check:
- Host is correct (no extra spaces)
- Port 3306 is open on remote server
- Firewall allows `0.0.0.0/0` (or just Hugging Face IPs)
- Database name is `edusync`

---

## Troubleshooting Connection Issues

### "Access denied for user"
```
Solution:
1. Verify username and password
2. Check if user exists on remote database
3. Verify user has permissions on edusync database
```

### "Can't connect to MySQL server"
```
Solution:
1. Verify host is correct (no typos)
2. Check if security group allows inbound on port 3306
3. Ensure public accessibility is enabled
4. Test with: mysql -h HOST -u USER -p
```

### "Unknown database 'edusync'"
```
Solution:
1. Verify you created the database first
2. Check if import succeeded completely
3. Verify database name is lowercase 'edusync'
```

### "Lost connection to MySQL"
```
Solution:
1. Check if Hugging Face timeout setting
2. Verify database is still running
3. Check if max connections reached
```

---

## Database Backup Strategy

### Regular Backups (Important!)

Set up weekly backups:

```bash
# Create a backup script (backup.sh)
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -h YOUR_DB_HOST -u admin -p"YOUR_PASSWORD" edusync > backup_$DATE.sql
```

Store backups in:
- AWS S3
- Google Drive
- OneDrive
- Local backup

---

## Security Best Practices

✅ **DO:**
- Use strong passwords (32+ characters)
- Encrypt connections (use SSL/TLS)
- Restrict IP addresses (if possible)
- Regular backups
- Use environment variables for secrets
- Enable database monitoring

❌ **DON'T:**
- Share database passwords
- Commit credentials to git
- Use `0.0.0.0/0` permanently (only for testing)
- Keep default passwords
- Disable SSL connections

---

## Performance Tips

For better performance on Hugging Face:

1. **Connection Pooling** ✅ Already set up in db.py
   ```python
   pool = pooling.MySQLConnectionPool(
       pool_size=10,
       ...
   )
   ```

2. **Database Indexes** ✅ Already created in schema

3. **Query Optimization:**
   - Avoid N+1 queries
   - Use prepared statements (already doing)
   - Cache frequently accessed data

4. **Scale resources** if needed:
   - Increase RDS instance size
   - Add read replicas
   - Use caching (Redis/Memcached)

---

## Quick Summary

```
Step 1: Create remote MySQL (AWS RDS recommended)
Step 2: Get DB_HOST, DB_USER, DB_PASSWORD
Step 3: Export local database (mysqldump)
Step 4: Import to remote database (mysql)
Step 5: Verify connection works
Step 6: Add secrets to Hugging Face Settings
Step 7: Push code to Hugging Face
Step 8: Test that app works with remote DB
```

---

## Important Database Credentials

For your project, you'll need these values ready:

```
# Remote Database
DB_HOST=___.rds.amazonaws.com
DB_USER=admin
DB_PASSWORD=_______________
DB_NAME=edusync
PORT=3306

# Flask
FLASK_SECRET=your-32-char-random-string

# YouTube
YT_API_KEY=AIzaSy...
```

⚠️ **Never commit these to git or share publicly!**

---

## Resources

- [AWS RDS MySQL Guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MySQL.html)
- [DigitalOcean Managed Databases](https://docs.digitalocean.com/products/databases/)
- [MySQL Dump Guide](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html)
- [Connection Pooling in Python](https://dev.mysql.com/doc/connector-python/en/connector-python-pooling.html)

---

## Questions?

Check Hugging Face Space logs for detailed error messages. Most issues are:
- Firewall/Security group blocking connections
- Wrong host/username/password
- Database not yet created on remote server
- Import didn't complete successfully

Good luck with your deployment! 🚀
