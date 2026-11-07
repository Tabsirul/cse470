"""Put starter data into the database.

Run it from the backend folder, with the virtual environment active:

    python seed.py          adds the course list and a grade rule
    python seed.py --demo   also adds a demo admin, tutor and student (on your own computer only)

It is safe to run again: it never creates the same thing twice.
"""

import sys
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.engine import make_url

from app.database import SessionLocal, engine
from app.models.course import Course
from app.models.syllabus import Syllabus
from app.models.prerequisite import Prerequisite
from app.models.tutor_course import TutorCourse
from app.models.tutor_profile import TutorProfile
from app.models.user import User
from app.services.auth_service import hash_password

COURSES = [
    ("CSE110", "Programming Language I"),
    ("CSE111", "Programming Language II"),
    ("CSE220", "Data Structures"),
    ("CSE221", "Algorithms"),
    ("CSE321", "Operating System"),
    ("CSE470", "Software Engineering"),
]

# course code -> lowest grade a tutor needs to teach it
GRADE_RULES = {"CSE470": "B", "CSE220": "B+"}
SYLLABI = [
    (
        "CSE470",
        "Software process models, agile and scrum, requirements engineering, UML diagrams",
        "Use case modelling, class diagrams, project proposal",
        "Git and GitHub, unit testing, REST API with FastAPI",
    ),
]

DEMO_PASSWORD = "password123"
DEMO_USERS = [
    ("Demo Admin", "admin@example.com", "admin"),
    ("Demo Tutor", "tutor@example.com", "tutor"),
    ("Demo Student", "student@example.com", "student"),
]


def is_local_database(url: str) -> bool:
    """Demo accounts have a known password, so only allow them on your own computer."""
    return make_url(url).host in (None, "", "localhost", "127.0.0.1", "::1")


def seed_courses(db) -> None:
    for code, title in COURSES:
        if db.scalar(select(Course).where(Course.code == code)) is None:
            db.add(Course(code=code, title=title))
            print(f"  added course {code}")
    db.commit()

    for code, min_grade in GRADE_RULES.items():
        course = db.scalar(select(Course).where(Course.code == code))
        if db.scalar(select(Prerequisite).where(Prerequisite.course_id == course.id)) is None:
            db.add(Prerequisite(course_id=course.id, min_grade=min_grade))
            print(f"  added rule: {code} needs at least {min_grade}")
    db.commit()

def seed_syllabi(db) -> None:
    for code, midterm, assignments, labs in SYLLABI:
        course = db.scalar(select(Course).where(Course.code == code))
        if course is None:
            continue
        if db.scalar(select(Syllabus).where(Syllabus.course_id == course.id)) is None:
            db.add(
                Syllabus(
                    course_id=course.id,
                    midterm_topics=midterm,
                    assignment_modules=assignments,
                    lab_requirements=labs,
                )
            )
            print(f"  added syllabus for {code}")
    db.commit()

def seed_demo(db) -> None:
    users = {}
    for name, email, role in DEMO_USERS:
        user = db.scalar(select(User).where(User.email == email))
        if user is None:
            user = User(name=name, email=email, password_hash=hash_password(DEMO_PASSWORD), role=role)
            db.add(user)
            db.commit()
            print(f"  added {role} {email}")
        users[role] = user

    course = db.scalar(select(Course).where(Course.code == "CSE470"))
    tutor, admin = users["tutor"], users["admin"]

    if db.scalar(select(TutorProfile).where(TutorProfile.user_id == tutor.id)) is None:
        db.add(TutorProfile(user_id=tutor.id, hourly_rate=300, bio="Demo tutor for CSE470."))
        print("  added the demo tutor's profile (300 taka per hour)")

    if db.scalar(
        select(TutorCourse).where(TutorCourse.tutor_id == tutor.id, TutorCourse.course_id == course.id)
    ) is None:
        db.add(
            TutorCourse(
                tutor_id=tutor.id,
                course_id=course.id,
                claimed_grade="A",
                status="approved",
                reason="Demo data",
                reviewed_by_id=admin.id,
                reviewed_at=datetime.now(),
            )
        )
        print("  approved the demo tutor for CSE470 with grade A")
    db.commit()


def main() -> None:
    demo = "--demo" in sys.argv
    if demo and not is_local_database(str(engine.url)):
        print("Refusing to add demo accounts: this database is not on your own computer.")
        sys.exit(1)

    with SessionLocal() as db:
        print("Courses and grade rules:")
        seed_courses(db)
        print("Syllabi:")
        seed_syllabi(db)
        if demo:
            print("Demo accounts:")
            seed_demo(db)
            print(f"\nLog in with the password '{DEMO_PASSWORD}' for:")
            for _, email, role in DEMO_USERS:
                print(f"  {role:8} {email}")
    print("\nDone.")


if __name__ == "__main__":
    main()