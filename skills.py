"""
skills.py  –  Skill extraction and gap analysis
Expanded skills database covering tech, data, cloud, soft skills.
"""

SKILLS_DB = [
    # Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
    "ruby", "php", "swift", "kotlin", "scala", "r", "matlab",
    # Web
    "html", "css", "react", "angular", "vue", "nextjs", "nodejs",
    "express", "django", "flask", "fastapi", "spring",
    # Data / AI
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
    "data analysis", "data science", "statistics", "tableau", "powerbi",
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "sqlite",
    "elasticsearch", "cassandra",
    # Cloud / DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
    "ci/cd", "jenkins", "github actions", "linux", "bash",
    # Tools
    "git", "jira", "agile", "scrum", "rest api", "graphql",
    # Soft skills
    "communication", "leadership", "teamwork", "problem solving",
]

def extract_skills(text: str) -> list:
    text_lower = text.lower()
    return [skill for skill in SKILLS_DB if skill in text_lower]

def missing_skills(resume: str, job: str) -> list:
    job_skills    = set(extract_skills(job))
    resume_skills = set(extract_skills(resume))
    return sorted(list(job_skills - resume_skills))