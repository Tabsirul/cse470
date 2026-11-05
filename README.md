# StudyBuddy

StudyBuddy is a collaborative study platform built with React, FastAPI, and PostgreSQL.

## Requirements

- Python 3
- Node.js and npm
- PostgreSQL
- Git

## 1. Clone the repository

```bash
git clone https://github.com/Tabsirul/cse470.git
cd cse470
```

## 2. Set up the PostgreSQL database

Open PostgreSQL and run:

```sql
CREATE USER studybuddy_user WITH PASSWORD 'YOUR_PASSWORD';
CREATE DATABASE studybuddy OWNER studybuddy_user;
```

## 3. Set up the backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create your local environment file:

```bash
cp .env.example .env
```

Update `backend/.env` with your PostgreSQL password.
Also replace SECRET_KEY with your own random text. Make one with: python3 -c "import secrets; print(secrets.token_hex(32))"

Run database migrations:

```bash
alembic upgrade head
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

Backend: http://127.0.0.1:8000

API documentation: http://127.0.0.1:8000/docs

## 4. Set up the frontend

Open another Terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

## 5. Verify the setup

Visit http://127.0.0.1:8000/api/health

Expected response:

```json
{
  "status": "ok",
  "database": "connected"
}
```

Open http://localhost:5173 to check the frontend.

## Important

- Never commit `.env`, `venv/`, or `node_modules/`.
- Each teammate must create their own local `.env` file.
- Run the backend and frontend in separate Terminal windows.

