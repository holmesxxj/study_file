"""FastAPI 路由模块。

提供 students 资源的增删改查（CRUD）接口。
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Student
from .schemas import StudentCreate, StudentOut, StudentUpdate

# 应用启动导入本模块时，自动创建尚不存在的数据表。
Base.metadata.create_all(bind=engine)

# 所有接口统一挂载到 /sqlalchemy 前缀下。
sqlalchemy_router = APIRouter(prefix="/sqlalchemy", tags=["sqlalchemy study"])


@sqlalchemy_router.post("/students", response_model=StudentOut)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    """创建一条学生记录并返回创建结果。"""

    # 将请求体数据映射为 ORM 实例。
    student = Student(name=payload.name, age=payload.age)
    db.add(student)
    # 提交事务，使 INSERT 真正落库。
    db.commit()
    # 刷新实例，拿到数据库回填字段（如 id、时间戳）。
    db.refresh(student)
    return student


@sqlalchemy_router.get("/students", response_model=list[StudentOut])
def list_students(db: Session = Depends(get_db)):
    """查询并返回所有学生，按 ID 升序排列。"""

    students = db.execute(select(Student).order_by(Student.id)).scalars().all()
    return students


@sqlalchemy_router.get("/students/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """按主键查询单个学生，不存在则返回 404。"""

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
    """更新指定学生。

    仅更新请求体中显式传入的字段。
    """

    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="student not found")

    # exclude_unset=True: 只保留客户端实际传入的字段，避免把未传字段覆盖为默认值。
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student


@sqlalchemy_router.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """删除指定学生，不存在则返回 404。"""

    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="student not found")

    db.delete(student)
    db.commit()
    return {"message": "student deleted"}
