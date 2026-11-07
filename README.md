# StudyBuddy: Campus Peer Tutoring

StudyBuddy is a web-based peer tutoring platform designed to connect university students with experienced student tutors. It allows students to find suitable tutors, arrange learning sessions, make payments through a sandbox payment system, and share feedback after completed sessions.

The project is developed as part of the CSE470 (Software Engineering) course by Group 4 at BRAC University.

Built with React, FastAPI and PostgreSQL, following the MVC architecture.

## Technology Stack

- **Frontend:** React, JavaScript, HTML and CSS
- **Backend:** Python, FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Database Migrations:** Alembic

## Main Capabilities

- User registration, authentication and role-based access.
- Student and tutor profile management.
- Tutor search, filtering and matching.
- Academic prerequisite and course verification.
- Session scheduling, booking and cancellation.
- Sandbox payment processing with escrow-style payment handling.
- Session completion and payment release.
- Student reviews and tutor ratings.
- Administrative management of academic verification.

Payments are simulated through a sandbox system. No real money is transferred.

## Project Structure

```text
cse470/
├── backend/
│   ├── app/
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── alembic/
│   ├── tests/
│   ├── seed.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── views/
│   │   ├── App.jsx
│   │   └── index.css
│   └── package.json
│
└── README.md
```

## Requirements

- Python 3
- Node.js and npm
- PostgreSQL
- Git

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Tabsirul/cse470.git
cd cse470
```

### 2. Set up the PostgreSQL database

Open PostgreSQL and run:

```sql
CREATE USER studybuddy_user WITH PASSWORD 'YOUR_PASSWORD';
CREATE DATABASE studybuddy OWNER studybuddy_user;
```

If the database user and database already exist, use your existing credentials.

### 3. Set up the backend

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

Update `backend/.env` with your PostgreSQL connection string:

```env
DATABASE_URL=postgresql+psycopg2://studybuddy_user:YOUR_PASSWORD@localhost:5432/studybuddy
SECRET_KEY=YOUR_SECRET_KEY
```

Generate a secure secret key:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Run database migrations

From the `backend` directory:

```bash
alembic upgrade head
```

### 5. Add initial database data

StudyBuddy includes a seed script to insert starter course information and prerequisite grade rules.

Run the following command from the `backend` directory:

```bash
python seed.py
```

This inserts the available starter courses and grade rules into the database.

To create sample accounts for local development and testing, run:

```bash
python seed.py --demo
```

The demo accounts are:

| Role | Email | Password |
|---|---|---|
| Admin | admin@example.com | password123 |
| Tutor | tutor@example.com | password123 |
| Student | student@example.com | password123 |

The demo setup also creates a tutor profile and an approved tutor-course record.

**Note:** Demo accounts use a shared test password. They are intended for local development only, not production use. The seed script avoids creating duplicate records when run repeatedly.

### 6. Start the backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

Backend: http://127.0.0.1:8000

API documentation: http://127.0.0.1:8000/docs

### 7. Set up and start the frontend

Open another Terminal window:

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

## Verify the Setup

Visit:

http://127.0.0.1:8000/api/health

Expected response:

```json
{
  "status": "ok",
  "database": "connected"
}
```

Open http://localhost:5173 to check the frontend.

## Run the Tests

From the `backend` directory, with the virtual environment active:

```bash
python -m pytest -q
```

## User Roles

- **Student:** Search for tutors, book sessions, make payments and submit reviews.
- **Tutor:** Manage profiles, apply for courses, offer sessions and view earnings and reviews.
- **Admin:** Manage academic grade rules and review tutor course-verification claims.

To make an existing user an admin, run the following SQL command in PostgreSQL:

```sql
UPDATE users
SET role = 'admin'
WHERE email = 'your@email.com';
```

## Team

**CSE470 Software Engineering – Group 4**

BRAC University

- Tabsirul Haque Nadim
- Md. Mashrur Ryan Millat
- Sutapa Roy
- M. Mushfiq Monzur

## Important Notes

- Never commit `.env`, `venv/` or `node_modules/`.
- Each team member must configure their own local environment.
- Run the backend and frontend in separate Terminal windows.
- Payments are simulated; no real financial transactions take place.
