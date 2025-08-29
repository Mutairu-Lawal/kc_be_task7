from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database import get_session
from models import Product


router = APIRouter()


@router.get("")
def get_products(session: Session = Depends(get_session),
                 offset: int = 0, limit: int = 10):
    products = session.exec(select(Product).offset(offset).limit(limit)).all()
    return products
