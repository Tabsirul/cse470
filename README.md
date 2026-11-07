# StudyBuddy: Campus Peer Tutoring

StudyBuddy is a web platform where students find tutors who did well in the same course, book a session, pay safely, and review the session afterwards. It is the CSE470 (Software Engineering) group project of Group 4 at BRAC University.

Built with React, FastAPI and PostgreSQL, following the MVC pattern.

## What it does

| Feature | What it does |
|---|---|
| F17 Prerequisite validation | A tutor applies for a course with their grade. The grade is checked against the course's minimum grade, and an admin can override the result. |
| F1 Tutor search and matching | A student searches by course, budget and rating. Tutors are ranked by a match score from rating, grade and price. |
| F5 Session reservation | Tutors offer one-to-one or group sessions. Seats cannot be double-booked, a student cannot book overlapping sessions, and a booking can be cancelled up to 2 hours before the start. |
| F9 Escrow payment | A student's payment is held until the session is completed, then released to the tutor minus a 10% platform fee. It is refunded if the booking or session is cancelled. |
| F13 Session review | A student who paid for a completed session can give 1 to 5 stars and a comment. Ratings feed back into tutor matching. |

Payments use a **sandbox**: no real money moves. A mobile number ending in `0000` is declined, so you can test a failed payment.

Other features of the project are built by their owners on separate branches.

## Roles

- **Student:** search for tutors, book, pay and review sessions.
- **Tutor:** make a profile, apply for courses, offer sessions, see earnings and reviews.
- **Admin:** set grade rules and review tutor applications. To make a user an admin, run in PostgreSQL:
  ```sql
  UPDATE users SET role = 'admin' WHERE email = 'your@email.com';
  ```

## How the code is organized (MVC)

| Part | Where | What it holds |
|---|---|---|
| Model | `backend/app/models/` | SQLAlchemy tables |
| View | `frontend/src/views/` | React pages |
| Controller | `backend/app/controllers/` | FastAPI routes |
| Services | `backend/app/services/` | The business rules (matching, booking, payment, review) |
| Schemas | `backend/app/schemas/` | Request and response shapes |

The rules that decide things (grade checks, match score, booking limits, payment moves, review limits) are small functions with tests in `backend/tests/`.

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
Also replace SECRET_KEY with your own random text. Make one with: `python3 -c "import secrets; print(secrets.token_hex(32))"`

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

## Run the tests

From `backend`, with the virtual environment active:

```bash
python -m pytest -q
```

## Try the whole flow

1. Register a tutor and a student, and make one user an admin (see Roles).
2. Tutor: apply for a course on "Tutor course verification". Admin: approve it.
3. Tutor: save a profile, then add a session on "My session slots".
4. Student: "Find a tutor", then "Book a session", book it and pay (sandbox).
5. Tutor: mark the session completed after its start time. The payment is released.
6. Student: leave a review. The tutor's rating appears in search.

## Important

- Never commit `.env`, `venv/`, or `node_modules/`.
- Each teammate must create their own local `.env` file.
- Run the backend and frontend in separate Terminal windows.