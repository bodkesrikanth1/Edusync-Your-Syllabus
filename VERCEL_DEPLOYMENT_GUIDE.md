# Deploy Flask App to Vercel - Complete Step-by-Step Guide

## ⚠️ IMPORTANT: Vercel vs Your Project

**Vercel is primarily for:**
- ✅ Next.js applications
- ✅ Static websites
- ✅ Serverless functions
- ✅ Frontend (React, Vue, etc.)

**For Flask backends, Vercel:**
- ✅ Works but with limitations
- ✅ Requires specific setup
- ✅ Database must be external (not local)
- ✅ Free tier good for learning
- ⚠️ Has execution time limits (10 seconds on free)

**Better alternatives:**
- Hugging Face Spaces (recommended) ⭐
- Railway.app
- Render.com
- PythonAnywhere

---

## 🚀 BUT... Can We Deploy to Vercel?

**YES!** Your Flask app can run on Vercel, but with these steps:

### Architecture for Vercel:
```
Frontend (HTML/CSS/JS)
    ↓
Vercel Functions (Flask backend)
    ↓
External Database (PlanetScale/Railway)
```

---

## 📋 REQUIREMENTS BEFORE STARTING

✅ GitHub account (required for Vercel)
✅ Vercel account (free)
✅ PlanetScale database created (from previous steps)
✅ Project files ready
✅ .env file with secrets

---

## 🔧 STEP-BY-STEP DEPLOYMENT TO VERCEL

### STEP 1: Create vercel.json (Configuration File)

Create a new file in your project root:

**File:** `vercel.json`

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "FLASK_APP": "app.py",
    "FLASK_ENV": "production"
  }
}
```

**What this does:**
- Tells Vercel how to run your Flask app
- Routes all requests to your Flask application
- Sets environment variables

---

### STEP 2: Modify app.py for Vercel

You need to wrap your Flask app for Vercel Serverless Functions.

**Find the bottom of app.py** (where you have `if __name__ == '__main__':`):

Replace this:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

With this:
```python
# For Vercel deployment
if __name__ == '__main__':
    # Local development
    app.run(debug=True, host='0.0.0.0', port=5000)

# Export app for Vercel
# Don't add anything after this line
```

**The app object is already exported**, so Vercel can find it automatically.

---

### STEP 3: Update requirements.txt

Add these Vercel-specific packages to your `requirements.txt`:

```
Flask==3.0.3
python-dotenv==1.0.1
mysql-connector-python==9.0.0
requests==2.32.3
scikit-learn==1.5.1
numpy==2.0.1
pandas==2.2.2
python-dateutil==2.9.0.post0
python-docx>=0.8.11
gunicorn>=21.2.0
werkzeug==3.0.0
```

---

### STEP 4: Create .vercelignore File

This file tells Vercel what NOT to upload:

**File:** `.vercelignore`

```
__pycache__
*.pyc
.env
.env.local
.env.*.local
.git
.gitignore
node_modules
.next
out
build
dist
venv
env
*.db
*.sqlite
```

---

### STEP 5: Push to GitHub

Your code needs to be on GitHub for Vercel to deploy:

```bash
# Initialize git if not already done
git init

# Add files
git add .

# Commit
git commit -m "Prepare for Vercel deployment"

# Add GitHub remote (replace YOUR_USERNAME and YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

### STEP 6: Create Vercel Account

1. Go to https://vercel.com/signup
2. Sign up (easiest: use GitHub)
3. Authorize Vercel to access GitHub
4. You'll be redirected to dashboard

---

### STEP 7: Create Vercel Project

#### Method 1: Import from GitHub (EASIEST)

```
1. Go to https://vercel.com
2. Click "Add New" → "Project"
3. Click "Import Git Repository"
4. Find your repository in the list
5. Click "Import"
```

#### Method 2: Import with URL

```
1. Go to https://vercel.com/import
2. Enter: https://github.com/YOUR_USERNAME/YOUR_REPO
3. Click "Import"
```

---

### STEP 8: Configure Environment Variables

**In Vercel Dashboard:**

```
1. Click on your project
2. Go to "Settings"
3. Find "Environment Variables"
4. Add each variable:
```

Add these variables:

| Key | Value |
|-----|-------|
| `FLASK_SECRET` | Your secret key (from .env) |
| `DB_HOST` | your-db.psdb.cloud |
| `DB_USER` | Your PlanetScale username |
| `DB_PASSWORD` | Your PlanetScale password |
| `DB_NAME` | edusync |
| `YT_API_KEY` | Your YouTube API key |
| `FLASK_ENV` | production |

**Steps to add:**
```
1. Key field: Type variable name (e.g., DB_HOST)
2. Value field: Type the value
3. Click "Add"
4. Repeat for all variables
5. Click "Save"
```

---

### STEP 9: Deploy

**Automatic Deployment:**

Once you push to GitHub, Vercel automatically builds and deploys!

```
1. GitHub push triggers build
2. Vercel receives webhook
3. Vercel builds (installs dependencies)
4. Vercel deploys your app
5. Get a live URL
```

**Manual Deploy:**

In Vercel Dashboard:
```
1. Click project
2. Click "Deployments"
3. Click "Redeploy" on any deployment
```

---

### STEP 10: Get Your Live URL

After deployment completes:

```
1. Go to Vercel dashboard
2. Click on your project
3. Top shows: https://your-project.vercel.app
4. Click the URL to open your live app
```

---

## 🎯 COMPLETE FILE STRUCTURE

Your GitHub repo should look like this:

```
your-repo/
├── app.py
├── config.py
├── db.py
├── nlp.py
├── youtube_api.py
├── requirements.txt
├── vercel.json          ← NEW
├── .vercelignore        ← NEW
├── .env                 (don't push, use Vercel secrets)
├── .env.example
├── .gitignore
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── admin_dashboard.html
│   └── ...
├── static/
│   ├── style.css
│   ├── app.js
│   └── images/
└── README.md
```

---

## 📝 EXAMPLE vercel.json

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "FLASK_APP": "app.py",
    "FLASK_ENV": "production"
  },
  "buildCommand": "pip install -r requirements.txt"
}
```

---

## 📝 EXAMPLE .vercelignore

```
__pycache__
*.pyc
.env
.env.local
.git
node_modules
venv
env
*.db
*.sqlite
.DS_Store
```

---

## ✅ DEPLOYMENT CHECKLIST

### Before Push:
- [ ] vercel.json created
- [ ] .vercelignore created
- [ ] app.py is Flask app
- [ ] requirements.txt updated
- [ ] No secrets in code (use .env)
- [ ] .env file is NOT in git

### GitHub:
- [ ] Repository created
- [ ] All files pushed
- [ ] Code is on GitHub

### Vercel:
- [ ] Account created
- [ ] Project imported
- [ ] Environment variables added:
  - [ ] DB_HOST
  - [ ] DB_USER
  - [ ] DB_PASSWORD
  - [ ] DB_NAME
  - [ ] FLASK_SECRET
  - [ ] YT_API_KEY
- [ ] Build completed
- [ ] App is live

---

## 🆘 COMMON ISSUES & FIXES

### Issue: "Module not found"
```
Fix:
1. Check requirements.txt has all packages
2. Verify spelling
3. Redeploy: git push
```

### Issue: "Database connection failed"
```
Fix:
1. Verify DB credentials in Vercel settings
2. Check PlanetScale allows external connections
3. Test locally first: python app.py
```

### Issue: "Static files not loading"
```
Fix:
1. Add to vercel.json:
   "staticRoutes": [
     {
       "src": "/static/(.*)",
       "dest": "static/$1"
     }
   ]
2. Redeploy
```

### Issue: "Function invocation timeout (>10s)"
```
Reason: Free tier has 10-second limit
Fix:
1. Optimize database queries
2. Cache results
3. Upgrade to Pro ($20/mo) for 60-second timeout
4. Consider different platform (Hugging Face better for this)
```

### Issue: "Build Error"
```
Fix:
1. Check build logs: Deployments → Click failed build
2. Read error message
3. Fix locally, test: python app.py
4. Push to GitHub again
```

---

## 🔗 YOUR VERCEL URL

After successful deployment:

```
Your app will be at:
https://your-project-name.vercel.app

Different URLs for each branch:
├─ main: https://your-project-name.vercel.app
├─ develop: https://develop.your-project-name.vercel.app
└─ feature: https://feature.your-project-name.vercel.app
```

---

## 🚀 DEPLOYMENT FLOW SUMMARY

```
1. Create vercel.json ✅
2. Create .vercelignore ✅
3. Update requirements.txt ✅
4. Push to GitHub ✅
5. Create Vercel account ✅
6. Import GitHub repository ✅
7. Add environment variables ✅
8. Wait for build (2-3 min) ✅
9. Get live URL ✅
10. Test your app 🎉
```

---

## 📊 VERCEL VS HUGGING FACE

| Feature | Vercel | Hugging Face |
|---------|--------|--------------|
| **Cost** | Free | Free |
| **Timeout** | 10s (free) | None |
| **Best For** | Frontend | Full stack |
| **Database** | External only | External only |
| **Ease** | Medium | Easy |
| **Scaling** | Good | Good |
| **Support** | Good | Good |

**For your Flask app:**
- **Recommendation: Hugging Face** (better for Python/Flask)
- Vercel works but has execution time limits
- Use Vercel if you have frontend-heavy app

---

## 💡 MY RECOMMENDATION

### For EdusyncYourSyllabus:

**Better Options (in order):**
1. **Hugging Face Spaces** ⭐⭐⭐ (Best for Flask)
2. **Railway.app** ⭐⭐ (Good & cheap)
3. **Render.com** ⭐⭐ (Good free tier)
4. **Vercel** ⭐ (Works but has limits)

**Why not push Vercel to the top?**
- 10-second timeout on free tier
- Your NLP/parsing might exceed this
- Database queries might be slow
- Hugging Face better for long-running tasks

---

## 🎯 IF YOU STILL WANT VERCEL

**Go with this plan:**

1. **Use PlanetScale for database** ✅ (Free)
2. **Create vercel.json** ✅ (Provided above)
3. **Push to GitHub** ✅
4. **Create Vercel account** ✅
5. **Import repository** ✅
6. **Add environment variables** ✅
7. **Deploy** ✅

**Total time: 30-45 minutes**

---

## 📚 REFERENCE FILES

### vercel.json (Copy-Paste Ready)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "FLASK_APP": "app.py",
    "FLASK_ENV": "production"
  }
}
```

### .vercelignore (Copy-Paste Ready)
```
__pycache__
*.pyc
.env
.env.local
.git
venv
env
*.db
```

---

## ✨ AFTER DEPLOYMENT

### Test Your App:
1. Go to your Vercel URL
2. Test login page
3. Test register page
4. Test file upload
5. Test parsing
6. Test YouTube search

### Monitor:
- Vercel Dashboard → Analytics
- Check error logs
- Monitor database queries

### Updates:
```bash
# Make changes locally
nano app.py

# Push to GitHub (automatic redeploy)
git add .
git commit -m "Fix bug"
git push
```

---

## 🆘 STILL CONFUSED?

**I recommend:** Use Hugging Face Spaces instead!

Reasons:
- ✅ Better suited for Flask apps
- ✅ No timeout limits
- ✅ Better debugging
- ✅ Easier deployment
- ✅ Works out of the box

**But if you prefer Vercel:**
Follow the steps above. It will work!

---

## 🚀 DEPLOY NOW!

Ready? Here's the quick checklist:

```
☐ vercel.json created
☐ .vercelignore created  
☐ requirements.txt updated
☐ GitHub account ready
☐ Code pushed to GitHub
☐ Vercel account created
☐ Project imported
☐ Env vars added
☐ Deployment complete
☐ Testing app works

YOU'RE LIVE! 🎉
```

Questions? Let me know!
