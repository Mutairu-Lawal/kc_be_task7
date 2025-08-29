from fastapi import APIRouter


router = APIRouter()


@router.post("/add")
def read_root():
    return {"message": "Welcome admin to the Products API"}


@router.post("/checkout")
def get_products():
    return {"products": ["Product 1", "Product 2", "Product 3"]}
