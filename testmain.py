from flask import Flask, request, render_template, redirect, url_for
import secrets
import sqlite3
# Create a db for sign in page and ask about the teachers from the student, create a teacher db, and have the students be able to select them from a drop down list
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route("/login")
def login():
    return render_template("login.html")

def get_db_connection():
    conn = sqlite3.connect('app.db')
    return conn

@app.route('/student', methods=['GET', 'POST'])
def student_view():
    student_id = 1  # You can replace this with session-based login in a real app

    conn = get_db_connection()

    if request.method == 'POST':
        if 'feedback' in request.form:
            feedback = request.form['feedback']
            # Optionally store this somewhere
        elif 'bookmark_job' in request.form:
            job_id = int(request.form['bookmark_job'])
            conn.execute(
                'INSERT INTO bookmarks (student_id, job_id) VALUES (?, ?)',
                (student_id, job_id)
            )
            conn.commit()
        elif 'apply_job' in request.form:
            job_id = int(request.form['apply_job'])
            conn.execute(
                'INSERT INTO applications (student_id, job_id) VALUES (?, ?)',
                (student_id, job_id)
            )
            conn.commit()
        return redirect(url_for('student_view'))

    # Fetch approved jobs
    jobs = conn.execute(
        'SELECT * FROM jobs WHERE approved = 1'
    ).fetchall()

    # Fetch student-specific applications and bookmarks
    applications = conn.execute(
        'SELECT jobs.* FROM jobs JOIN applications ON jobs.id = applications.job_id WHERE applications.student_id = ?',
        (student_id,)
    ).fetchall()

    bookmarked_jobs = conn.execute(
        'SELECT jobs.* FROM jobs JOIN bookmarks ON jobs.id = bookmarks.job_id WHERE bookmarks.student_id = ?',
        (student_id,)
    ).fetchall()

    letters_of_rec = conn.execute(
        'SELECT * FROM letters_of_rec WHERE student_id = ?',
        (student_id,)
    ).fetchall()

    conn.close()

    return render_template(
        'student_view.html',
        jobs=jobs,
        applications=applications,
        bookmarked_jobs=bookmarked_jobs,
        letters_of_rec=letters_of_rec
    )

@app.route('/admin', methods=['GET', 'POST'])
def admin_view():
    conn = get_db_connection()

    if request.method == 'POST':
        job_id = int(request.form['job_id'])
        action = request.form['action']
        
        if action == 'approve':
            conn.execute(
                'UPDATE jobs SET approved = 1 WHERE id = ?',
                (job_id,)
            )
            conn.commit()
    
    # Load pending jobs (approved = 0)
    pending_jobs = conn.execute(
        'SELECT * FROM jobs WHERE approved = 0'
    ).fetchall()

    conn.close()
    print(pending_jobs)
    return render_template('admin.html', pending_jobs=pending_jobs)


@app.route("/employer", methods=['GET', 'POST'])
def employer():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        distance = int(request.form['distance'])

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO jobs (title, company, distance, approved) VALUES (?, ?, ?, ?)',
            (title, company, distance, 0)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("employer"))

    return render_template("employer.html")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")