from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel


class ProductBase(SQLModel):
    name: str
    price: float


class Product(ProductBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None


class UserBase(SQLModel):
    email: EmailStr
    username: str
    full_name: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str


class UserRegister(UserBase):
    password: str


class UserPublic(UserBase):
    id: int


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None
