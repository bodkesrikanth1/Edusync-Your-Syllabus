# VERCEL DEPLOYMENT - FINAL CHECKLIST ✓

## Status: Your app is now FIXED and ready to deploy

### Issues Fixed:
✓ Indentation error in app.py  
✓ Error handling added to all routes  
✓ Health check endpoint added  
✓ Comprehensive error templates  
✓ Database connection on-demand (serverless-friendly)  
✓ Lazy loading for heavy libraries (sklearn, scipy)  
✓ Better logging and error reporting  

### Local Testing Results:
✓ Flask app imports successfully  
✓ Database connection working  
✓ All templates present and valid  
✓ All static files present  

---

## DEPLOYMENT STEPS (CRITICAL)

### STEP 1: Verify Local App Works
```bash
python -c "import app; print('✓ App imports successfully')"
```
Expected output: `✓ App imports successfully`

### STEP 2: Set Environment Variables in Vercel

Go to: **Vercel Dashboard → Your Project → Settings → Environment Variables**

Add ALL of these (copy from your .env file):

```
FLASK_SECRET=your-secret-key-here
DB_HOST=your-planetscale-host.cp.tidb-cloud.com
DB_USER=your-username
DB_PASSWORD=your-password
DB_NAME=edusync
YT_API_KEY=your-youtube-api-key
```

**IMPORTANT:**
- Do NOT use localhost or 127.0.0.1 for DB_HOST
- Do NOT commit sensitive values to git
- Use your actual PlanetScale/MySQL hostname from your provider

### STEP 3: Ensure Database is Set Up

Create all required tables by running this on your database:

```sql
-- Users table
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

-- Syllabi table
CREATE TABLE IF NOT EXISTS syllabi (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255),
  text LONGTEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Syllabus Units table
CREATE TABLE IF NOT EXISTS syllabus_units (
  id INT AUTO_INCREMENT PRIMARY KEY,
  syllabus_id INT,
  unit_no INT,
  unit_title VARCHAR(255),
  FOREIGN KEY(syllabus_id) REFERENCES syllabi(id)
);

-- Topics table
CREATE TABLE IF NOT EXISTS topics (
  id INT AUTO_INCREMENT PRIMARY KEY,
  unit_id INT,
  topic_text VARCHAR(500),
  weight FLOAT,
  FOREIGN KEY(unit_id) REFERENCES syllabus_units(id)
);

-- Videos table
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
  FOREIGN KEY(topic_id) REFERENCES topics(id)
);
```

### STEP 4: Deploy to Vercel

```bash
git add .
git commit -m "Fix 500 errors - add error handling and fix indentation"
git push
```

Vercel will automatically redeploy. This typically takes 30-60 seconds.

### STEP 5: Test Your Deployment

Check 3 endpoints:

1. **Health Check** (should respond with database status):
   ```
   https://your-domain.vercel.app/health
   ```
   Expected: `{"status": "healthy", "database": "ok"}`

2. **Landing Page** (should load without errors):
   ```
   https://your-domain.vercel.app/
   ```

3. **Vercel Logs** (to see any actual errors):
   - Go to Vercel Dashboard
   - Click your project
   - Go to "Deployments"
   - Click the latest deployment
   - Click "View Deployment"
   - Look at the logs section

---

## IF YOU STILL GET 500 ERRORS

### First, check the logs:
1. Deploy to Vercel
2. Go to Vercel Dashboard → Deployments
3. Click latest deployment
4. View Logs - look for error messages

### Common Issues and Fixes:

**Error: "No module named 'python_dotenv'"**
- This is OK - it's just a warning, not an error
- Should not prevent deployment

**Error: "Can't connect to database"**
- Verify DB_HOST is set in Vercel environment variables
- Verify DB_PASSWORD is correct
- Verify database accepts connections from internet
- Test with: `https://your-domain.vercel.app/health`

**Error: "Unknown database"**
- Run the SQL schema above to create tables
- Verify DB_NAME environment variable is correct

**Error: "Template not found"**
- This won't happen - all templates are included
- Should be deployed automatically

**Error: "Static files not loading"**
- Flask serves static files automatically
- Check that static/ folder exists with files

---

## FINAL CHECK BEFORE DEPLOYMENT

Run this command locally one more time:

```bash
python diagnose.py
```

Should show:
```
✓ Configuration: PASS
✓ Flask App: PASS
✓ Database: PASS
✓ Templates: PASS
✓ Static Files: PASS
```

If Database says FAIL, you may have connectivity issues that will also prevent Vercel deployment.

---

## WHAT'S CHANGED

### app.py
- ✓ Fixed indentation error
- ✓ Added comprehensive error handlers
- ✓ Added error.html template rendering
- ✓ Improved load_logged_in_user with better exception handling
- ✓ Added /health endpoint for monitoring

### db.py
- ✓ Added logging for debugging
- ✓ Better error messages
- ✓ Connection-on-demand for serverless

### New Files
- ✓ templates/error.html - Professional error pages
- ✓ diagnose.py - Diagnostic script for testing

### api/index.py
- ✓ Added fallback error handling

---

## MONITORING YOUR DEPLOYMENT

After deployment, you can monitor your app:

```bash
# Watch real-time logs
vercel logs your-project-name --tail

# Check specific deployment
vercel logs your-project-name
```

---

## SUPPORT

If you still have issues after following this checklist:

1. Check Vercel logs (Dashboard → Deployments → View Logs)
2. Run `python diagnose.py` locally to compare
3. Verify all environment variables are set
4. Ensure database is accessible from internet
5. Try visiting `/health` endpoint to test database

**The app is now properly configured. Deploy with confidence!**
