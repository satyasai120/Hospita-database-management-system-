from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# DB path (works on Render)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "hospital.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ✅ CREATE TABLES AUTOMATICALLY
def init_db():
    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS doctors(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        specialization TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS appointments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


# run once at startup
init_db()


@app.route("/")
def home():
    conn = get_db()
    data = conn.execute("""
        SELECT a.id, p.name as patient, d.name as doctor, a.date
        FROM appointments a
        JOIN patients p ON p.id = a.patient_id
        JOIN doctors d ON d.id = a.doctor_id
    """).fetchall()
    return render_template("index.html", data=data)


@app.route("/add_doctor", methods=["POST"])
def add_doctor():
    name = request.form["name"]
    spec = request.form["spec"]

    conn = get_db()
    conn.execute(
        "INSERT INTO doctors(name, specialization) VALUES (?, ?)",
        (name, spec)
    )
    conn.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)