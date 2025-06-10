from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from database import lifespan, get_session
from models import Student

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Student and Course Management API",
        "endpoints": {"/students", "/courses", "/enrollaments"}
    }

@app.post("/students/", response_model=Student)
def create_students(student: Student, session: Session = Depends(get_session)):
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

@app.get("/students/", response_model=List[Student])
def get_students(student_id: int, session: Session = Depends(get_session)):
    return session.exec(select(Student)).all()

@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int, session: Session = Depends((get_session))):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Dtudent not found")
    return student

@app.put("students/{student_id}", response_model=Student)
def update_student(student_id: int, updated: Student, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.name = updated.name
    student.age = updated.age
    session.commit()
    session.refresh(student)
    return student

@app.delete("/students/{student_id}")
def delete(student_id: int, session: Session = Depends(get_session())):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    session.delete(student)
    session.commit()
    return {"ok": True}

@app.get("/students/count")
def count_students(session: Session = Depends(get_session)):
    statement = select(Student)
    total = len(session.exec(statement).all())
    return {"total_students": total}