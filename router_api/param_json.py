from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator

json_param = APIRouter(prefix="/json", tags=["json body param test"])


class Address(BaseModel):
    province: str = Field(..., min_length=2, max_length=20, description="province")
    city: str = Field(..., min_length=2, max_length=20, description="city")


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=20, description="user name")
    age: int = Field(..., ge=0, le=120, description="user age")
    email: str | None = Field(default=None, description="optional email")
    addr: Address

    @field_validator("age")
    @classmethod
    def validate_age(cls, value: int) -> int:  # 因为是类方法，所以是cls不是self
        if value < 18:
            raise ValueError("age must be at least 18")
        if value % 2 != 0:
            raise ValueError("age must be an even number")
        return value


@json_param.post("/user")
def create_user(user: UserCreate):
    return {
        "name": user.name,
        "age": user.age,
        "email": user.email,
        "addr": user.addr,
    }
