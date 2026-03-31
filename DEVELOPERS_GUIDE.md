# 👨‍💻 EdusyncYourSyllabus - Developer's Guide

## Table of Contents
1. [Development Environment Setup](#development-environment-setup)
2. [Project Architecture](#project-architecture)
3. [Code Modules Deep Dive](#code-modules-deep-dive)
4. [Database Guide](#database-guide)
5. [API Integration Guide](#api-integration-guide)
6. [Testing & Debugging](#testing--debugging)
7. [Contributing Guidelines](#contributing-guidelines)
8. [Common Development Tasks](#common-development-tasks)

---

## 🛠️ Development Environment Setup

### Prerequisites
```bash
✓ Python 3.9 or higher
✓ MySQL 5.7 or higher
✓ Git
✓ Virtual environment package (venv)
✓ pip (Python package manager)
```

### Local Setup Steps

**1. Clone Repository**
```bash
git clone https://github.com/yourusername/edusync-your-syllabus.git
cd "Edusync Your Syllabus"
```

**2. Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Setup Environment Variables**
```bash
# Copy template
cp .env.example .env

# Edit .env with your settings
# DATABASE_URL=mysql+pymysql://user:password@localhost/edusync
# YOUTUBE_API_KEY=your_key_here
```

**5. Initialize Database**
```bash
# Create database
mysql -u root -p
> CREATE DATABASE edusync;
> EXIT;

# Import schema
mysql -u root -p edusync < schema.sql

# Import sample data
mysql -u root -p edusync < edusync.sql
```

**6. Run Application**
```bash
python app.py
# Visit: http://localhost:5000
```

---

## 🏗️ Project Architecture

### Layered Architecture Diagram

```
┌─────────────────────────────────────────┐
│       PRESENTATION LAYER                │
│  ├─ HTML Templates (Jinja2)             │
│  ├─ CSS Styling                         │
│  └─ JavaScript (Vanilla)                │
│         ↑                               │
│         │ HTTP GET/POST                 │
│         ↓                               │
├─────────────────────────────────────────┤
│    APPLICATION LAYER (Flask)            │
│  ├─ Route Handlers (@app.route)         │
│  ├─ Business Logic                      │
│  ├─ Form Validation                     │
│  └─ Session Management                  │
│         ↑                               │
│         │ Function Calls                │
│         ↓                               │
├─────────────────────────────────────────┤
│      SERVICE LAYER                      │
│  ├─ nlp.py (Topic Extraction)           │
│  ├─ youtube_api.py (Video Ranking)      │
│  └─ db.py (Database Operations)         │
│         ↑                               │
│         │ SQL/API Calls                 │
│         ↓                               │
├─────────────────────────────────────────┤
│      DATA LAYER                         │
│  ├─ MySQL Database                      │
│  └─ YouTube Data API v3                 │
└─────────────────────────────────────────┘
```

### Data Flow Example: Processing a Syllabus

```
User uploads syllabus (index.html)
         │
         ↓
POST to /process endpoint (app.py)
         │
         ├─ Extract file/text
         │
         ├─ Parse units (nlp.split_units)
         │
         ├─ Extract topics (nlp.extract_topics_per_unit)
         │
         ├─ Store in database (db.insert_*)
         │
         ├─ For each topic:
         │  ├─ Search YouTube (youtube_api.search_and_rank)
         │  ├─ Score videos (youtube_api ranking algorithm)
         │  └─ Store videos (db.insert_videos)
         │
         └─ Redirect to results page (results.html)
```

---

## 📝 Code Modules Deep Dive

### 1. app.py (Main Application)

**Purpose:** Flask application, route handling, session management

**Key Routes:**

```python
@app.route('/')
def landing():
    """Landing page - no login required"""
    return render_template('landing.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        # Validate input
        # Hash password
        # Create database record
        # Redirect to login
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User authentication"""
    if request.method == 'POST':
        # Verify credentials
        # Create session token
        # Redirect to dashboard
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Student dashboard - requires login"""
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    """Process syllabus - THE MAIN MAGIC ✨"""
    
    # Step 1: Get input (file or text)
    if 'file' in request.files:
        file = request.files['file']
        text = extract_text_from_file(file)
    else:
        text = request.form.get('text')
    
    # Step 2: Parse units
    units = nlp.split_units(text)
    
    # Step 3: Extract topics & save to DB
    syllabus_id = db.insert_syllabus(text, title)
    for unit_no, unit_content in units.items():
        unit_id = db.insert_unit(syllabus_id, unit_no, unit_content)
        topics = nlp.extract_topics_per_unit(unit_content, top_k=6)
        for topic_text, weight in topics:
            topic_id = db.insert_topic(unit_id, topic_text, weight)
            
            # Step 4: Search YouTube
            videos = youtube_api.search_and_rank(topic_text)
            for video in videos:
                db.insert_video(topic_id, video)
    
    return redirect(f'/results/{syllabus_id}')

@app.route('/results/<int:syllabus_id>')
def results(syllabus_id):
    """Display ranked video recommendations"""
    # Fetch from database
    # Apply filters (client-side in JavaScript)
    # Render results.html
    return render_template('results.html', ...)

@app.route('/admin')
def admin_dashboard():
    """Admin panel"""
    if session.get('role') != 'admin':
        return redirect('/')
    users = db.get_all_users()
    return render_template('admin_dashboard.html', users=users)
```

**Key Functions:**

```python
def extract_text_from_file(file):
    """Extract text from uploaded file"""
    if file.filename.endswith('.txt'):
        # Read text file
        text = file.read().decode('utf-8')
    elif file.filename.endswith('.docx'):
        # Extract from Word document
        doc = Document(file)
        text = '\n'.join([para.text for para in doc.paragraphs])
    return text

def hash_password(password):
    """Hash password securely"""
    from werkzeug.security import generate_password_hash
    return generate_password_hash(password, method='pbkdf2')

def verify_password(password, hash):
    """Verify password against hash"""
    from werkzeug.security import check_password_hash
    return check_password_hash(hash, password)
```

---

### 2. nlp.py (NLP Processing)

**Purpose:** Extract topics from syllabus units using TF-IDF

**Algorithm Details:**

```python
from sklearn.feature_extraction.text import TfidfVectorizer
import re

def split_units(text: str) -> dict:
    """
    Parse syllabus into units
    
    Looks for patterns: "UNIT I", "UNIT II", "UNIT 1", etc.
    Falls back to single unit if pattern not found
    
    Args:
        text (str): Full syllabus text
    
    Returns:
        dict: {unit_no: unit_content}
    
    Example:
        >>> text = "UNIT I: Arrays\\nContent...\\nUNIT II: Lists\\nMore..."
        >>> units = split_units(text)
        >>> units == {1: "Arrays\\nContent...", 2: "Lists\\nMore..."}
        True
    """
    # Pattern to match: UNIT I, UNIT 1, UNIT II, UNIT 2, etc.
    pattern = r'UNIT\s+([IVX]+|\d+)\s*[:-]?\s*(.+?)(?=UNIT\s+|$)'
    
    units = {}
    for match in re.finditer(pattern, text, re.IGNORECASE | re.DOTALL):
        unit_num_str = match.group(1)
        unit_content = match.group(2)
        
        # Convert Roman numerals to integers
        unit_num = roman_to_int(unit_num_str)
        units[unit_num] = unit_content.strip()
    
    # Fallback: if no units found, create single unit
    if not units:
        units[1] = text
    
    return units

def extract_topics_per_unit(text: str, top_k: int = 6) -> list:
    """
    Extract key topics from unit text using TF-IDF
    
    Args:
        text (str): Unit content
        top_k (int): Number of top topics to extract
    
    Returns:
        list: [(topic_text, weight), ...] sorted by weight descending
    """
    # Clean text
    text = clean_text(text)
    
    # Tokenize
    tokens = tokenize(text)
    
    if len(tokens) < 3:
        # Not enough content
        return []
    
    # TF-IDF vectorization
    try:
        vectorizer = TfidfVectorizer(
            max_features=100,           # Max 100 features
            min_df=1,                   # Include rare terms
            ngram_range=(1, 2),         # Unigrams + bigrams
            stop_words='english'        # Remove common words
        )
        
        # Fit and transform
        tfidf_matrix = vectorizer.fit_transform([text])
        
        # Get feature names and scores
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]
        
        # Get top K
        top_indices = scores.argsort()[-top_k:][::-1]
        topics = [(feature_names[i], scores[i]) for i in top_indices]
        
        return topics
    
    except Exception as e:
        print(f"TF-IDF failed: {e}, falling back to frequency")
        return frequency_fallback(tokens, top_k)

def clean_text(text: str) -> str:
    """
    Clean text for processing
    
    - Remove special characters (keep hyphens)
    - Normalize whitespace
    - Lowercase
    """
    # Remove special chars except hyphens
    text = re.sub(r'[^\w\s\-]', '', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.lower()

def tokenize(text: str) -> list:
    """
    Tokenize text into meaningful words
    
    - Min 3 characters
    - Must start with letter
    - Preserve hyphenated terms
    """
    pattern = r'\b[a-zA-Z][\w\-]{2,}\b'
    tokens = re.findall(pattern, text, re.IGNORECASE)
    return tokens

def frequency_fallback(tokens: list, top_k: int = 6) -> list:
    """
    Fallback: Extract topics by frequency if TF-IDF fails
    
    Used when text is too short or unusual format
    """
    from collections import Counter
    counter = Counter(tokens)
    return counter.most_common(top_k)

def roman_to_int(roman: str) -> int:
    """Convert Roman numeral to integer"""
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
    total = 0
    for i, char in enumerate(roman.upper()):
        if i + 1 < len(roman) and values[roman[i+1]] > values[char]:
            total -= values[char]
        else:
            total += values[char]
    return total
```

---

### 3. youtube_api.py (Video Ranking)

**Purpose:** Search YouTube, fetch metadata, rank videos

```python
import requests
from datetime import datetime
import math

def search_and_rank(topic: str, num_results: int = 25) -> list:
    """
    Search YouTube for topic and rank results
    
    Args:
        topic (str): Topic to search
        num_results (int): Number of videos to fetch
    
    Returns:
        list: Ranked video objects with scores
    
    Flow:
        1. Search YouTube API
        2. Fetch video details
        3. Fetch channel stats
        4. Calculate scores
        5. Rank by final_score
        6. Return top results
    """
    api_key = os.getenv('YOUTUBE_API_KEY')
    
    # Step 1: Search
    search_url = "https://www.googleapis.com/youtube/v3/search"
    search_params = {
        'q': topic,
        'type': 'video',
        'maxResults': num_results,
        'relevanceLanguage': 'en',
        'safeSearch': 'moderate',
        'key': api_key
    }
    
    try:
        search_response = requests.get(search_url, params=search_params, timeout=10)
        search_response.raise_for_status()
        search_results = search_response.json()
    except Exception as e:
        print(f"YouTube search failed: {e}")
        return []
    
    video_ids = [item['id']['videoId'] for item in search_results.get('items', [])]
    
    if not video_ids:
        return []
    
    # Step 2: Fetch video details
    videos_url = "https://www.googleapis.com/youtube/v3/videos"
    videos_params = {
        'id': ','.join(video_ids),
        'part': 'snippet,contentDetails,statistics',
        'key': api_key
    }
    
    video_response = requests.get(videos_url, params=videos_params)
    video_response.raise_for_status()
    videos_data = video_response.json()
    
    # Step 3: Process and score
    videos = []
    for item in videos_data.get('items', []):
        video = {
            'youtube_id': item['id'],
            'title': item['snippet']['title'],
            'channel_title': item['snippet'].get('channelTitle', 'Unknown'),
            'channel_id': item['snippet'].get('channelId', ''),
            'description': item['snippet'].get('description', ''),
            'published_at': item['snippet'].get('publishedAt', ''),
            'duration_sec': duration_to_seconds(item['contentDetails']['duration']),
            'view_count': int(item['statistics'].get('viewCount', 0)),
            'like_count': int(item['statistics'].get('likeCount', 0)),
            'comment_count': int(item['statistics'].get('commentCount', 0)),
            'url': f"https://www.youtube.com/watch?v={item['id']}"
        }
        
        # Calculate scores
        video['similarity'] = calculate_similarity(topic, video['title'], video['description'])
        video['quality'] = calculate_quality(video['view_count'], video['like_count'], video['comment_count'])
        video['recency'] = calculate_recency(video['published_at'])
        video['difficulty'] = difficulty_from_title(video['title'])
        
        # Get channel stats
        channel_stats = get_channel_stats(video['channel_id'], api_key)
        video['channel_subscribers'] = channel_stats.get('subscriberCount', 0)
        video['channel_score'] = calculate_channel_score(channel_stats)
        
        # Final score: weighted combination
        video['final_score'] = (
            0.40 * video['similarity'] +
            0.30 * video['quality'] +
            0.20 * video['recency'] +
            0.10 * video['channel_score']
        )
        
        videos.append(video)
    
    # Sort by final score
    videos.sort(key=lambda x: x['final_score'], reverse=True)
    
    return videos[:10]  # Return top 10

def calculate_similarity(topic: str, title: str, description: str) -> float:
    """
    Calculate topic-video similarity using TF-IDF cosine similarity
    
    Returns:
        float: Similarity score (0.0 - 1.0)
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    
    # Combine title and description
    video_text = f"{title} {description}"
    
    vectorizer = TfidfVectorizer().fit_transform([topic, video_text])
    similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:2])[0][0]
    
    return float(similarity)

def calculate_quality(views: int, likes: int, comments: int) -> float:
    """
    Calculate video quality score
    
    Factors:
    - View count (logarithmic)
    - Like ratio
    - Comment engagement (bonus)
    
    Returns:
        float: Quality score (0.0 - 1.0)
    """
    # View score (log scale: 1000 views = 0.2, 1M views = 0.8)
    view_score = min(math.log10(max(views, 1)) / 10, 1.0)
    
    # Like ratio score
    total = likes + max(1, comments)  # Avoid division by zero
    like_ratio = likes / total if total > 0 else 0.5
    
    # Combine
    quality = (0.7 * view_score) + (0.3 * like_ratio)
    
    return min(quality, 1.0)

def calculate_recency(published_at: str) -> float:
    """
    Calculate recency score
    
    Recent videos scored higher
    Score decreases with age
    
    Returns:
        float: Recency score (0.0 - 1.0)
    """
    from datetime import datetime
    pub_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
    days_old = (datetime.now(pub_date.tzinfo) - pub_date).days
    
    # Inverse log scale: 1 day old = 1.0, 1000 days = 0.33
    recency = 1.0 / (math.log10(days_old + 10))
    
    return max(min(recency, 1.0), 0.0)

def calculate_channel_score(channel_stats: dict) -> float:
    """
    Calculate channel credibility score
    
    Factors:
    - Subscriber count
    - Total views
    - Video count
    """
    subs = int(channel_stats.get('subscriberCount', 0))
    views = int(channel_stats.get('viewCount', 0))
    videos = int(channel_stats.get('videoCount', 0))
    
    # Log scale scoring
    sub_score = min(math.log10(max(subs, 1)) / 6, 1.0)  # 1M subs = 1.0
    view_score = min(math.log10(max(views, 1)) / 10, 1.0)
    video_score = min(videos / 1000, 1.0)
    
    # Weighted average
    score = (0.5 * sub_score) + (0.3 * view_score) + (0.2 * video_score)
    
    return min(score, 1.0)

def difficulty_from_title(title: str) -> str:
    """
    Detect video difficulty level from title
    
    Returns:
        str: 'beginner', 'intermediate', or 'advanced'
    """
    title_lower = title.lower()
    
    if any(word in title_lower for word in ['beginner', 'intro', 'basics', 'start']):
        return 'beginner'
    elif any(word in title_lower for word in ['advanced', 'expert', 'professional', 'deep']):
        return 'advanced'
    else:
        return 'intermediate'

def duration_to_seconds(iso_duration: str) -> int:
    """
    Convert ISO 8601 duration to seconds
    
    Example: PT12M30S → 750 seconds
    """
    pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
    match = re.match(pattern, iso_duration)
    
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    
    return hours * 3600 + minutes * 60 + seconds
```

---

### 4. db.py (Database Operations)

```python
import mysql.connector
from mysql.connector import pooling
import os

class Database:
    """Database connection pooling and CRUD operations"""
    
    def __init__(self):
        """Initialize connection pool"""
        self.pool = pooling.MySQLConnectionPool(
            pool_name="edusync_pool",
            pool_size=5,
            pool_reset_session=True,
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'edusync')
        )
    
    def execute_query(self, query: str, params: tuple = None):
        """Execute SELECT query"""
        conn = self.pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    def execute_update(self, query: str, params: tuple = None):
        """Execute INSERT/UPDATE/DELETE query"""
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or ())
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
    
    # User operations
    def insert_user(self, full_name: str, email: str, password_hash: str, role: str = 'student', **kwargs):
        """Create new user"""
        query = """
        INSERT INTO users 
        (full_name, email, password_hash, role, college, department, year, enrollment_no, phone)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (full_name, email, password_hash, role,
                  kwargs.get('college'), kwargs.get('department'),
                  kwargs.get('year'), kwargs.get('enrollment_no'),
                  kwargs.get('phone'))
        return self.execute_update(query, params)
    
    def get_user_by_email(self, email: str):
        """Fetch user by email"""
        query = "SELECT * FROM users WHERE email = %s"
        results = self.execute_query(query, (email,))
        return results[0] if results else None
    
    def get_all_users(self):
        """Fetch all users (admin)"""
        query = "SELECT id, full_name, email, role, college, department, year, created_at FROM users ORDER BY created_at DESC"
        return self.execute_query(query)
    
    # Syllabus operations
    def insert_syllabus(self, title: str, text: str):
        """Save syllabus"""
        query = "INSERT INTO syllabi (title, text) VALUES (%s, %s)"
        return self.execute_update(query, (title, text))
    
    def insert_unit(self, syllabus_id: int, unit_no: int, unit_title: str = None):
        """Save unit"""
        query = "INSERT INTO syllabus_units (syllabus_id, unit_no, unit_title) VALUES (%s, %s, %s)"
        return self.execute_update(query, (syllabus_id, unit_no, unit_title))
    
    # Topic operations
    def insert_topic(self, unit_id: int, topic_text: str, weight: float):
        """Save topic"""
        query = "INSERT INTO topics (unit_id, topic_text, weight) VALUES (%s, %s, %s)"
        return self.execute_update(query, (unit_id, topic_text, weight))
    
    # Video operations
    def insert_video(self, topic_id: int, video_data: dict):
        """Save video"""
        query = """
        INSERT INTO videos 
        (topic_id, youtube_id, title, channel_title, duration_sec, 
         view_count, published_at, rating_score, similarity, final_score, difficulty, url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            topic_id,
            video_data.get('youtube_id'),
            video_data.get('title'),
            video_data.get('channel_title'),
            video_data.get('duration_sec'),
            video_data.get('view_count'),
            video_data.get('published_at'),
            video_data.get('quality'),
            video_data.get('similarity'),
            video_data.get('final_score'),
            video_data.get('difficulty'),
            video_data.get('url')
        )
        return self.execute_update(query, params)
    
    def get_results(self, syllabus_id: int):
        """Fetch all units, topics, and videos for a syllabus"""
        query = """
        SELECT u.id, u.unit_no, u.unit_title,
               t.id as topic_id, t.topic_text, t.weight,
               v.id as video_id, v.youtube_id, v.title, v.duration_sec,
               v.view_count, v.difficulty, v.final_score, v.url
        FROM syllabus_units u
        LEFT JOIN topics t ON u.id = t.unit_id
        LEFT JOIN videos v ON t.id = v.topic_id
        WHERE u.syllabus_id = %s
        ORDER BY u.unit_no, t.weight DESC, v.final_score DESC
        """
        return self.execute_query(query, (syllabus_id,))

# Global database instance
db = Database()
```

---

## 🗄️ Database Guide

### Schema Overview

```sql
-- Users table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(512) NOT NULL,
    role VARCHAR(64) DEFAULT 'student',
    college VARCHAR(255),
    department VARCHAR(255),
    year VARCHAR(64),
    enrollment_no VARCHAR(128),
    phone VARCHAR(32),
    preferences TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Syllabi table
CREATE TABLE syllabi (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    text LONGTEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Syllabus units (chapters/sections)
CREATE TABLE syllabus_units (
    id INT PRIMARY KEY AUTO_INCREMENT,
    syllabus_id INT NOT NULL,
    unit_no INT NOT NULL,
    unit_title VARCHAR(255),
    FOREIGN KEY (syllabus_id) REFERENCES syllabi(id) ON DELETE CASCADE
);

-- Topics table (extracted keywords)
CREATE TABLE topics (
    id INT PRIMARY KEY AUTO_INCREMENT,
    unit_id INT NOT NULL,
    topic_text VARCHAR(512) NOT NULL,
    weight FLOAT DEFAULT 0,
    FOREIGN KEY (unit_id) REFERENCES syllabus_units(id) ON DELETE CASCADE
);

-- Videos table (YouTube video recommendations)
CREATE TABLE videos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    topic_id INT NOT NULL,
    youtube_id VARCHAR(128),
    title VARCHAR(512),
    channel_title VARCHAR(255),
    channel_id VARCHAR(128),
    duration_sec INT,
    view_count INT,
    published_at DATETIME,
    rating_score FLOAT,
    similarity FLOAT,
    final_score FLOAT,
    difficulty VARCHAR(32),
    url VARCHAR(512),
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
);
```

### Useful Queries

```sql
-- Get all videos for a topic by relevance
SELECT * FROM videos 
WHERE topic_id = 42 
ORDER BY final_score DESC;

-- Get top topics in a unit
SELECT topic_text, weight FROM topics 
WHERE unit_id = 5 
ORDER BY weight DESC LIMIT 6;

-- Get all recommendations for a syllabus
SELECT 
    su.unit_no, su.unit_title,
    t.topic_text, t.weight,
    v.title, v.final_score, v.difficulty
FROM syllabus_units su
LEFT JOIN topics t ON su.id = t.unit_id
LEFT JOIN videos v ON t.id = v.topic_id
WHERE su.syllabus_id = 42
ORDER BY su.unit_no, t.weight DESC, v.final_score DESC;

-- Find users by role
SELECT * FROM users WHERE role = 'student';

-- Get statistics
SELECT 
    (SELECT COUNT(*) FROM users) as total_users,
    (SELECT COUNT(*) FROM syllabi) as total_syllabi,
    (SELECT COUNT(*) FROM topics) as total_topics,
    (SELECT COUNT(*) FROM videos) as total_videos;
```

---

## 🔌 API Integration Guide

### YouTube API Setup

**1. Create Google Cloud Project**
```
1. Go to https://console.cloud.google.com
2. Create new project
3. Enable "YouTube Data API v3"
4. Create API key (Application default credentials)
5. Add to .env: YOUTUBE_API_KEY=key_here
```

**2. API Rate Limits**
```
Free Tier:
- 10,000 units/day
- Max 25 results per search
- Max 50 videos details at once

Cost:
- No cost for free tier
- $0.00055 per query (paid tier)
```

**3. Making API Calls**

```python
import requests

def call_youtube_api(endpoint, params):
    """Generic YouTube API call with error handling"""
    base_url = "https://www.googleapis.com/youtube/v3"
    url = f"{base_url}/{endpoint}"
    params['key'] = os.getenv('YOUTUBE_API_KEY')
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        # Retry logic
        time.sleep(2)
        return call_youtube_api(endpoint, params)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            # Quota exceeded
            raise Exception("YouTube API quota exceeded")
        elif e.response.status_code == 401:
            # Invalid API key
            raise Exception("Invalid YouTube API key")
        else:
            raise
```

---

## 🧪 Testing & Debugging

### Unit Tests Example

```python
import unittest
from app import app
from nlp import split_units, extract_topics_per_unit

class TestNLPModule(unittest.TestCase):
    
    def test_split_units_basic(self):
        """Test unit parsing"""
        text = "UNIT I: Arrays\\nContent 1\\nUNIT II: Lists\\nContent 2"
        units = split_units(text)
        
        self.assertEqual(len(units), 2)
        self.assertIn("Arrays", units[1])
        self.assertIn("Lists", units[2])
    
    def test_extract_topics(self):
        """Test topic extraction"""
        text = "Arrays are data structures. Arrays store data in sequential format."
        topics = extract_topics_per_unit(text, top_k=3)
        
        self.assertGreater(len(topics), 0)
        # Check if "arrays" is extracted
        topics_text = [t[0] for t in topics]
        self.assertIn("arrays", ' '.join(topics_text).lower())

if __name__ == '__main__':
    unittest.main()
```

### Debugging Tips

```python
# Enable Flask debug mode
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

# Add logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Log important steps
logger.debug(f"Extracted units: {units}")
logger.debug(f"Topics: {topics}")
logger.debug(f"Final score: {score}")

# Test individual functions
if __name__ == '__main__':
    # Test NLP
    from nlp import split_units
    units = split_units("UNIT I: Test\\nContent")
    print("Units:", units)
    
    # Test YouTube API
    from youtube_api import search_and_rank
    videos = search_and_rank("arrays")
    print("Videos found:", len(videos))
    print("Top video:", videos[0] if videos else None)
```

---

## 🤝 Contributing Guidelines

### Code Style

```python
# Use type hints
def process_syllabus(text: str) -> dict:
    """Process syllabus and return results"""
    pass

# Docstrings
def extract_topics(text: str, top_k: int = 6) -> list:
    """
    Extract top K topics from text using TF-IDF.
    
    Args:
        text (str): Input text to process
        top_k (int): Number of topics to extract (default: 6)
    
    Returns:
        list: [(topic_text, weight), ...] sorted by weight
    
    Raises:
        ValueError: If text is empty
    
    Example:
        >>> topics = extract_topics("Machine learning is AI")
        >>> topics[0][0]
        'machine learning'
    """
    pass

# Comments for complex logic
# Calculate cosine similarity between vectors
similarity = 1 - cosine_distance(vec1, vec2)
```

### Branching Strategy

```bash
# Feature branch
git checkout -b feature/add-export-results
# ... make changes ...
git commit -m "Add export results feature"
git push origin feature/add-export-results
# Create pull request

# Bug fix branch
git checkout -b bugfix/fix-nlp-extraction
# ... fix the bug ...
git commit -m "Fix NLP topic extraction for short texts"
git push origin bugfix/fix-nlp-extraction
```

---

## 📋 Common Development Tasks

### Add a New Route

```python
@app.route('/api/topics/<int:unit_id>')
def get_topics(unit_id):
    """Get topics for a specific unit"""
    topics = db.execute_query(
        "SELECT * FROM topics WHERE unit_id = %s ORDER BY weight DESC",
        (unit_id,)
    )
    return jsonify(topics)
```

### Add Database Field

```sql
# In schema.sql or migration
ALTER TABLE videos ADD COLUMN channel_id VARCHAR(128);

# Update db.py insert function
def insert_video(self, topic_id, video_data):
    # Update to include channel_id
    ...
```

### Optimize Slow Query

```python
# Before: N+1 query problem
units = db.get_all_units()
for unit in units:
    topics = db.get_topics(unit['id'])  # Runs for each unit

# After: Single JOIN query
query = """
SELECT u.*, t.* FROM units u
LEFT JOIN topics t ON u.id = t.unit_id
"""
results = db.execute_query(query)
```

---

**Happy Coding! 🎉**

For more info, see [APPLICATION_DOCUMENTATION.md](APPLICATION_DOCUMENTATION.md)
