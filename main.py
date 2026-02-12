# uvicorn main:app --reload

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,Field

app = FastAPI(
    title="Student Management API",
    description="A backend API to manage students, marks, and performance analytics.",
    version="1.0.0"
)

class student(BaseModel):
    id: int
    name: str
    marks: int = Field(ge=0, le=100)

students = []

@app.get("/")
def root():
    return {"message": "Student Management API is running"}

@app.post("/students")
def add_student(student: student):
    students.append(student)
    return {"message": "Student added", "student": student}
for existing in students:
    if existing.id == student.id:
        raise HTTPException(status_code=400, detail="Student ID already exists")


@app.get("/students")
def get_students():
    return students


@app.get("/students/passed")
def get_passed_students():
    return [student for student in students if student.marks >= 40]

@app.get("/students/failed")
def get_failed_students():
    return[student for student in students if student.marks < 40]

@app.get("/students/toppers")
def get_topper():
    if not students:
        raise HTTPException(status_code=404, detail="No students available")
    topper = max(students, key=lambda s: s.marks)
    return topper

@app.get("/students/average")
def get_average():
    if not students:
        raise HTTPException(status_code=404, detail="No students available")
    total = sum(student.marks for student in students)
    average = total / len(students)
    return {"average": average}

@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student.id == student_id:
            return student
    return {"error": "Student not found"}
