import mysql.connector
from mysql.connector import pooling
from config import Config
import mysql.connector
from mysql.connector import pooling
from config import Config
from dateutil import parser as dtparser, tz  # <- add this import
import json
pool = pooling.MySQLConnectionPool(
    pool_name="edusync_pool",
    pool_size=10,   # increase pool size if you expect more parallel requests
    pool_reset_session=True,
    host=Config.DB_HOST,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    database=Config.DB_NAME,
    charset="utf8mb4",
    collation="utf8mb4_unicode_ci"
)

def get_conn():
    return pool.get_connection()

def insert_syllabus(title, text):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO syllabi (title, text) VALUES (%s, %s)", (title, text))
        conn.commit()
        return cur.lastrowid
    finally:
        cur.close()
        conn.close()

def insert_unit(syllabus_id, unit_no, unit_title=None):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""INSERT INTO syllabus_units (syllabus_id, unit_no, unit_title)
                       VALUES (%s, %s, %s)""", (syllabus_id, unit_no, unit_title))
        conn.commit()
        return cur.lastrowid
    finally:
        cur.close()
        conn.close()

def insert_topic(unit_id, topic_text, weight):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""INSERT INTO topics (unit_id, topic_text, weight)
                       VALUES (%s, %s, %s)""", (unit_id, topic_text, float(weight)))
        conn.commit()
        return cur.lastrowid
    finally:
        cur.close()
        conn.close()

def _to_mysql_datetime(iso_str):
    """Convert ISO-8601 (with or without Z/offset) to naive UTC datetime for MySQL DATETIME."""
    if not iso_str:
        return None
    try:
        dt = dtparser.isoparse(iso_str)  # handles Z or +00:00 etc.
    except Exception:
        dt = dtparser.parse(iso_str)
    # convert to UTC, drop tzinfo (MySQL DATETIME has no tz)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tz.UTC)
    dt_utc = dt.astimezone(tz.UTC).replace(tzinfo=None)
    return dt_utc  # mysql-connector accepts datetime objects directly

def insert_video(topic_id, v):
    conn = get_conn()
    try:
        cur = conn.cursor()
        pub_dt = _to_mysql_datetime(v.get("published_at"))  # <- normalize here
        cur.execute("""INSERT INTO videos
            (topic_id, youtube_id, title, channel_title, channel_id,
             duration_sec, view_count, published_at, rating_score,
             similarity, final_score, difficulty, url)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (topic_id, v["youtube_id"], v["title"], v.get("channel_title"),
             v.get("channel_id"), v.get("duration_sec", 0), v.get("view_count", 0),
             pub_dt,  # <- pass datetime, not the ISO string
             v.get("rating_score", 0.0), v.get("similarity", 0.0),
             v.get("final_score", 0.0), v.get("difficulty", "auto"), v["url"]))
        conn.commit()
        return cur.lastrowid
    finally:
        cur.close()
        conn.close()

def fetch_units_topics_videos(syllabus_id, filters=None):
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""SELECT id, unit_no, unit_title FROM syllabus_units
                       WHERE syllabus_id=%s ORDER BY unit_no ASC""", (syllabus_id,))
        units = cur.fetchall()
        for u in units:
            cur.execute("""SELECT id, topic_text, weight FROM topics
                           WHERE unit_id=%s ORDER BY weight DESC""", (u["id"],))
            topics = cur.fetchall()
            u["topics"] = topics
            for t in topics:
                query = """SELECT * FROM videos WHERE topic_id=%s"""
                clauses, params = [], [t["id"]]
                if filters:
                    if filters.get("duration") in ("short","medium","long"):
                        if filters["duration"] == "short":
                            clauses.append("duration_sec < 240")
                        elif filters["duration"] == "medium":
                            clauses.append("duration_sec BETWEEN 240 AND 1200")
                        else:
                            clauses.append("duration_sec > 1200")
                    if filters.get("difficulty") and filters["difficulty"] != "all":
                        clauses.append("difficulty=%s")
                        params.append(filters["difficulty"])
                    if filters.get("min_rating") is not None:
                        clauses.append("rating_score >= %s")
                        params.append(float(filters["min_rating"]))
                if clauses:
                    query += " AND " + " AND ".join(clauses)
                query += " ORDER BY final_score DESC LIMIT 12"
                cur2 = conn.cursor(dictionary=True)
                cur2.execute(query, params)
                vids = cur2.fetchall()
                cur2.close()
                t["videos"] = vids
        cur.close()
        return units
    finally:
        conn.close()

# ---------------- User authentication helper functions ----------------


def create_user(full_name: str, email: str, password_hash: str,
                role: str = "student", college: str = None,
                department: str = None, year: str = None,
                enrollment_no: str = None, phone: str = None,
                preferences: dict = None) -> int:
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users
            (full_name, email, password_hash, role, college, department, year, enrollment_no, phone, preferences)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (full_name, email, password_hash, role, college, department, year, enrollment_no, phone,
              None if preferences is None else json.dumps(preferences)))
        conn.commit()
        return cur.lastrowid
    finally:
        cur.close()
        conn.close()

def get_user_by_email(email: str):
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()

def get_user_by_id(uid: int):
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE id=%s", (uid,))
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()

def get_all_users():
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT id, full_name, email, role, college, department, year, enrollment_no, phone, created_at
            FROM users
            ORDER BY created_at DESC
        """)
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()
