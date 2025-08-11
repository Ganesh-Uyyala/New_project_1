from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List
import sqlite3, json
import pandas as pd
from fastapi.responses import FileResponse

app = FastAPI()

# Pydantic Model
class StudentModel(BaseModel):
    name: str
    roll_number: str
    marks: dict

# Database Helper Functions
def get_db_connection():
    conn = sqlite3.connect("students.db")
    return conn

def fetch_students_by_name(name_substring: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, roll_number, marks FROM students WHERE name LIKE ?", (f"%{name_substring}%",))
    rows = cursor.fetchall()
    conn.close()
    return [StudentModel(name=row[0], roll_number=row[1], marks=json.loads(row[2])) for row in rows]

def fetch_all_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, roll_number, marks FROM students")
    rows = cursor.fetchall()
    conn.close()
    return [StudentModel(name=row[0], roll_number=row[1], marks=json.loads(row[2])) for row in rows]

def save_student(student: StudentModel):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO students (roll_number, name, marks)
        VALUES (?, ?, ?)
    ''', (student.roll_number, student.name, json.dumps(student.marks)))
    conn.commit()
    conn.close()

# API Endpoints
@app.post("/students/")
def add_student(student: StudentModel):
    save_student(student)
    return {"message": "Student added successfully"}

@app.get("/students/", response_model=List[StudentModel])
def get_all_students():
    return fetch_all_students()

@app.get("/students/search/", response_model=List[StudentModel])
def search_students(name: str = Query(..., description="Substring to search in student names")):
    return fetch_students_by_name(name)

@app.get("/students/export/")
def export_students(format: str = Query("csv", enum=["csv", "excel", "pdf"])):
    students = fetch_all_students()
    df = pd.DataFrame([s.dict() for s in students])
    file_path = f"students_export.{format}"

    if format == "csv":
        df.to_csv(file_path, index=False)
    elif format == "excel":
        df.to_excel(file_path, index=False)
    elif format == "pdf":
        import matplotlib.pyplot as plt
        from pandas.plotting import table
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.axis('off')
        tbl = table(ax, df, loc='center')
        tbl.scale(1, 1.5)
        plt.savefig(file_path, bbox_inches='tight')

    return FileResponse(path=file_path, filename=file_path, media_type="application/octet-stream")
