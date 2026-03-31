# Quick Commands for Database Migration

## 1️⃣ EXPORT Your Local Database

### Using mysqldump (Command Line)
```bash
# Simple export
mysqldump -u root -p edusync > edusync_backup.sql

# With password in command (less secure)
mysqldump -u root -p"sri1" edusync > edusync_backup.sql

# Export with drop database statement
mysqldump -u root -p edusync --add-drop-database > edusync_backup.sql
```

### On Windows Command Prompt:
```cmd
cd C:\Program Files\MySQL\MySQL Server 5.7\bin

mysqldump -u root -p edusync > C:\edusync_backup.sql

# Then enter password: sri1
```

**Result**: Creates `edusync_backup.sql` file (~5-10 MB)

---

## 2️⃣ IMPORT to Remote Database

### Step A: Create Database on Remote Server
```bash
mysql -h YOUR_DB_HOST -u admin -p"YOUR_PASSWORD" -e "CREATE DATABASE edusync CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### Step B: Import the Backup File
```bash
mysql -h YOUR_DB_HOST -u admin -p"YOUR_PASSWORD" edusync < edusync_backup.sql
```

### Combined with Progress (Better for large files)
```bash
pv edusync_backup.sql | mysql -h YOUR_DB_HOST -u admin -p"YOUR_PASSWORD" edusync
# Note: Requires 'pv' tool installed
```

---

## 3️⃣ VERIFY Import Succeeded

```bash
# Check database exists
mysql -h YOUR_DB_HOST -u admin -p"YOUR_PASSWORD" -e "SHOW DATABASES;" | grep edusync

# Check tables count
mysql -h YOUR_DB_HOST -u admin -p"YOUR_PASSWORD" edusync -e "SHOW TABLES;"

# Check user count
mysql -h YOUR_DB_HOST -u admin -p"YOUR_PASSWORD" edusync -e "SELECT COUNT(*) as user_count FROM users;"

# Expected output: 12 users
```

---

## 4️⃣ Complete Flow (AWS RDS Example)

### Prerequisites:
- AWS RDS instance created and running
- Database endpoint: `edusync.xxxxx.us-east-1.rds.amazonaws.com`
- Master user: `admin`
- Password: `YourStrongPassword123!`

### Commands to Run:

```bash
# 1. Export local database
mysqldump -u root -p"sri1" edusync > edusync_backup.sql

# 2. Create database on RDS
mysql -h edusync.xxxxx.us-east-1.rds.amazonaws.com -u admin -p"YourStrongPassword123!" -e "CREATE DATABASE edusync CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 3. Import backup to RDS
mysql -h edusync.xxxxx.us-east-1.rds.amazonaws.com -u admin -p"YourStrongPassword123!" edusync < edusync_backup.sql

# 4. Verify
mysql -h edusync.xxxxx.us-east-1.rds.amazonaws.com -u admin -p"YourStrongPassword123!" edusync -e "SELECT COUNT(*) FROM users;"
```

---

## 5️⃣ Using Python (If CLI Not Available)

```python
import mysql.connector
from mysql.connector import Error

# 1. EXPORT - Dump local database
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='sri1',
    database='edusync'
)

cursor = connection.cursor()

# Get all tables
cursor.execute("SHOW TABLES;")
tables = cursor.fetchall()

dump_content = "-- edusync Database Backup\n"
dump_content += "CREATE DATABASE IF NOT EXISTS edusync CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\n"
dump_content += "USE edusync;\n\n"

for table in tables:
    table_name = table[0]
    cursor.execute(f"SHOW CREATE TABLE {table_name};")
    create_statement = cursor.fetchone()[1]
    dump_content += create_statement + ";\n\n"
    
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    if rows:
        cursor.execute(f"DESCRIBE {table_name};")
        columns = [col[0] for col in cursor.fetchall()]
        for row in rows:
            dump_content += f"INSERT INTO {table_name} VALUES {row};\n"

# Save to file
with open('edusync_backup.sql', 'w') as f:
    f.write(dump_content)

print("✅ Database exported to edusync_backup.sql")
cursor.close()
connection.close()
```

---

## 6️⃣ Troubleshooting Common Issues

### Issue: "Access denied for user 'admin'"
```bash
# Verify credentials
mysql -h YOUR_DB_HOST -u admin -p
# Type password when prompted

# If still fails, reset user password on RDS:
# Use AWS Console → RDS → Modify → Change master password
```

### Issue: "Can't connect to MySQL server"
```bash
# Check if host is reachable
ping YOUR_DB_HOST

# Check if port 3306 is open
telnet YOUR_DB_HOST 3306

# Windows alternative
Test-NetConnection -ComputerName YOUR_DB_HOST -Port 3306
```

### Issue: Import is slow
```bash
# Disable foreign keys during import (faster)
mysql -h HOST -u USER -p DB < backup.sql
# Add this to top of backup.sql file:
# SET FOREIGN_KEY_CHECKS=0;
# ... data ...
# SET FOREIGN_KEY_CHECKS=1;
```

### Issue: "Table already exists"
```bash
# Use --drop-database flag
mysqldump -u root -p edusync --drop-database > backup.sql

# Or manually drop:
mysql -h HOST -u USER -p -e "DROP DATABASE edusync;"
```

---

## 7️⃣ One-Liner Commands (Copy-Paste Ready)

### Export to File
```bash
mysqldump -u root -p"sri1" edusync > edusync_backup.sql
```

### Create Remote DB + Import (AWS Example)
```bash
# First create DB:
mysql -h edusync.xxxxx.us-east-1.rds.amazonaws.com -u admin -p"PASSWORD" -e "CREATE DATABASE edusync CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Then import:
mysql -h edusync.xxxxx.us-east-1.rds.amazonaws.com -u admin -p"PASSWORD" edusync < edusync_backup.sql
```

### Quick Verify
```bash
mysql -h edusync.xxxxx.us-east-1.rds.amazonaws.com -u admin -p"PASSWORD" -e "USE edusync; SELECT COUNT(*) FROM users; SELECT COUNT(*) FROM syllabi; SELECT COUNT(*) FROM topics;"
```

---

## 8️⃣ Backup Strategies

### Daily Backup to File
```bash
# Create backup_db.sh
#!/bin/bash
DATE=$(date +%Y-%m-%d_%H-%M-%S)
mysqldump -h -u root -p"sri1" edusync > backups/edusync_${DATE}.sql
echo "✅ Backup created: edusync_${DATE}.sql"
```

### Backup to Cloud (AWS S3)
```bash
# Requires AWS CLI installed
mysqldump -u root -p"sri1" edusync | aws s3 cp - s3://my-bucket/edusync_backup.sql

# Restore from S3
aws s3 cp s3://my-bucket/edusync_backup.sql - | mysql -u admin -p"PASSWORD" edusync
```

---

## 📋 Checklist Before Pushing to Hugging Face

- [ ] Local database backed up: `edusync_backup.sql`
- [ ] Remote MySQL created (AWS RDS/DigitalOcean/Google Cloud)
- [ ] Database `edusync` created on remote server
- [ ] Backup imported successfully
- [ ] Verification query returned 12 users
- [ ] Secrets added to Hugging Face:
  - [ ] DB_HOST
  - [ ] DB_USER
  - [ ] DB_PASSWORD
  - [ ] DB_NAME
  - [ ] FLASK_SECRET
  - [ ] YT_API_KEY
- [ ] Code pushed to Hugging Face Space
- [ ] Build completed without errors
- [ ] App loads and works

---

## 🆘 Need Help?

### Contact Me:
- Database backup issues: Check mysqldump documentation
- AWS RDS setup: Check AWS documentation
- Connection errors: Check firewall/security groups

---

## Quick Reference Table

| Step | Command | Example |
|------|---------|---------|
| Export | `mysqldump -u root -p DB > file.sql` | `mysqldump -u root -p"sri1" edusync > edusync_backup.sql` |
| Create | `mysql -h HOST -u USER -p -e "CREATE DATABASE DB;"` | `mysql -h aws-host.rds.amazonaws.com -u admin -p"PASS" -e "CREATE DATABASE edusync;"` |
| Import | `mysql -h HOST -u USER -p DB < file.sql` | `mysql -h aws-host.rds.amazonaws.com -u admin -p"PASS" edusync < edusync_backup.sql` |
| Verify | `mysql -h HOST -u USER -p DB -e "SELECT COUNT(*) FROM T;"` | `mysql -h aws-host.rds.amazonaws.com -u admin -p"PASS" edusync -e "SELECT COUNT(*) FROM users;"` |

---

Make sure to replace:
- `YOUR_DB_HOST` with your actual RDS endpoint
- `YOUR_PASSWORD` with your actual password
- `sri1` with your local password

Happy deploying! 🚀
