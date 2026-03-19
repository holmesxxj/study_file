"""ORM 模型定义模块。

此文件使用 SQLAlchemy 2.0 的声明式写法定义数据表结构。
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Student(Base):
    """学生表模型。

    继承 Base 后会自动拥有：
    - created_at
    - updated_at
    """

    # 对应数据库中的表名。
    __tablename__ = "students"

    # 主键 ID，建立索引便于按主键查询。
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # 姓名：长度限制 50，不能为空，同时建立普通索引便于按姓名检索。
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    # 年龄：整数类型，不能为空。
    age: Mapped[int] = mapped_column(nullable=False)
