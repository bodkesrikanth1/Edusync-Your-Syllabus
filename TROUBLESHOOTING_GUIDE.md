# 🆘 EdusyncYourSyllabus - Comprehensive Troubleshooting Guide

## Quick Troubleshooting Matrix

| Problem | Symptom | Root Cause | Solution |
|---------|---------|-----------|----------|
| **Database Error** | "Access denied" | Wrong credentials | Check .env DATABASE_URL |
| **YouTube No Results** | Empty video list | API key invalid/quota | Verify YOUTUBE_API_KEY |
| **Slow Processing** | Timeout after 60s | Too many topics searched | Reduce top_k in nlp.py |
| **No Topics Found** | "0 topics extracted" | Bad unit parsing | Check for "UNIT" headers |
| **Wrong Difficulty** | All videos "Intermediate" | Detection failed | Review title patterns |
| **File Upload Fails** | "File too large" | Max size exceeded | Increase MAX_CONTENT_LENGTH |
| **Admin Can't Login** | "Invalid credentials" | Admin not created | Run create_admin.py |
| **Results Page Blank** | No units/videos shown | Query returned empty | Check database has data |

---

## 🔴 Critical Errors & Solutions

### Error 1: "ModuleNotFoundError: No module named 'flask'"

**Problem:** Missing Python dependencies

**Solution:**
```bash
# 1. Check pip installation
pip --version

# 2. Install requirements
pip install -r requirements.txt

# 3. Verify installation
python -c "import flask; print(flask.__version__)"

# 4. If still fails, create fresh virtual environment
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### Error 2: "No Python executable found"

**On Windows:**
```bash
# 1. Check Python installed
python --version

# 2. Add to PATH if missing
# Settings → Environment Variables → PATH → Add C:\Python39

# 3. Or use full path
C:\Python39\python.exe app.py

# 4. Or use virtual environment
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python app.py
```

**On macOS/Linux:**
```bash
# Use python3 instead
python3 --version
python3 -m venv venv
source venv/bin/activate
python3 app.py
```

---

### Error 3: "Error binding to port 5000"

**Symptom:** `Address already in use` or `Port 5000 in use`

**Solution:**

**On Windows:**
```powershell
# 1. Find process using port
netstat -ano | findstr :5000

# 2. Kill process
taskkill /PID <PID> /F

# 3. Or use different port
set FLASK_ENV=development
python app.py --port 8080
```

**On macOS/Linux:**
```bash
# 1. Find process
lsof -i :5000

# 2. Kill process
kill -9 <PID>

# 3. Or use different port
FLASK_PORT=8080 python app.py
```

**In app.py:**
```python
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

---

### Error 4: "MySQL connection failed"

**Symptom:** `Error 2003` or `Access denied for user`

**Solutions:**

**Check MySQL is running:**
```bash
# Windows - Services
# Check "MySQL80" is running

# macOS
brew services list
brew services start mysql

# Linux
sudo systemctl status mysql
sudo systemctl start mysql
```

**Verify credentials:**
```bash
# Test connection manually
mysql -h localhost -u root -p
# Enter password when prompted

# If works → credentials are correct
# If not → reset MySQL password
```

**Reset MySQL password (Windows):**
```bash
# 1. Stop MySQL service
# 2. Start with skip-grant-tables
mysqld --skip-grant-tables

# 3. In new terminal
mysql -u root
# 4. Run commands in MySQL:
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'newpassword';
EXIT;

# 5. Update .env
DATABASE_URL=mysql+pymysql://root:newpassword@localhost/edusync
```

**For cloud databases (PlanetScale):**
```
1. Connection string: Copy from PlanetScale → Connect
2. Format: mysql+pymysql://user:pass@host/db?ssl_verify_cert=true
3. Spaces in pass? URL encode: space=%20, @=%40
4. Test: mysql --ssl-mode=REQUIRED -h host -u user -p db
```

---

### Error 5: "YouTube API Error"

**Error: `"API key not found"` or `"Invalid API key"`**

```bash
# 1. Verify YOUTUBE_API_KEY in .env
echo $YOUTUBE_API_KEY  # macOS/Linux
echo %YOUTUBE_API_KEY%  # Windows PowerShell

# 2. If empty, set it
export YOUTUBE_API_KEY="your_key_here"  # macOS/Linux
set YOUTUBE_API_KEY=your_key_here       # Windows CMD

# 3. Restart Flask app
python app.py

# 4. If still fails, create new API key
# https://console.cloud.google.com
# APIs → YouTube Data API v3
# Credentials → Create → API Key
# Copy to .env
```

**Error: `"Quota exceeded"`**

```
Cause: >10,000 API units used in 24 hours
Solution:
1. Wait 24 hours for quota reset
2. Upgrade to paid plan ($0.00055/unit)
3. Optimize code to use fewer units:
   - Cache results
   - Reduce video results (25 → 10)
   - Search fewer topics

Code optimization:
```python
# Reduce results from 25 to 10
search_params['maxResults'] = 10  # was 25

# Cache results to avoid duplicate searches
@lru_cache(maxsize=100)
def search_and_rank(topic):
    # Cache for 1 hour
    ...
```

**Error: `"Cannot find videos"` (returns empty)**

```python
# Debug: Add logging to youtube_api.py
import logging
logger = logging.getLogger(__name__)

def search_and_rank(topic):
    logger.debug(f"Searching for topic: {topic}")
    
    results = requests.get(search_url, params=search_params)
    logger.debug(f"YouTube returned {len(results)} results")
    
    if not results:
        logger.warning(f"No videos found for: {topic}")
    
    return results

# Check logs to see what's happening
# If 0 results, topic might be too obscure
# Try broader search terms
```

---

## 🟠 Warning Errors (Non-Critical)

### Warning: NLP Extraction Returns Too Few Topics

**Symptom:** Only 2-3 topics extracted instead of 6

**Causes & Fixes:**

```python
# 1. Text too short
# Solution: Minimum 500 characters for good extraction
if len(text) < 500:
    # Use simpler algorithm
    topics = frequency_analysis(text)

# 2. No TF-IDF by default, try frequency
def extract_topics_per_unit(text, top_k=6):
    try:
        vectorizer = TfidfVectorizer(...)
        # ... TF-IDF code ...
    except:
        print(f"TF-IDF failed, using frequency fallback")
        return frequency_fallback(text, top_k)

# 3. Text parsing issue
# Solution: Check for encoding issues
text = text.encode('utf-8', errors='ignore').decode('utf-8')

# 4. Stopwords removing too much
# Solution: Customize stopwords
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
custom_stop = ENGLISH_STOP_WORDS - {'no', 'not', 'and', 'or'}
vectorizer = TfidfVectorizer(stop_words=custom_stop)
```

### Warning: DOCX File Parsing Error

**Symptom:** "Unable to extract text from DOCX" or returns empty

**Solutions:**

```python
# Handle malformed DOCX
from docx import Document

def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        # Extract from paragraphs
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        
        # Also extract from tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if cell.text.strip():
                        paragraphs.append(cell.text)
        
        text = '\n'.join(paragraphs)
        
        if not text:
            print("Warning: DOCX parsed but no text found")
            return None
        
        return text
    
    except Exception as e:
        print(f"Error parsing DOCX: {e}")
        # Fallback: return original binary
        return None

# If DOCX fails, ask user to convert to TXT
# Or upload as PDF and extract text using pdfplumber
```

---

## 🟡 Performance Issues

### Slow Response Times

**Problem:** Page loads take >5 seconds

**Diagnosis:**
```bash
# 1. Check network latency
ping database-host.com

# 2. Check database size
SELECT COUNT(*) FROM videos;
SELECT COUNT(*) FROM topics;

# If millions of rows:
- Add indexes
- Archive old data
- Paginate results
```

**Indexing:**
```sql
-- Add if missing
CREATE INDEX idx_final_score ON videos(final_score DESC);
CREATE INDEX idx_topic_difficulty ON videos(topic_id, difficulty);

-- Check index usage
EXPLAIN SELECT * FROM videos 
WHERE topic_id = 1 
ORDER BY final_score DESC;
-- Should show "Using index"
```

---

### High Memory Usage

**Symptom:** Server uses >500MB RAM

**Causes & Fixes:**

```python
# 1. Large TF-IDF matrices
# Solution: Process in chunks
def extract_topics_chunked(text, chunk_size=1000):
    tokens = tokenize(text)
    chunks = [tokens[i:i+chunk_size] for i in range(0, len(tokens), chunk_size)]
    
    all_topics = []
    for chunk in chunks:
        topics = extract_topics(chunk)
        all_topics.extend(topics)
    
    return all_topics

# 2. YouTube API response caching
# Solution: Don't keep all videos in memory
def process_videos(topic):
    for video in get_videos(topic):  # Generator, not list
        save_to_db(video)
        # Don't store in memory

# 3. Database connection pooling
# Already implemented in db.py with pooling
```

---

## 🟢 Database Issues

### Database Table is Corrupted

**Symptom:** `"Incorrect key file for table"` or `"Table doesn't exist"`

**Solutions:**

```sql
-- Check table status
CHECK TABLE videos;

-- If error, repair
REPAIR TABLE videos;

-- Or recreate from schema
DROP TABLE videos;
-- Run schema.sql to recreate
```

### Running Out of Storage

**Current State:** `~2 GB on PlanetScale free`

**When approaching limit:**
```sql
-- Check size
SELECT SUM(data_length + index_length) / 1024 / 1024 as size_mb
FROM information_schema.tables
WHERE table_schema = 'edusync';

-- Archive old videos (older than 1 year)
DELETE FROM videos 
WHERE published_at < DATE_SUB(CURDATE(), INTERVAL 1 YEAR);

-- Or on PlanetScale: Upgrade to paid tier ($15/mo for 100GB)
```

---

## 🔧 Login & Authentication Issues

### Can't Login - "Invalid Credentials"

**Check user exists:**
```bash
# In MySQL
SELECT * FROM users WHERE email = 'test@example.com';

# If empty, user not registered
# Tell user to register first
```

**Password reset workflow (not implemented yet):**
```python
# Add to app.py
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = db.get_user_by_email(email)
        
        if user:
            # Generate reset token
            token = secrets.token_urlsafe(32)
            # Store in database
            db.save_reset_token(user['id'], token)
            # Send email with reset link
            send_email(email, f"Reset: /reset-password/{token}")
        
        return "Check your email for reset link"
    
    return render_template('forgot_password.html')
```

### Session Keep Timing Out

**Issue:** User logged out after 30 minutes

**Solution:** Increase session timeout in app.py

```python
from datetime import timedelta

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
app.config['SESSION_REFRESH_EACH_REQUEST'] = True

@app.before_request
def make_session_permanent():
    session.permanent = True
```

---

## 🎬 Video Recommendations Issues

### Videos Not Showing

**Checklist:**
```
1. ✓ Topics extracted correctly?
   - Check db: SELECT * FROM topics WHERE unit_id = 1;
   - If 0 topics, NLP extraction failed

2. ✓ YouTube search worked?
   - Check db: SELECT * FROM videos WHERE topic_id = 1;
   - If 0 videos, YouTube API failed

3. ✓ Results page loads?
   - Check /results/<id> URL
   - Check logs for errors

4. ✓ Filter working?
   - Check app.js filter logic
   - Open browser console (F12)
   - Check for JavaScript errors
```

**Debug: Show all videos**
```html
<!-- In results.html, add debug output -->
<script>
console.log("All videos:", window.allVideos);
console.log("Filtered videos:", window.filteredVideos);
</script>
```

### Videos Wrong Format/Broken

**Issue:** Video title contains strange characters

**Cause:** Encoding issue from YouTube API

**Fix:**
```python
def sanitize_video_title(title):
    """Clean video title"""
    # Remove invalid UTF-8
    title = title.encode('utf-8', errors='ignore').decode('utf-8')
    # Remove special chars
    title = ''.join(c for c in title if ord(c) > 31)
    return title

# In insert_video
video['title'] = sanitize_video_title(video['title'])
```

---

## 📱 Frontend Issues

### UI Not Responsive on Mobile

**Check CSS media queries in static/style.css:**

```css
/* Add if missing */
@media (max-width: 768px) {
    body {
        font-size: 14px;
    }
    
    .container {
        padding: 10px;
    }
    
    .grid {
        grid-template-columns: 1fr;
    }
}
```

### JavaScript Errors in Console

**Open browser DevTools:** Press F12

**Common errors & fixes:**

```javascript
// Error: "Uncaught ReferenceError: $ is not defined"
// Solution: jQuery not loaded, add:
// <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

// Error: "Cannot read property 'length' of undefined"
// Solution: Check if array exists before accessing
if (results && results.length > 0) {
    // safe to use
}

// Error: "CORS error"
// Solution: Backend needs CORS headers
from flask_cors import CORS
CORS(app)
```

### Filters Not Working

**Check JavaScript in results.html:**

```javascript
// Debug filter function
function applyFilters() {
    console.log("Filter applied");
    console.log("Duration:", selectedDuration);
    console.log("Difficulty:", selectedDifficulty);
    
    // Check if videos exist
    if (!allVideos || allVideos.length === 0) {
        console.error("No videos loaded");
        return;
    }
    
    // Apply filtering logic
    let filtered = allVideos.filter(v => {
        let match = true;
        
        if (selectedDuration !== 'all') {
            // Check duration ranges
        }
        
        if (selectedDifficulty !== 'all') {
            match = match && v.difficulty === selectedDifficulty;
        }
        
        return match;
    });
    
    console.log("Filtered videos:", filtered.length);
    displayVideos(filtered);
}
```

---

## 🔍 Debugging Tools

### Enable Debug Mode

```python
# app.py
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('app.log', maxBytes=10240000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.DEBUG)
    app.logger.info('EdusyncYourSyllabus startup')
```

### Print Debug Info

```python
# In process() route
def process():
    # ... processing code ...
    
    print("DEBUG INFO:")
    print(f"Units extracted: {len(units)}")
    print(f"Syllabus saved: ID={syllabus_id}")
    
    for unit_id, topics in unit_topics.items():
        print(f"  Unit {unit_id}: {len(topics)} topics")
        for topic, weight in topics[:3]:
            print(f"    - {topic} ({weight:.2f})")
    
    print("Processing complete!")
    
    return redirect(f'/results/{syllabus_id}')
```

### Browser Console (F12)

```javascript
// Check what's loaded
console.log("Flask app location:", window.location.href);
console.log("All videos:", window.allVideos);
console.log("User session:", document.cookie);

// Test filter manually
applyFilters();

// Monitor API calls
fetch('/api/data').then(r => r.json()).then(data => console.log(data));
```

---

## 📞 Support Checklist

When reporting bugs, include:

```
1. Error message (full text)
2. What were you doing?
3. Which browser? (Chrome, Firefox, Safari)
4. Which OS? (Windows, macOS, Linux)
5. Logs (app.log file)
6. Screenshots if visual issue

Example:
"When I upload a DOCX file > 1 MB:
- Browser: Chrome 120 Windows 11
- Error: '413 Request Entity Too Large'
- Expected: File should upload successfully
- Actual: Error message shown"
```

---

🎉 **Still stuck?** Check the full documentation:
- [APPLICATION_DOCUMENTATION.md](APPLICATION_DOCUMENTATION.md) - Full project overview
- [DEVELOPERS_GUIDE.md](DEVELOPERS_GUIDE.md) - Code deep-dive
- [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) - Quick overview

Good luck! 🚀
