"""Pydantic 数据校验与响应模型模块。

此文件负责定义：
- 创建学生时的请求体结构
- 更新学生时的请求体结构
- 对外返回的学生数据结构
"""

from datetime import datetime

from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    """创建学生请求模型。"""

    # 必填，最短 2 个字符，最长 50 个字符。
    name: str = Field(..., min_length=2, max_length=50)
    # 必填，范围限制在 1~120。
    age: int = Field(..., ge=1, le=120)


class StudentUpdate(BaseModel):
    """更新学生请求模型。

    所有字段都可选，便于实现“部分更新”。
    """

    # 可选姓名；传入时仍然会进行长度校验。
    name: str | None = Field(default=None, min_length=2, max_length=50)
    # 可选年龄；传入时仍然会进行范围校验。
    age: int | None = Field(default=None, ge=1, le=120)


class StudentOut(BaseModel):
    """学生响应模型。

    API 返回给前端的数据结构统一由该模型约束。
    """

    id: int
    name: str
    age: int
    created_at: datetime
    updated_at: datetime

    # 允许直接从 ORM 对象读取字段（Pydantic v2 配置写法）。
    model_config = {"from_attributes": True}
