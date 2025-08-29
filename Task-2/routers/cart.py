from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
# from ..database import get_session
from database import get_session
from models import AddToCartIn, Product
import json
import os


router = APIRouter()

# In-memory cart for demonstration (use DB for production)
cart = {}

ORDERS_FILE = os.path.join(os.path.dirname(__file__), '..', 'orders.json')


@router.post("/add")
def add_to_cart(item: AddToCartIn, session: Session = Depends(get_session)):
    product = session.get(Product, item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < item.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
    # Add to cart
    cart_item = cart.get(item.product_id, {
                         "product_id": item.product_id, "name": product.name, "price": product.price, "quantity": 0})
    cart_item["quantity"] += item.quantity
    cart[item.product_id] = cart_item
    return {"message": f"Added {item.quantity} of {product.name} to cart", "cart": list(cart.values())}


@router.post("/checkout")
def checkout(session: Session = Depends(get_session)):
    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")
    order = {
        "items": list(cart.values()),
        "total": sum(item["price"] * item["quantity"] for item in cart.values())
    }
    # Save to orders.json
    try:
        if os.path.exists(ORDERS_FILE):
            with open(ORDERS_FILE, "r") as f:
                orders = json.load(f)
        else:
            orders = []
        orders.append(order)
        with open(ORDERS_FILE, "w") as f:
            json.dump(orders, f, indent=2)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to save order: {str(e)}")
    # Update stock
    for item in cart.values():
        product = session.get(Product, item["product_id"])
        if product:
            product.stock -= item["quantity"]
            session.add(product)
    session.commit()
    cart.clear()
    return {"message": "Checkout successful", "order": order}
