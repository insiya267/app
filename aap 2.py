import os
import psycopg2
from flask import Flask, render_template, request, redirect, jsonify
 
app = Flask(__name__)
 
DATABASE_URL = os.getenv("DATABASE_URL")
 
def get_connection():
    return psycopg2.connect(DATABASE_URL)
 
 
def create_table():
 
 
    conn = get_connection()
    cur = conn.cursor()
 
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,
        name TEXT,
        age INT,
        course TEXT,
        email TEXT
    )
    """)
 
    conn.commit()
    cur.close()
    conn.close()
 
 
create_table()
 
 
@app.route("/")
def home():
    return render_template("index.html")
 
 
@app.route("/add_student", methods=["POST"])
def add_student():
 
    name = request.form["name"]
    age = request.form["age"]
    course = request.form["course"]
    email = request.form["email"]
 
    conn = get_connection()
    cur = conn.cursor()
 
    cur.execute(
        "INSERT INTO students (name, age, course, email) VALUES (%s,%s,%s,%s)",
        (name, age, course, email),
    )
 
    conn.commit()
    cur.close()
    conn.close()
 
    return redirect("/")
 
 
@app.route("/students")
def view_students():
 
    conn = get_connection()
    cur = conn.cursor()
 
    cur.execute("SELECT * FROM students")
 
    students = cur.fetchall()
 
    cur.close()
    conn.close()
 
    return render_template("students.html", students=students)
 
 
@app.route("/search")
def search_students():
    q = request.args.get("q", "").strip()
 
    conn = get_connection()
    cur = conn.cursor()
 
    cur.execute("SELECT * FROM students WHERE name ILIKE %s LIMIT 50", (f"%{q}%",))
    rows = cur.fetchall()
 
    cur.close()
    conn.close()
 
    students = [
        {"id": r[0], "name": r[1], "age": r[2], "course": r[3], "email": r[4]}
        for r in rows
    ]
 
    return jsonify(students)

@app.route("/search", methods=["GET"])
def search_student():

    name = request.args.get("name")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM students WHERE name ILIKE %s",
        ('%' + name + '%',)
    )

    students = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("students.html", students=students)
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
 