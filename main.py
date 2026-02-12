# uvicorn main:app --reload

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,Field
from database import create_table, get_connection
import sqlite3

app = FastAPI(
    title="Student Management API",
    description="A backend API to manage students, marks, and performance analytics.",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    create_table()  # Ensure the database and table are created when the app starts

class student(BaseModel):
    id: int
    name: str
    marks: int = Field(ge=0, le=100)

@app.get("/")
def root():
    return {"message": "Student Management API is running"}

@app.post("/students")
def add_student(student: student):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO students (id, name, marks) VALUES (?, ?, ?)", (student.id, student.name, student.marks))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            raise HTTPException(status_code=400, detail="Student ID already exists")
        conn.close()
        return {"message": "Student added successfully"}


@app.get("/students")
def get_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.get("/students/passed")
def get_passed_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE marks >= 40")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/students/failed")
def get_failed_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE marks < 40")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/students/toppers")
def get_topper():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students ORDER BY marks DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="No students available")
    return dict(row)

@app.get("/students/average")
def get_average():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(marks) FROM students")
    average = cursor.fetchone()[0]
    conn.close()

    if average is None:
        raise HTTPException(status_code=404, detail="No students available")
    return {"average": average}

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found")
    
    conn.close()
    return {"message": "Student deleted"}
                   
@app.get("/students/{student_id}")
def get_student(student_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    if row: 
        return dict(row)
    raise HTTPException(status_code=404, detail="Student not found")  

