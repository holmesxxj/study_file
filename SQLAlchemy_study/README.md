# SQLAlchemy Study

## 1) Install

```bash
pip install sqlalchemy
```

## 2) Use In FastAPI

Add this in `main.py`:

```python
from SQLAlchemy_study.router import sqlalchemy_router
app.include_router(sqlalchemy_router)
```

## 3) API

- `POST /sqlalchemy/students` create student
- `GET /sqlalchemy/students` list students
- `GET /sqlalchemy/students/{student_id}` get one
- `PUT /sqlalchemy/students/{student_id}` update
- `DELETE /sqlalchemy/students/{student_id}` delete

SQLite db file path:

- `SQLAlchemy_study/study.db`
