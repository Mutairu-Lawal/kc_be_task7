# Student Management API (FastAPI)

A simple FastAPI project for managing students, user authentication, and CRUD operations. Uses SQLite, JWT authentication, and bcrypt password hashing.

## Features

- User registration and login (JWT authentication)
- Student CRUD operations
- Password hashing with bcrypt
- SQLite database
- CORS enabled for frontend integration

## Endpoints

### Auth

- `POST /students/login` — Login and get JWT token
- `POST /students/create-student` — Register a new user

### Students

- `GET /students/` — List all users
- `POST /students/` — Create a new student (requires authentication)

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/Mutairu-Lawal/kc_be_task7.git
   cd kc_be_task7/Task-1
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   uvicorn main:app --reload
   ```

## Usage

- Use `/students/login` to get a JWT token.
- Use the token as `Bearer <token>` for protected endpoints.
- Register users via `/students/create-student`.

## File Structure

- `main.py` — FastAPI app setup
- `lib.py` — Auth, password, and utility functions
- `models.py` — Pydantic models
- `database.py` — DB setup
- `routers/students.py` — Student and user routes
- `users.json` — User data
- `database.db` — SQLite DB
