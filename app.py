from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO
import sqlite3, os, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from models.matcher import calculate_match
from models.parser import extract_text
from models.skills import missing_skills

app = Flask(__name__)
app.secret_key = "hireai_secret_2024"

socketio = SocketIO(app, cors_allowed_origins="*")

# ── Use absolute paths so Windows slashes never break ──
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads", "resumes")
CHART_FOLDER  = os.path.join(BASE_DIR, "static", "charts")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CHART_FOLDER,  exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    conn = sqlite3.connect(os.path.join(BASE_DIR, "database.db"))
    conn.row_factory = sqlite3.Row
    return conn

@app.context_processor
def inject_user():
    return {
        "current_user": session.get("user"),
        "current_name": session.get("name"),
        "current_role": session.get("role"),
    }

# ───────────────────── ROUTES ─────────────────────

@app.route('/')
def home():
    if 'user' in session:
        return redirect('/admin' if session.get('role') == 'admin' else '/dashboard')
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' in session:
        return redirect('/dashboard')
    error = None
    if request.method == 'POST':
        name     = request.form.get('name', '').strip()
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        if not name or not email or not password:
            error = "All fields are required."
        else:
            try:
                db = get_db()
                db.execute(
                    "INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)",
                    (name, email, generate_password_hash(password), "user")
                )
                db.commit()
                return redirect('/login')
            except sqlite3.IntegrityError:
                error = "An account with that email already exists."
    return render_template('register.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect('/admin' if session.get('role') == 'admin' else '/dashboard')
    error = None
    if request.method == 'POST':
        db   = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE email=?",
            (request.form.get('email', '').strip(),)
        ).fetchone()
        if user and check_password_hash(user['password'], request.form.get('password', '')):
            session['user'] = user['email']
            session['name'] = user['name']
            session['role'] = user['role']
            return redirect('/admin' if user['role'] == "admin" else '/dashboard')
        else:
            error = "Invalid email or password. Please try again."
    return render_template('login.html', error=error)


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    db   = get_db()
    jobs = db.execute("SELECT * FROM jobs").fetchall()
    return render_template('dashboard.html', jobs=jobs)


@app.route('/upload/<int:job_id>', methods=['GET', 'POST'])
def upload(job_id):
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        file = request.files.get('resume')
        if not file or file.filename == "":
            return render_template('upload.html', error="No file selected.", job_id=job_id)
        if not allowed_file(file.filename):
            return render_template('upload.html', error="Only PDF files are allowed.", job_id=job_id)

        filename = secure_filename(file.filename)
        path     = os.path.join(app.config["UPLOAD_FOLDER"], filename)  # correct on Windows too
        file.save(path)

        resume_text = extract_text(path)
        if not resume_text.strip():
            return render_template('upload.html', error="Could not read text from PDF.", job_id=job_id)

        db  = get_db()
        job = db.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
        if not job:
            return render_template('upload.html', error="Job not found.", job_id=job_id)

        score   = calculate_match(resume_text, job['description'])
        missing = missing_skills(resume_text, job['description'])

        db.execute(
            "INSERT INTO applications (user_email,job_id,score) VALUES (?,?,?)",
            (session['user'], job_id, score)
        )
        db.commit()
        socketio.emit('match_result', {'score': score, 'message': f'Match Score: {score}%'})

        return render_template('results.html', score=score, missing=missing, job=job)

    return render_template('upload.html', job_id=job_id)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session.get('role') != 'admin':
        return redirect('/login')
    db    = get_db()
    error = None
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        desc  = request.form.get('description', '').strip()
        if not title or not desc:
            error = "Both title and description are required."
        else:
            db.execute("INSERT INTO jobs (title,description) VALUES (?,?)", (title, desc))
            db.commit()
            socketio.emit('new_job', {'message': f'New Job Posted: {title}'})
    jobs = db.execute("SELECT * FROM jobs").fetchall()
    return render_template('admin.html', jobs=jobs, error=error)


@app.route('/admin/delete/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    if session.get('role') != 'admin':
        return redirect('/login')
    get_db().execute("DELETE FROM jobs WHERE id=?", (job_id,))
    get_db().commit()
    return redirect('/admin')


@app.route('/analytics')
def analytics():
    if session.get('role') != 'admin':
        return redirect('/login')
    db     = get_db()
    data   = db.execute("SELECT score FROM applications").fetchall()
    scores = [d['score'] for d in data]

    if scores:
        plt.figure(figsize=(8, 4), facecolor='#161b2e')
        ax = plt.gca()
        ax.set_facecolor('#0a0c12')
        ax.hist(scores, bins=10, color='#6366f1', edgecolor='#818cf8', linewidth=0.8)
        ax.set_title("Match Score Distribution", color='#e8eaf6', fontsize=13, pad=12)
        ax.set_xlabel("Score (%)", color='#8b93b8')
        ax.set_ylabel("Applicants",  color='#8b93b8')
        ax.tick_params(colors='#8b93b8')
        for spine in ax.spines.values():
            spine.set_edgecolor('#2a2f4e')
        plt.tight_layout()
        plt.savefig(os.path.join(CHART_FOLDER, "chart.png"), facecolor='#161b2e')
        plt.close()

    total_apps  = db.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
    total_jobs  = db.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
    total_users = db.execute("SELECT COUNT(*) FROM users WHERE role='user'").fetchone()[0]
    avg_score_r = db.execute("SELECT AVG(score) FROM applications").fetchone()[0]
    avg_score   = round(avg_score_r, 1) if avg_score_r else 0

    return render_template('analytics.html',
        total_apps=total_apps, total_jobs=total_jobs,
        total_users=total_users, avg_score=avg_score
    )


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    socketio.run(app, debug=True)