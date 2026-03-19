"""数据库连接与会话管理模块。

这个文件负责：
1. 创建 SQLAlchemy 引擎（Engine）；
2. 创建会话工厂（SessionLocal）；
3. 定义所有 ORM 模型共享的基类 Base；
4. 提供 FastAPI 依赖注入使用的数据库会话生成器 get_db。
"""

from datetime import datetime

from sqlalchemy import DateTime, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

# SQLite 数据库 URL。`./` 以项目根目录为基准。
SQLALCHEMY_DATABASE_URL = "sqlite:///./SQLAlchemy_study/study.db"

# 创建数据库引擎：
# - check_same_thread=False: 允许在不同线程中复用同一连接（FastAPI 常见配置）。
# - echo=True: 打印 SQL 日志，便于学习和调试。
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True,
)

# 会话工厂。每次调用 SessionLocal() 都会创建一个独立 Session。
# autocommit=False: 需要手动 commit。
# autoflush=False: 关闭自动 flush，减少隐式行为。
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """所有 ORM 模型的公共基类。

    这里统一放置每张表都需要的通用字段（创建时间、更新时间），
    子类模型（例如 Student）会自动继承这些列。
    """

    # 声明为抽象基类：只提供公共字段，不直接映射成独立数据表。
    __abstract__ = True

    # 记录数据创建时间，由数据库函数 now() 在插入时自动赋值。
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    # 记录数据最后更新时间：
    # - 首次插入时默认 now()
    # - 每次更新时自动刷新为 now()
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


def get_db():
    """FastAPI 依赖函数：按请求提供数据库会话，并在结束后关闭。"""

    # 为当前请求创建数据库会话。
    db = SessionLocal()
    try:
        # `yield` 会把 db 交给路由函数使用。
        yield db
    finally:
        # 无论请求成功或失败，都确保连接被释放。
        db.close()
