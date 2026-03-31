import math
import requests
from datetime import datetime, timezone
from dateutil import parser as dtparser

# Lazy imports for sklearn to avoid slow imports in serverless
_tfidf_vectorizer = None
_cosine_similarity = None

def _get_tfidf_vectorizer():
    global _tfidf_vectorizer
    if _tfidf_vectorizer is None:
        from sklearn.feature_extraction.text import TfidfVectorizer
        _tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    return _tfidf_vectorizer

def _get_cosine_similarity():
    global _cosine_similarity
    if _cosine_similarity is None:
        from sklearn.metrics.pairwise import cosine_similarity
        _cosine_similarity = cosine_similarity
    return _cosine_similarity

SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"
CHANNELS_URL = "https://www.googleapis.com/youtube/v3/channels"

def iso8601_to_seconds(duration):
    # Examples: PT5M33S, PT1H02M, PT55S
    hours = minutes = seconds = 0
    num = ''
    duration = duration.replace('P','').replace('T','')
    for ch in duration:
        if ch.isdigit():
            num += ch
        else:
            if ch == 'H': hours = int(num or 0)
            elif ch == 'M': minutes = int(num or 0)
            elif ch == 'S': seconds = int(num or 0)
            num = ''
    return hours*3600 + minutes*60 + seconds

def difficulty_from_title(title, description):
    text = f"{title} {description}".lower()
    if any(k in text for k in ["beginner","intro","introduction","for beginners","101","basics"]):
        return "beginner"
    if any(k in text for k in ["advanced","expert","graduate","research"]):
        return "advanced"
    return "intermediate"

def recency_score(published_at):
    try:
        dt = dtparser.parse(published_at)
        days = (datetime.now(timezone.utc) - dt).days + 1
        # Newer => higher score, simple inverse log
        return 1.0 / math.log10(days + 10)
    except Exception:
        return 0.5

def channel_stats(api_key, channel_id):
    params = {"part": "statistics", "id": channel_id, "key": api_key}
    r = requests.get(CHANNELS_URL, params=params, timeout=15)
    if r.status_code == 200 and r.json().get("items"):
        s = r.json()["items"][0]["statistics"]
        subs = int(s.get("subscriberCount", 0)) if s.get("hiddenSubscriberCount") is False else 0
        return subs
    return 0

def search_and_rank(api_key, query, max_results=12):
    # 1) search
    params = {
        "part": "snippet",
        "type": "video",
        "q": query,
        "maxResults": min(max_results, 25),
        "relevanceLanguage": "en",
        "safeSearch": "moderate",
        "key": api_key
    }
    r = requests.get(SEARCH_URL, params=params, timeout=20)
    r.raise_for_status()
    items = r.json().get("items", [])
    if not items:
        return []

    ids = [it["id"]["videoId"] for it in items]
    # 2) details
    vd = requests.get(VIDEOS_URL, params={
        "part": "snippet,contentDetails,statistics",
        "id": ",".join(ids),
        "key": api_key
    }, timeout=20)
    vd.raise_for_status()
    details = {v["id"]: v for v in vd.json().get("items", [])}

    # Prepare texts for similarity
    docs = []
    metas = []
    for vid in ids:
        d = details.get(vid)
        if not d: 
            continue
        title = d["snippet"]["title"]
        desc = d["snippet"].get("description","")
        docs.append((vid, f"{title}. {desc}"))
        metas.append(d)

    if not docs:
        return []

    # TF-IDF similarity between query and each video text
    corpus = [query] + [doc for _, doc in docs]
    vec = _get_tfidf_vectorizer()
    X = vec.fit_transform(corpus)
    sims = _get_cosine_similarity()(X[0:1], X[1:]).flatten()

    # Compute rating-like score using views + channel subs + recency
    rating = []
    for i, meta in enumerate(metas):
        stats = meta.get("statistics", {})
        views = int(stats.get("viewCount", 0))
        ch_id = meta["snippet"]["channelId"]
        subs = channel_stats(api_key, ch_id)
        rec = recency_score(meta["snippet"].get("publishedAt"))
        score = math.log10(views + 1) + 0.5 * math.log10(subs + 1) + 0.6 * rec
        rating.append(score)

    # Normalize to 0..1
    def norm(arr):
        if not arr: return []
        mn, mx = min(arr), max(arr)
        if mx - mn < 1e-9: 
            return [0.5 for _ in arr]
        return [(x - mn) / (mx - mn) for x in arr]

    sims_n = norm(sims.tolist())
    rating_n = norm(rating)

    ranked = []
    for i, meta in enumerate(metas):
        vid = meta["id"]
        title = meta["snippet"]["title"]
        desc = meta["snippet"].get("description","")
        url = f"https://www.youtube.com/watch?v={vid}"
        duration_iso = meta["contentDetails"]["duration"]
        duration_sec = iso8601_to_seconds(duration_iso)
        views = int(meta.get("statistics", {}).get("viewCount", 0))
        channel_title = meta["snippet"]["channelTitle"]
        channel_id = meta["snippet"]["channelId"]
        difficulty = difficulty_from_title(title, desc)
        published_at = meta["snippet"].get("publishedAt")

        final_score = 0.6*sims_n[i] + 0.3*rating_n[i] + 0.1*(1 if 240 <= duration_sec <= 1200 else 0.5)

        ranked.append({
            "youtube_id": vid,
            "title": title,
            "channel_title": channel_title,
            "channel_id": channel_id,
            "duration_sec": duration_sec,
            "view_count": views,
            "published_at": published_at,
            "rating_score": float(rating_n[i]),
            "similarity": float(sims_n[i]),
            "final_score": float(final_score),
            "difficulty": difficulty,
            "url": url
        })

    ranked.sort(key=lambda x: x["final_score"], reverse=True)
    return ranked
