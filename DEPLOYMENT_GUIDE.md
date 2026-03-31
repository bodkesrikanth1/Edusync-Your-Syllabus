# EdusyncYourSyllabus - Hugging Face Spaces Deployment Guide

## Overview
This guide explains how to deploy the EdusyncYourSyllabus Flask application to Hugging Face Spaces.

## Prerequisites
- Hugging Face account (sign up at https://huggingface.co)
- Git installed on your machine
- Your application files ready

## Step 1: Prepare Your Project

### 1.1 Update requirements.txt
Ensure your `requirements.txt` is properly formatted. Remove any malformed lines like:
```
pip install python-docx
```

It should just be:
```
python-docx
```

### 1.2 Create/Update Environment Files
- Copy `.env.example` to `.env.local` for local testing
- Never commit your real `.env` file to version control

## Step 2: Database Setup Options

### Option A: MySQL Database (Recommended for Persistence)
If you want to use your existing MySQL database hosted elsewhere:
1. Ensure your MySQL database is accessible from the internet
2. Set these environment variables in Hugging Face Spaces secrets:
   - `DB_HOST`: Remote MySQL host
   - `DB_USER`: Database username
   - `DB_PASSWORD`: Database password
   - `DB_NAME`: Database name

### Option B: SQLite Database (Simpler for testing)
SQLite is file-based and works well for smaller projects:
1. The database file will be stored in `/tmp/data/edusync.db`
2. Set `DB_TYPE=sqlite` in environment variables

**Note**: On Hugging Face Spaces, the `/tmp` directory is ephemeral (temporary). For persistent storage, consider Option A with MySQL or use Hugging Face's persistent storage feature.

## Step 3: Create Hugging Face Space

1. Go to https://huggingface.co/new-space
2. Fill in the details:
   - **Space name**: `edusync-your-syllabus` (or your preferred name)
   - **License**: Choose appropriate license
   - **Space SDK**: Select "Docker"
3. Click "Create Space"

## Step 4: Configure Environment Variables

In your Spaces settings (Settings → Repository secrets):

```
FLASK_SECRET=your-super-secret-key-here
DB_HOST=your-database-host
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_NAME=edusync
YT_API_KEY=your-youtube-api-key
```

## Step 5: Push Your Code to Hugging Face

### Using Git (Recommended)

```bash
# Clone the space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/edusync-your-syllabus
cd edusync-your-syllabus

# Copy your project files (keep Dockerfile)
# Copy all your Python files, templates, static files, etc.

# Add and commit
git add .
git commit -m "Initial deployment"

# Push to Hugging Face
git push
```

### Structure after git push:
```
Dockerfile
app.py
config.py
db.py
nlp.py
youtube_api.py
requirements.txt
.env.example
templates/
  base.html
  index.html
  login.html
  register.html
  admin_dashboard.html
  ...
static/
  style.css
  app.js
  images/
  ...
```

## Step 6: Configure Port

The Dockerfile already sets port 7860 (required for Spaces). Flask will automatically use this when running on Hugging Face Spaces.

## Step 7: Update Configuration for Production

Your `config.py` should automatically read from environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET", "dev")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "edusync")
    YT_API_KEY = os.getenv("YT_API_KEY", "")
```

## Step 8: Verify Deployment

Once you push:
1. Go to your Space: `huggingface.co/spaces/YOUR_USERNAME/edusync-your-syllabus`
2. The space will build and deploy automatically (takes ~5-10 minutes)
3. Monitor the "Build" tab for any errors
4. Once deployed, access your app via the provided URL

## Troubleshooting

### Port Issues
- Hugging Face Spaces only accepts port 7860
- Flask must bind to `0.0.0.0` to receive external connections

### Database Connection Errors
- Verify MySQL host is publicly accessible
- Check firewall rules allow connections from Hugging Face
- Test credentials locally first

### Missing Environment Variables
- Check all secrets are set in Spaces settings
- Restart the space after adding/changing secrets
- Check logs: Settings → Logs

### File Upload Issues
- Temporary files are stored in `/tmp` (ephemeral)
- For persistent uploads, implement a cloud storage solution (S3, etc.)

## Advanced: Persistent Storage

For persistent file storage beyond temporary directories:

1. **Option 1**: Upload to cloud storage (AWS S3, Google Cloud Storage)
2. **Option 2**: Save to MySQL BLOB (if using MySQL)
3. **Option 3**: Use Hugging Face Datasets API

## Monitoring & Logs

- Check space build logs: Settings → Repo info → Build
- Runtime logs appear in the Space interface
- Set up error tracking with services like Sentry for production

## Security Best Practices

1. Never commit `.env` files
2. Use strong `FLASK_SECRET` values
3. Rotate API keys regularly
4. Use environment variables for all sensitive data
5. Enable HTTPS (automatic on Hugging Face)
6. Implement rate limiting for APIs
7. Validate all user inputs

## Next Steps

1. Push your project following Step 5
2. Monitor build logs
3. Test all features once deployed
4. Set up custom domain (optional) in Settings
5. Share your Space with the community

## Additional Resources

- [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [Docker Deployment Guide](https://huggingface.co/docs/hub/spaces-sdks-docker)
- [Flask Deployment Best Practices](https://flask.palletsprojects.com/en/3.0.x/deploying/)

---

For questions or issues, check the Hugging Face community forums or contact support.
