from fastapi import APIRouter
from models import ProductCreate, Product
from lib import get_current_user
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from database import get_session

router = APIRouter()


@router.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, user=Depends(get_current_user), session: Session = Depends(get_session)):
    post_data = data.model_dump()

    if user['role'] != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    product = Product(**post_data)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product
