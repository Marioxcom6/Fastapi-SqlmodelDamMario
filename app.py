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

@app.get("/students/age/min/{min_age}")
def students_min_age(min_age: int, session: Session = Depends(get_session)):
    statement = select(Student).where(Student.age >= min_age)
    return session.exec(statement).all()


@app.get("/students/age/max/{max_age}")
def students_max_age(max_age: int, session: Session = Depends(get_session)):
    statement = select(Student).where(Student.age <= max_age)
    return session.exec(statement).all()


@app.get("/students/name/{substring}")
def students_name_contains(substring: str, session: Session = Depends(get_session)):
    statement = select(Student).where(Student.name.contains(substring))
    return session.exec(statement).all()


@app.get("/students/count")
def student_count(session: Session = Depends(get_session)):
    total = session.exec(select(Student)).all()
    return {"total_students": len(total)}


@app.get("/students/age/average")
def average_age(session: Session = Depends(get_session)):
    students = session.exec(select(Student)).all()
    if not students:
        return {"average_age": 0}
    avg = sum(s.age for s in students) / len(students)
    return {"average_age": round(avg, 2)}