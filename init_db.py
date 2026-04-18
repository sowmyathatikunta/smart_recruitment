import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS applications;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password TEXT,
    role TEXT
);

CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT
);

CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT,
    job_id INTEGER,
    score REAL
);
""")

# ── Users ──────────────────────────────────────────────────────────────────────
cur.execute("INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)",
    ("Admin", "admin@gmail.com", generate_password_hash("admin123"), "admin"))

cur.execute("INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)",
    ("User", "user@gmail.com", generate_password_hash("user123"), "user"))

# ── 16 Jobs ────────────────────────────────────────────────────────────────────
cur.execute("INSERT INTO jobs (title,description) VALUES (?,?)",
    ("Python Developer",
     "python flask django rest api sql postgresql machine learning data pipelines "
     "backend development object oriented programming pytest git"))

cur.execute("INSERT INTO jobs (title,description) VALUES (?,?)",
    ("Frontend Developer",
     "html css javascript react typescript tailwind css responsive design "
     "web accessibility ui ux figma git webpack vite"))

cur.execute("INSERT INTO jobs (title,description) VALUES (?,?)",
    ("AI / Machine Learning Engineer",
     "artificial intelligence deep learning tensorflow pytorch neural networks nlp "
     "computer vision python scikit-learn model deployment mlops docker"))

cur.execute("INSERT INTO jobs (title,description) VALUES (?,?)",
    ("Full Stack Developer",
     "javascript node.js react mongodb express.js rest api responsive design "
     "python flask html css sql git docker authentication"))

cur.execute("INSERT INTO jobs (title,description) VALUES (?,?)",
    ("Cloud Architect",
     "aws azure google cloud kubernetes docker microservices infrastructure scaling "
     "terraform iam vpc cost optimization reliability security"))

cur.execute("INSERT INTO jobs (title,description) VALUES (?,?)",
    ("DevOps Engineer",
     "ci cd pipeline jenkins kubernetes docker container orchestration monitoring "
     "automation ansible terraform linux bash scripting prometheus grafana"))

cur.execute("INSERT INTO jobs (title,description) VALUES (?,?)",
    ("Data Scientist",
     "python pandas numpy scikit-learn statistical analysis data visualization sql "
     "matplotlib seaborn tableau hypothesis testing machine learning r"))

cur.execute("INSERT INTO jobs (title,description) VALUES (?,?)",
    ("React Native Developer",
     "react native javascript mobile app development ios android swift kotlin "
     "expo redux firebase rest api navigation push notifications"))

cur.execute("INSERT INTO jobs (title,description) VALUES (?,?)",
    ("Cybersecurity Specialist",
     "network security encryption penetration testing firewall vulnerability assessment "
     "compliance siem ethical hacking owasp iso 27001 incident response risk"))

cur.execute("INSERT INTO jobs (title,description) VALUES (?,?)",
    ("Backend Engineer",
     "java spring boot node.js golang distributed systems database design api "
     "development microservices postgresql redis kafka docker git"))

cur.execute("INSERT INTO jobs (title,description) VALUES (?,?)",
    ("UX / UI Designer",
     "figma adobe xd user research wireframing prototyping responsive design "
     "accessibility interaction design visual design css html design systems"))

cur.execute("INSERT INTO jobs (title,description) VALUES (?,?)",
    ("Data Engineer",
     "python sql spark hadoop airflow kafka etl pipelines postgresql mysql "
     "data warehousing aws s3 redshift bigquery dbt data modeling"))

cur.execute("INSERT INTO jobs (title,description) VALUES (?,?)",
    ("Android Developer",
     "android java kotlin jetpack compose xml retrofit room database firebase "
     "mvvm clean architecture git play store material design api integration"))

cur.execute("INSERT INTO jobs (title,description) VALUES (?,?)",
    ("Database Administrator",
     "sql postgresql mysql oracle database design indexing query optimization "
     "backup recovery replication performance tuning stored procedures plsql triggers"))

cur.execute("INSERT INTO jobs (title,description) VALUES (?,?)",
    ("QA / Test Engineer",
     "manual testing automation testing selenium pytest java testng cucumber "
     "api testing postman jira agile regression testing ci cd performance jmeter"))

cur.execute("INSERT INTO jobs (title,description) VALUES (?,?)",
    ("iOS Developer",
     "swift objective c xcode ios swiftui uikit core data alamofire firebase "
     "mvvm rest api app store testing git cocoapods push notifications"))

conn.commit()
conn.close()

print("Database initialized with 16 jobs and 2 users.")