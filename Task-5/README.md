# Task 5: Contact Manager API

A full Contact Management System using FastAPI, SQLModel, and JWT-based authentication.

## Features

- Contact model: `id`, `name`, `email`, `phone`, `user_id` (foreign key)
- Endpoints:
  - `POST /contacts/` — add new contact (only logged-in user)
  - `GET /contacts/` — list user’s contacts
  - `PUT /contacts/{id}` — update contact
  - `DELETE /contacts/{id}` — delete contact
- Dependency injection for DB
- Security: JWT-based authentication
- Middleware to log IP address of every request
- Enable CORS

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   uvicorn main:app --reload
   ```

## Authentication

- Register a new user:
  ```
  POST /register
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- Login to get JWT token:
  ```
  POST /login
  Form data: username, password
  Response: {"access_token": "...", "token_type": "bearer"}
  ```
- Use the token in the `Authorization` header for all contact endpoints:
  ```
  Authorization: Bearer <access_token>
  ```

## Endpoints

- **Add Contact**
  ```
  POST /contacts/
  {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890"
  }
  ```
- **List Contacts**
  ```
  GET /contacts/
  ```
- **Update Contact**
  ```
  PUT /contacts/{id}
  {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "0987654321"
  }
  ```
- **Delete Contact**
  ```
  DELETE /contacts/{id}
  ```

## Notes

- All contact endpoints require authentication.
- The app logs the IP address of every request.
- CORS is enabled for all origins.
