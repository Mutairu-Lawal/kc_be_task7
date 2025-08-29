# E-Commerce API (Task-2)

This FastAPI project provides a simple e-commerce backend with product management, cart operations, and order backup.

## Features

- Add products
- Add items to cart
- Checkout cart
- Orders are saved to `orders.json` for backup
- Product stock management
- Middleware to measure response time (header: `X-Process-Time`)

## Endpoints

### Cart

- `POST /cart/add` — Add product to cart
  - Request body: `{ "product_id": int, "quantity": int }`
- `POST /cart/checkout` — Checkout cart and save order

### Products

- Product endpoints are available for CRUD operations (see `routers/products.py`)

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
3. API docs available at `/docs`

## Data Files

- `database.db` — SQLite database
- `orders.json` — Orders backup
- `users.json` — User data

## Notes

- Cart is stored in-memory (for demo purposes)
- Orders are appended to `orders.json` on checkout
- Product stock is updated on checkout

## Project Structure

```
Task-2/
  main.py
  models.py
  database.py
  lib.py
  routers/
    products.py
    cart.py
    users.py
    admin.py
  orders.json
  users.json
  requirements.txt
```

## Author

Mutairu-Lawal
