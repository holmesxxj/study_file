from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Student
from .schemas import StudentCreate, StudentOut, StudentUpdate

Base.metadata.create_all(bind=engine)

sqlalchemy_router = APIRouter(prefix="/sqlalchemy", tags=["sqlalchemy study"])


@sqlalchemy_router.post("/students", response_model=StudentOut)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    student = Student(name=payload.name, age=payload.age)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@sqlalchemy_router.get("/students", response_model=list[StudentOut])
def list_students(db: Session = Depends(get_db)):
    students = db.execute(select(Student).order_by(Student.id)).scalars().all()
    return students


@sqlalchemy_router.get("/students/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="student not found")
    return student


@sqlalchemy_router.put("/students/{student_id}", response_model=StudentOut)
def update_student(
    student_id: int,
    payload: StudentUpdate,
    db: Session = Depends(get_db),
):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="student not found")

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student


@sqlalchemy_router.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="student not found")

    db.delete(student)
    db.commit()
    return {"message": "student deleted"}
