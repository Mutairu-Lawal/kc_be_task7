# Task 3: Job Application Tracker

A FastAPI project using SQLModel for tracking job applications.

## Features

- JobApplication model: company, position, status, date_applied
- User authentication: users can only access their own applications
- Endpoints:
  - POST /applications/ — add new job application
  - GET /applications/ — list all applications
  - GET /applications/search?status=pending — search by status
- Error handling for invalid queries
- Middleware to reject requests missing User-Agent header

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

## Authentication

- Register a user via `POST /users/register` (username, password required; each user gets a unique id).
- Login via `POST /users/login` to receive a JWT access token.
- Use the token in the `Authorization: Bearer <token>` header for all requests.

## Endpoints

- `POST /applications/` — Add a new job application (fields: company, position, status, date_applied).
- `GET /applications/` — List all job applications for the authenticated user.
- `GET /applications/search?status=<status>` — Search applications by status for the authenticated user.
- `POST /users/register` — Register a new user (unique id assigned).
- `POST /users/login` — Login and get JWT token.

## Error Handling

- Invalid queries return appropriate HTTP error codes and messages.
- Requests missing the `User-Agent` header are rejected by middleware.

## Data

- User data is stored in `users.json`.
- Job applications are stored in `database.db` (SQLite).

## Example Usage

1. Register a user:
   ```bash
   curl -X POST "http://127.0.0.1:8000/users/register" -H "Content-Type: application/json" -H "User-Agent: test" -d '{"username": "demo", "password": "demo123"}'
   ```
2. Login:
   ```bash
   curl -X POST "http://127.0.0.1:8000/users/login" -H "Content-Type: application/x-www-form-urlencoded" -H "User-Agent: test" -d "username=demo&password=demo123"
   ```
3. Add job application (use token from login):
   ```bash
   curl -X POST "http://127.0.0.1:8000/applications/" -H "Authorization: Bearer <token>" -H "User-Agent: test" -H "Content-Type: application/json" -d '{"company": "Acme", "position": "Engineer", "status": "pending", "date_applied": "2025-08-29"}'
   ```
