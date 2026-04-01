# Vercel Deployment Debugging Checklist

## Issue: Internal Server Error (500)

Your application is now properly configured to handle errors gracefully. If you still see 500 errors, check these:

### 1. Environment Variables
Ensure all these are set in Vercel Project Settings → Environment Variables:

```
✓ FLASK_SECRET=your-secret-here
✓ DB_HOST=your-db-host
✓ DB_USER=your-db-user
✓ DB_PASSWORD=your-db-password
✓ DB_NAME=edusync
✓ YT_API_KEY=your-youtube-key (optional but needed for /process)
```

### 2. Database Connection
- Verify your database is accessible from the internet (not localhost)
- Test connection from a terminal:
  ```
  mysql -h DB_HOST -u DB_USER -p DB_NAME
  ```
- Make sure all tables are created (run DATABASE_SETUP_GUIDE.md)

### 3. Check Vercel Logs
1. Go to Vercel Project Dashboard
2. Click "Deployments" tab
3. Find your latest deployment
4. Click the "≡" menu and select "View Logs"
5. Look for error messages

### 4. Common Issues

#### Error: "connection refused"
- Database host is wrong or unreachable
- Database is down
- Firewall is blocking connection

#### Error: "unknown database"
- Database name doesn't exist
- SQL tables weren't created

#### Error: Session/Cookie issues
- FLASK_SECRET might be too short or unsafe
- Session storage isn't configured for serverless

#### Error: YouTube API errors
- YT_API_KEY is missing or invalid
- API quota exceeded

### 5. Fixes Applied to Your Code

The following improvements have been made:

✅ Error handlers added (500, 404)
✅ Try-catch blocks around all database operations
✅ Better `load_logged_in_user` error handling
✅ Lazy imports for heavy libraries (sklearn, scipy)
✅ Connection-on-demand database access (serverless-friendly)
✅ Improved error messages

### 6. Testing Locally First

Before redeploying:
```bash
python -c "import app; print('Import successful')"
```

If this fails, you'll see the actual error message.

### 7. Next Steps

1. Set all environment variables in Vercel
2. Verify database connection
3. Redeploy by pushing to git or clicking "Redeploy" in Vercel
4. Check logs after deployment
5. Test the landing page: https://your-domain.vercel.app/

### 8. Still Having Issues?

Enable debug mode temporarily (NOT for production):
```python
# In app.py
app.config['DEBUG'] = True
```

This will show detailed error messages in responses.

---

**Last Updated:** April 1, 2026
