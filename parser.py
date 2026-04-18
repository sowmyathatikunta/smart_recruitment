"""
parser.py  –  Extract text from PDF resumes
Tries pypdf (modern) first, falls back to PyPDF2 (legacy).
Install: pip install pypdf
"""

def extract_text(path: str) -> str:
    text = ""

    # ── Try pypdf first (actively maintained, better text extraction) ──
    try:
        from pypdf import PdfReader
        reader = PdfReader(path)
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
        if text.strip():
            return text
    except ImportError:
        pass
    except Exception:
        pass

    # ── Fallback: PyPDF2 ──
    try:
        import PyPDF2
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
    except Exception as e:
        print(f"[parser] PDF read error: {e}")

    return text