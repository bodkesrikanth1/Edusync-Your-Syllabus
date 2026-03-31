# Quick Deployment to Hugging Face Spaces

This folder now contains everything needed to deploy to Hugging Face Spaces.

## Quick Start (5 minutes)

### Step 1: Create a Hugging Face Space
1. Go to https://huggingface.co/new-space
2. Choose "Docker" as SDK
3. Name it `edusync-your-syllabus`

### Step 2: Get Git Clone Command
After creating the space, Hugging Face will show you a git clone command. Copy it.

### Step 3: Initialize Deployment

```bash
# Clone the space
git clone https://huggingface.co/spaces/YOUR_USERNAME/edusync-your-syllabus
cd edusync-your-syllabus

# Copy all your project files here (but keep the Dockerfile from Spaces)
# Copy: app.py, config.py, db.py, nlp.py, youtube_api.py, requirements.txt, templates/, static/

# Add files
git add .
git commit -m "Initial deployment"
git push
```

### Step 4: Set Environment Variables
1. Go to your Space settings
2. Find "Repository secrets"
3. Add these secrets:
   ```
   FLASK_SECRET=your-random-secret-key
   DB_HOST=your-mysql-host
   DB_USER=your-db-user
   DB_PASSWORD=your-db-password
   DB_NAME=edusync
   YT_API_KEY=your-youtube-api-key
   ```

### Step 5: Wait for Deployment
The space will build automatically. Check the "Build" tab for progress.

## Files Included

- **Dockerfile** - Docker configuration for Spaces
- **requirements.txt** - All Python dependencies
- **.env.example** - Template for environment variables
- **.gitignore** - Git ignore rules (prevent committing secrets)
- **DEPLOYMENT_GUIDE.md** - Detailed deployment guide with troubleshooting

## Important Notes

⚠️ **Security**
- Never commit your `.env` file with real credentials
- Use Hugging Face "Repository secrets" instead
- Keep API keys private

⚠️ **Database**
- MySQL must be accessible from the internet
- Test connection locally first
- For persistent data, use MySQL (not SQLite, as /tmp is ephemeral on Spaces)

⚠️ **Port**
- Always use port 7860 on Hugging Face Spaces
- Flask is configured to use this port automatically

## Support

See **DEPLOYMENT_GUIDE.md** for:
- Detailed troubleshooting
- MySQL setup instructions
- Security best practices
- Advanced configuration options

## Quick Links

- Your Space: `https://huggingface.co/spaces/YOUR_USERNAME/edusync-your-syllabus`
- Hugging Face Docs: https://huggingface.co/docs/hub/spaces
- Docker Docs: https://huggingface.co/docs/hub/spaces-sdks-docker

Good luck with your deployment! 🚀
