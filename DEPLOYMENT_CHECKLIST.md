# Hugging Face Spaces - Deployment Checklist

## Pre-Deployment (Local Setup)

### Environment Setup
- [ ] Create `.env.local` from `.env.example`
- [ ] Fill in your local MySQL credentials
- [ ] Add your YouTube API key
- [ ] Test locally: `python app.py`
- [ ] Verify all features work (upload, NLP, YouTube search)

### Code Review
- [ ] No hardcoded credentials in code ✓ (config.py updated)
- [ ] requirements.txt is clean ✓ (removed `pip install` line)
- [ ] Flask secret key is strong
- [ ] Database connection logic handles environment variables ✓

### Git Preparation
- [ ] Initialize git: `git init`
- [ ] Create `.gitignore` ✓ (already created)
- [ ] Add files: `git add .`
- [ ] Create initial commit: `git commit -m "Initial project setup"`

---

## Hugging Face Setup

### Create Spaces Repository

- [ ] Go to https://huggingface.co/new-space
- [ ] Fill in details:
  - **Space name**: `edusync-your-syllabus` (use your preferred name)
  - **Owner**: Your username
  - **Space SDK**: Choose **"Docker"**
  - **License**: Choose appropriate license
  - **Visibility**: Public or Private
- [ ] Click "Create Space"

### Clone and Deploy

```bash
# Get the clone URL from your new space (it will be shown on creation)
git clone https://huggingface.co/spaces/YOUR_USERNAME/your-space-name
cd your-space-name

# Copy your project files here (keep the README.md if it exists)
# Copy these files/folders:
# - app.py
# - config.py
# - db.py
# - nlp.py
# - youtube_api.py
# - requirements.txt
# - templates/
# - static/
# - .env.example
# - Dockerfile (replace if needed)
# - start.sh
# - DEPLOYMENT_GUIDE.md
# - SPACES_README.md

# Add all files
git add .

# Commit
git commit -m "Initial EdusyncYourSyllabus deployment"

# Push to Hugging Face
git push
```

**The space will start building automatically!** ✓

---

## Configuration on Hugging Face

### Add Environment Secrets

1. Go to your Space URL: `https://huggingface.co/spaces/YOUR_USERNAME/your-space-name`
2. Click **Settings** (gear icon)
3. Find **"Repository secrets"**
4. Add each secret individually:

```
FLASK_SECRET = your-very-random-secure-secret-key-at-least-32-chars

DB_HOST = your-mysql-host.com (or ip address)

DB_USER = your-database-username

DB_PASSWORD = your-database-password

DB_NAME = edusync

YT_API_KEY = AIzaSy... (your YouTube API key)
```

### Important Notes
- [ ] Do NOT include these values in code or .env file
- [ ] Use strong FLASK_SECRET (32+ characters is recommended)
- [ ] Restart space after changing secrets (automatic in most cases)
- [ ] Never log in as admin with default credentials - create new admin account

---

## Verify Deployment

### Wait for Build
- [ ] Check build status in **Settings → Build**
- [ ] Wait 5-10 minutes for deployment
- [ ] Look for any errors in build logs

### Test the Application
Once build completes successfully:
- [ ] Access your Space: `YOUR-SPACE-URL` (provided by Hugging Face)
- [ ] Test register page
- [ ] Test login functionality
- [ ] Test file upload
- [ ] Test syllabus parsing
- [ ] Test YouTube search and ranking
- [ ] Test admin dashboard

---

## Security Checklist

- [ ] No sensitive data in git commits
- [ ] All secrets stored in Hugging Face secrets, NOT in code
- [ ] FLASK_SECRET is unique and strong (32+ characters)
- [ ] MySQL host is secure (whitelist IPs if possible)
- [ ] Create new admin user (don't use default)
- [ ] Test password hashing works (should use bcrypt)
- [ ] Disable debug mode in production ✓ (Flask production mode set)

---

## Optional: Custom Domain

- [ ] (Optional) Set custom domain in Space Settings
- [ ] (Optional) Enable persistent storage if needed
- [ ] (Optional) Set up monitoring/logging

---

## Troubleshooting

### Build Fails
1. Check build logs: Settings → Build
2. Verify all dependencies in requirements.txt
3. Check Dockerfile syntax
4. Try rebuilding: Settings → Restart Space

### Application Won't Run
1. Check runtime logs
2. Verify FLASK_SECRET is set
3. Verify DB_HOST is correct and accessible
4. Check MySQL connection (test locally first)

### Database Connection Errors
1. Ensure MySQL is accessible from internet
2. Check firewall/security group rules
3. Verify credentials are correct
4. Test connection with MySQL client locally

### Features Not Working
1. Check if all environment variables are set
2. Verify YouTube API key is valid and enabled
3. Check file upload size limits
4. Review error logs in Space interface

---

## Post-Deployment

- [ ] Monitor space logs regularly
- [ ] Test all features work correctly
- [ ] Create backup of database
- [ ] Update README with Space URL
- [ ] Share Space URL with users
- [ ] Set up contact/feedback mechanism
- [ ] Plan for scaling if needed

---

## Quick Command Reference

```bash
# Local testing
pip install -r requirements.txt
python app.py

# Git operations
git status
git add .
git commit -m "description"
git push  # This triggers Space build on HF

# Restart Space remotely (if needed)
# Go to Settings → Restart Space button

# View Logs
# Settings → Repo info → Build (for build logs)
# Space main page (for runtime logs)
```

---

## Need Help?

- **Hugging Face Docs**: https://huggingface.co/docs/hub/spaces
- **Docker Docs**: https://huggingface.co/docs/hub/spaces-sdks-docker
- **Flask Deployment**: https://flask.palletsprojects.com/deploying/
- **Report Issues**: Via Hugging Face Space settings

---

## Success Indicators

✓ Space builds without errors  
✓ Application starts successfully  
✓ Can access the web interface  
✓ Database connection works  
✓ User can register and login  
✓ File upload and parsing works  
✓ YouTube API integration works  
✓ Admin dashboard accessible  

You're ready to deploy! 🚀
