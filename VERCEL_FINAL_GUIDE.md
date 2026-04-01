# Vercel Deployment Fix - Complete Configuration Guide

## The Issue: Build Configuration Warning

When Vercel sees a `builds` section in `vercel.json`, it may warn about conflicting Project Settings. This is not an error, but we've now optimized the configuration to prevent it.

---

## ✅ What Was Fixed

### 1. **Updated vercel.json**
- Added explicit Python runtime: `python3.9`
- Added memory limit configuration
- Added environment variables configuration
- Optimized Lambda size to `50mb`

### 2. **Improved api/index.py**
- Better error handling and logging
- HTML error pages in addition to JSON
- Security headers (anti-XSS, anti-clickjacking)
- More detailed error reporting

### 3. **Added wsgi.py**
- Alternative entry point for Flask (if needed)
- Cleaner configuration option

---

## 📋 Deployment Checklist

### Before You Deploy:

**1. Verify Local Setup**
```bash
python diagnose.py
```
Expected: All tests PASS

**2. Commit Your Changes**
```bash
git add -A
git commit -m "Update Vercel configuration and improve error handling"
git push
```

**3. In Vercel Dashboard:**
- Go to: Settings → Environment Variables
- Add/verify these variables:
  ```
  FLASK_SECRET=your-secret-key
  DB_HOST=your-database-host.com
  DB_USER=your-database-user
  DB_PASSWORD=your-database-password
  DB_NAME=edusync
  YT_API_KEY=your-youtube-api-key
  ```

**4. Check Database:**
- Database is accessible from internet (not localhost)
- All tables are created (see schema below)
- User has proper permissions

---

## 🛠️ Database Schema (If Not Created)

Run this SQL on your PlanetScale/MySQL database:

```sql
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  full_name VARCHAR(255),
  email VARCHAR(255) UNIQUE,
  password_hash VARCHAR(255),
  role VARCHAR(50) DEFAULT 'student',
  college VARCHAR(255),
  department VARCHAR(255),
  year VARCHAR(50),
  enrollment_no VARCHAR(100),
  phone VARCHAR(20),
  preferences JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS syllabi (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255),
  text LONGTEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS syllabus_units (
  id INT AUTO_INCREMENT PRIMARY KEY,
  syllabus_id INT,
  unit_no INT,
  unit_title VARCHAR(255),
  FOREIGN KEY(syllabus_id) REFERENCES syllabi(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS topics (
  id INT AUTO_INCREMENT PRIMARY KEY,
  unit_id INT,
  topic_text VARCHAR(500),
  weight FLOAT,
  FOREIGN KEY(unit_id) REFERENCES syllabus_units(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS videos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  topic_id INT,
  youtube_id VARCHAR(100),
  title VARCHAR(500),
  channel_title VARCHAR(255),
  channel_id VARCHAR(100),
  duration_sec INT,
  view_count INT,
  published_at DATETIME,
  rating_score FLOAT,
  similarity FLOAT,
  final_score FLOAT,
  difficulty VARCHAR(50),
  url VARCHAR(500),
  FOREIGN KEY(topic_id) REFERENCES topics(id) ON DELETE CASCADE
);
```

---

## 🚀 Deploy to Vercel

```bash
# 1. Commit changes
git add .
git commit -m "Fix Vercel configuration and error handling"

# 2. Push to deployed branch
git push

# 3. Vercel will automatically build and deploy (30-60 seconds)
```

---

## ✅ Verify Deployment

### Test 1: Health Check
```
GET https://your-domain.vercel.app/health
```
Expected Response:
```json
{
  "status": "healthy",
  "database": "ok"
}
```

### Test 2: Landing Page
```
GET https://your-domain.vercel.app/
```
Expected: HTML page loads (no 500 error)

### Test 3: Check Logs
- Go to Vercel Dashboard
- Deployments tab
- Click latest deployment
- View Logs - should show successful deployment

---

## 🔍 If You Still See Errors

### Step 1: Check Vercel Logs
```bash
vercel logs <project-name> --tail
```

### Step 2: Look for Specific Errors

**"ModuleNotFoundError: No module named"**
- Check requirements.txt has package
- Run: `pip install -r requirements.txt` locally
- Commit requirements.txt if updated

**"Connection refused" or "Can't connect to database"**
- Verify DB_HOST is correct (not localhost)
- Verify database accepts internet connections
- Test connection locally first

**"Unknown database"**
- Run SQL schema above to create database/tables
- Verify DB_NAME environment variable is correct

**"IndentationError" or "SyntaxError"**
- Run `python -m py_compile app.py` to check syntax
- Run `python -c "import app"` to test imports

### Step 3: Test Locally First
```bash
python -c "from app import app; print('App imports OK')"
python diagnose.py
```

---

## 📁 File Structure (Should Have These)

```
.
├── app.py                          ✓ Main Flask app
├── api/
│   └── index.py                    ✓ Vercel entry point
├── wsgi.py                         ✓ Alternative WSGI entry
├── vercel.json                     ✓ Vercel config (updated)
├── requirements.txt                ✓ Python packages
├── .vercelignore                   ✓ Files to ignore
├── config.py                       ✓ Configuration
├── db.py                          ✓ Database module
├── nlp.py                         ✓ NLP module (lazy imports)
├── youtube_api.py                 ✓ YouTube API (lazy imports)
├── templates/
│   ├── base.html                  ✓ Base template
│   ├── landing.html               ✓ Landing page
│   ├── login.html                 ✓ Login page
│   ├── register.html              ✓ Register page
│   ├── index.html                 ✓ Dashboard
│   ├── results.html               ✓ Results page
│   ├── admin_login.html           ✓ Admin login
│   ├── admin_dashboard.html       ✓ Admin dashboard
│   └── error.html                 ✓ Error page (NEW)
├── static/
│   ├── style.css                  ✓ Styles
│   ├── app.js                     ✓ JavaScript
│   └── images/                    ✓ Images folder
└── diagnose.py                    ✓ Diagnostic tool
```

---

## 🔧 Advanced Troubleshooting

### Enable Debug Mode (Temporary Only!)
Add to app.py after creating the Flask app:
```python
app.config['DEBUG'] = True
```
Then redeploy. This will show detailed error messages.

### Check Environment Loading
```bash
# Test environment variables locally
python -c "from config import Config; print(Config.DB_HOST)"
```

### Test Database Connection
```bash
python -c "from db import get_conn; c = get_conn(); print('Connected!'); c.close()"
```

---

## 📊 Deployment Metrics

- **Build Time**: 30-60 seconds
- **Cold Start**: First request ~2-5 seconds (warm: <100ms)
- **Database**: Connected from api/index.py
- **Max Request Size**: 6MB (Vercel limit)
- **Max Execution Time**: 60 seconds (Vercel free tier)

---

## ⚙️ Configuration Priority

Vercel uses this priority for configuration:

1. **vercel.json** (in project root) ← We fixed this
2. **Project Settings** (Vercel Dashboard)
3. **Environment Variables** (Dashboard) ← Set yours here

Since we have vercel.json configured, Project Settings in Dashboard are ignored.

---

## 🎯 Next Actions

1. **Push your code with git**
2. **Wait for Vercel build** (watch the deployment log)
3. **Visit your project URL**
4. **Test the /health endpoint**
5. **If issues, check logs**

---

## 📞 Emergency Rollback

If deployment breaks, you can rollback:
1. Go to Vercel Dashboard
2. Deployments tab
3. Find previous working deployment
4. Click "..." menu
5. Select "Promote to Production"

---

Your application is now **fully optimized for Vercel deployment!**

**Deploy with confidence!** 🚀
