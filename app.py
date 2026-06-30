<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            category TEXT,
            done INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    all_tasks = c.fetchall()
    conn.close()

    total_tasks = len(all_tasks)
    completed_tasks = sum(1 for task in all_tasks if task[3] == 1)
    progress = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    return render_template(
        "index.html",
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        progress=progress
    )

@app.route("/notes", methods=["GET", "POST"])
def notes():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()

    if request.method == "POST":
        note = request.form.get("note")
        category = request.form.get("category")

        if note:
            note = note[:2000]
            c.execute(
                "INSERT INTO notes (content, category) VALUES (?, ?)",
                (note, category)
            )
            conn.commit()

        return redirect("/notes")

    category_filter = request.args.get("category", "")

    if category_filter:
        c.execute(
            "SELECT * FROM notes WHERE category LIKE ? ORDER BY id DESC",
            (f"%{category_filter}%",)
        )
    else:
        c.execute("SELECT * FROM notes ORDER BY id DESC")

    all_notes = c.fetchall()
    conn.close()

    return render_template("notes.html", notes=all_notes)

@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    if request.method == "POST":
        task = request.form.get("task")
        category = request.form.get("category")

        if task:
            task = task[:100]

        if task:
            conn = sqlite3.connect("tasks.db")
            c = conn.cursor()
            c.execute(
                "INSERT INTO tasks (text, category, done) VALUES (?, ?, ?)",
                (task, category, 0)
            )
            conn.commit()
            conn.close()

        return redirect("/tasks")

    category = request.args.get("category", "All")
    search = request.args.get("search", "")

    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()

    query = "SELECT * FROM tasks"
    params = []
    conditions = []

    if category != "All":
        conditions.append("category = ?")
        params.append(category)

    if search:
        conditions.append("text LIKE ?")
        params.append(f"%{search}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    c.execute(query, params)
    tasks = c.fetchall()
    conn.close()

    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task[3] == 1)
    progress = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    return render_template(
        "tasks.html",
        tasks=tasks,
        selected_category=category,
        search=search,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        progress=progress
    )

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/tasks")

@app.route("/delete_note/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("notes"))

@app.route("/toggle/<int:id>")
def toggle(id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()

    c.execute("SELECT done FROM tasks WHERE id=?", (id,))
    result = c.fetchone()

    if result:
        new_value = 0 if result[0] == 1 else 1
        c.execute("UPDATE tasks SET done=? WHERE id=?", (new_value, id))

    conn.commit()
    conn.close()
    return redirect("/tasks")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()

    if request.method == "POST":
        new_text = request.form.get("task")
        new_category = request.form.get("category")

        c.execute(
            "UPDATE tasks SET text=?, category=? WHERE id=?",
            (new_text, new_category, id)
        )
        conn.commit()
        conn.close()
        return redirect("/tasks")

    c.execute("SELECT * FROM tasks WHERE id=?", (id,))
    task = c.fetchone()
    conn.close()

    return render_template("edit.html", task=task)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
=======
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = "/tmp/tasks.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            category TEXT,
            done INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.before_request
def before_request():
    init_db()

@app.route("/")
def home():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    all_tasks = c.fetchall()
    conn.close()

    total_tasks = len(all_tasks)
    completed_tasks = sum(1 for task in all_tasks if task[3] == 1)
    progress = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    return render_template(
        "index.html",
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        progress=progress
    )

@app.route("/notes", methods=["GET", "POST"])
def notes():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if request.method == "POST":
        note = request.form.get("note")
        category = request.form.get("category")

        if note:
            note = note[:2000]
            c.execute(
                "INSERT INTO notes (content, category) VALUES (?, ?)",
                (note, category)
            )
            conn.commit()

        return redirect("/notes")

    category_filter = request.args.get("category", "")

    if category_filter:
        c.execute(
            "SELECT * FROM notes WHERE category LIKE ? ORDER BY id DESC",
            (f"%{category_filter}%",)
        )
    else:
        c.execute("SELECT * FROM notes ORDER BY id DESC")

    all_notes = c.fetchall()
    conn.close()

    return render_template("notes.html", notes=all_notes)

@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    if request.method == "POST":
        task = request.form.get("task")
        category = request.form.get("category")

        if task:
            task = task[:100]

        if task:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute(
                "INSERT INTO tasks (text, category, done) VALUES (?, ?, ?)",
                (task, category, 0)
            )
            conn.commit()
            conn.close()

        return redirect("/tasks")

    category = request.args.get("category", "All")
    search = request.args.get("search", "")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    query = "SELECT * FROM tasks"
    params = []
    conditions = []

    if category != "All":
        conditions.append("category = ?")
        params.append(category)

    if search:
        conditions.append("text LIKE ?")
        params.append(f"%{search}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    c.execute(query, params)
    tasks = c.fetchall()
    conn.close()

    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task[3] == 1)
    progress = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    return render_template(
        "tasks.html",
        tasks=tasks,
        selected_category=category,
        search=search,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        progress=progress
    )

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/tasks")

@app.route("/delete_note/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("notes"))

@app.route("/toggle/<int:id>")
def toggle(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT done FROM tasks WHERE id=?", (id,))
    result = c.fetchone()

    if result:
        new_value = 0 if result[0] == 1 else 1
        c.execute("UPDATE tasks SET done=? WHERE id=?", (new_value, id))

    conn.commit()
    conn.close()
    return redirect("/tasks")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if request.method == "POST":
        new_text = request.form.get("task")
        new_category = request.form.get("category")

        c.execute(
            "UPDATE tasks SET text=?, category=? WHERE id=?",
            (new_text, new_category, id)
        )
        conn.commit()
        conn.close()
        return redirect("/tasks")

    c.execute("SELECT * FROM tasks WHERE id=?", (id,))
    task = c.fetchone()
    conn.close()

    return render_template("edit.html", task=task)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
>>>>>>> 8b7d7c2470e19022eb526f21f19a9372de343f40
