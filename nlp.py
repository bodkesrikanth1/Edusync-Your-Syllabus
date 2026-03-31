import re
from typing import List, Dict
import numpy as np

# Lazy import for sklearn to avoid slow imports in serverless
_tfidf_vectorizer = None

def _get_tfidf_vectorizer():
    global _tfidf_vectorizer
    if _tfidf_vectorizer is None:
        from sklearn.feature_extraction.text import TfidfVectorizer
        _tfidf_vectorizer = TfidfVectorizer(
            stop_words='english',
            token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z0-9\-]{2,}\b",
            max_features=1000,
            ngram_range=(1, 2)
        )
    return _tfidf_vectorizer

UNIT_PATTERNS = [
    r'(?:^|\n)\s*(?:UNIT|Unit|Module|MODULE)\s*[-:]?\s*(\w+)\s*(.*)',
    r'(?:^|\n)\s*(?:Unit|UNIT)\s*(\d+)\s*[:.\- ]\s*(.*)'
]

# A tiny custom stopword list; less aggressive than sklearn's full list
# so we don't accidentally wipe out short inputs.
BASIC_STOPS = set("""
the a an of on in for to is are was were be being been and or with by from as this that those these
""".split())

TOKEN_PATTERN = r"(?u)\b[a-zA-Z][a-zA-Z0-9\-]{2,}\b"  # >=3 chars, starts alpha

def _clean_text(text: str) -> str:
    # Normalize spaces and punctuation; keep hyphenated academic terms
    text = re.sub(r'[^\w\s\-:/()]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def split_units(text: str):
    lines = text.strip().splitlines()
    indices = []
    for i, line in enumerate(lines):
        for pat in UNIT_PATTERNS:
            m = re.match(pat, line.strip())
            if m:
                indices.append((i, line.strip()))
                break
    if not indices:
        cleaned = _clean_text(text)
        return [{"unit_no": 1, "unit_title": "Unit 1", "content": cleaned}]
    units = []
    for idx, (i, header) in enumerate(indices):
        start = i + 1
        end = indices[idx+1][0] if idx+1 < len(indices) else len(lines)
        content = "\n".join(lines[start:end]).strip()
        units.append({
            "unit_no": idx+1,
            "unit_title": header,
            "content": _clean_text(content)
        })
    return units

def _fallback_keywords(text: str, k: int) -> List[str]:
    # Very simple keyword fallback: top frequency tokens not in BASIC_STOPS
    tokens = re.findall(TOKEN_PATTERN, text.lower())
    tokens = [t for t in tokens if t not in BASIC_STOPS]
    if not tokens:
        return []
    freq = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    ranked = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    return [w for w, _ in ranked[:k]]

def top_topics(text: str, k: int = 6) -> List[tuple]:
    """
    Robust keyword extractor:
    1) Try TF-IDF with a conservative token pattern and tiny stoplist.
    2) If vectorizer raises "empty vocabulary", use fallback frequency.
    """
    cleaned = _clean_text(text)
    if not cleaned or len(cleaned.split()) < 3:
        # too short, nothing meaningful—return empty and let caller fallback
        return []

    try:
        vec = _get_tfidf_vectorizer()
        X = vec.fit_transform([cleaned])
        if X.shape[1] == 0:
            raise ValueError("empty vocabulary")
        scores = X.toarray()[0]
        terms = np.array(vec.get_feature_names_out())
        order = np.argsort(-scores)
        result = []
        for idx in order:
            term = terms[idx]
            if term in BASIC_STOPS:
                continue
            result.append((term, float(scores[idx])))
            if len(result) >= k:
                break
        if result:
            return result
        # If TF-IDF returned nothing useful, drop to fallback
        fb = _fallback_keywords(cleaned, k)
        return [(t, 1.0) for t in fb]
    except Exception:
        fb = _fallback_keywords(cleaned, k)
        return [(t, 1.0) for t in fb]

def extract_topics_per_unit(syllabus_text: str, topics_per_unit: int = 6) -> List[Dict]:
    units = split_units(syllabus_text)
    out = []
    for u in units:
        tps = top_topics(u["content"], topics_per_unit)
        # Final safety net: if still empty, seed with header words
        if not tps:
            header_terms = _fallback_keywords(u.get("unit_title", "") + " " + u["content"], topics_per_unit)
            tps = [(t, 1.0) for t in (header_terms or ["overview", "introduction"])]
        u["topics"] = [{"text": t, "weight": w} for t, w in tps]
        out.append(u)
    return out
