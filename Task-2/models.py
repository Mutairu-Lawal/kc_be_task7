from sqlmodel import SQLModel, Field
from typing import Optional, Union
from pydantic import BaseModel


# ---------- DB models ----------
class ProductCreate(SQLModel):
    name: str
    price: float
    stock: int


class Product(ProductCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class AddToCartIn(BaseModel):
    product_id: int
    quantity: int


class Token(BaseModel):
    access_token: str
    token_type: str


class Users(BaseModel):
    username: str
    password: str
    role:  str = 'user'  # 'admin' or 'user'
