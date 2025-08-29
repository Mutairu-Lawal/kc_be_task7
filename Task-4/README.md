# Task 4: Notes API

A FastAPI application for managing notes with file and database storage, request counting middleware, and CORS support.

## Features

- Create, list, view, and delete notes
- Middleware to count and log total requests
- Backup notes to notes.json
- CORS for multiple origins

## Usage

- Only `title` and `content` are required when creating a note. `id` and `created_at` are generated automatically.
- All endpoints use the following models:
  - `NoteCreate`: input (title, content)
  - `NoteRead`: output (id, title, content, created_at)

### Endpoints

- `POST /notes/` — create note
- `GET /notes/` — list all notes
- `GET /notes/{id}` — view single note
- `DELETE /notes/{id}` — delete note

### Middleware

- Counts and logs total requests to the API.

### Backup

- All notes are backed up to `notes.json` after creation and deletion.

### CORS

- Allowed origins: `http://localhost:3000`, `http://127.0.0.1:5500`

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   uvicorn main:app --reload
   ```
