"""
matcher.py  –  AI-powered resume ↔ job matching
Uses a two-stage approach:
  1. sentence-transformers (all-MiniLM-L6-v2) for deep semantic similarity
  2. Falls back to TF-IDF cosine similarity if transformers not installed

sentence-transformers is FREE, runs 100% locally, no API key, no rate limits.
Install: pip install sentence-transformers
"""

def calculate_match(resume_text: str, job_desc: str) -> float:
    """Return a match score 0-100 between resume text and job description."""
    resume_text = resume_text.strip()
    job_desc    = job_desc.strip()

    if not resume_text or not job_desc:
        return 0.0

    # ── Stage 1: try sentence-transformers (best quality) ──
    try:
        from sentence_transformers import SentenceTransformer, util

        # Model is cached after first download (~90 MB), fully local after that
        model = SentenceTransformer('all-MiniLM-L6-v2')

        emb_resume = model.encode(resume_text[:512], convert_to_tensor=True)
        emb_job    = model.encode(job_desc[:512],    convert_to_tensor=True)

        cosine = util.cos_sim(emb_resume, emb_job).item()
        # Scale: cosine is 0-1, boost slightly so scores feel natural
        score = round(min(cosine * 110, 100), 2)
        return score

    except ImportError:
        pass

    # ── Stage 2: TF-IDF fallback (always available, no extra install) ──
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    docs   = [resume_text, job_desc]
    tfidf  = TfidfVectorizer(stop_words='english')
    matrix = tfidf.fit_transform(docs)
    score  = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
    return round(score * 100, 2)