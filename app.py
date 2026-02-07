from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Correct DB path for Render
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "hospital.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


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