from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.prerequisite import Prerequisite
from app.models.tutor_course import TutorCourse
from app.models.user import User
from app.services.errors import ConflictError, NotFoundError
from app.services.grade_rules import GRADE_POINTS, decide_claim


def get_course(db: Session, course_id: int) -> Course:
    course = db.get(Course, course_id)
    if course is None:
        raise NotFoundError("Course not found")
    return course


def claim_detail(claim: TutorCourse, tutor: User, course: Course) -> dict:
    return {
        "id": claim.id,
        "tutor_id": tutor.id,
        "tutor_name": tutor.name,
        "tutor_email": tutor.email,
        "course_id": course.id,
        "course_code": course.code,
        "claimed_grade": claim.claimed_grade,
        "status": claim.status,
        "reason": claim.reason,
        "reviewed_at": claim.reviewed_at,
        "created_at": claim.created_at,
    }


def rule_detail(rule: Prerequisite, course: Course) -> dict:
    return {
        "course_id": course.id,
        "course_code": course.code,
        "course_title": course.title,
        "min_grade": rule.min_grade,
    }


def list_rules(db: Session) -> list[dict]:
    rows = db.execute(
        select(Prerequisite, Course)
        .join(Course, Prerequisite.course_id == Course.id)
        .order_by(Course.code)
    ).all()
    return [rule_detail(rule, course) for rule, course in rows]

def list_grades() -> list[str]:
    return list(GRADE_POINTS)


def list_courses(db: Session) -> list[dict]:
    rows = db.execute(
        select(Course, Prerequisite)
        .outerjoin(Prerequisite, Prerequisite.course_id == Course.id)
        .order_by(Course.code)
    ).all()
    return [
        {
            "course_id": course.id,
            "course_code": course.code,
            "course_title": course.title,
            "min_grade": rule.min_grade if rule else None,
        }
        for course, rule in rows
    ]
def set_rule(db: Session, course_id: int, min_grade: str) -> dict:
    course = get_course(db, course_id)
    rule = db.scalar(select(Prerequisite).where(Prerequisite.course_id == course_id))
    if rule is None:
        rule = Prerequisite(course_id=course_id, min_grade=min_grade)
        db.add(rule)
    else:
        rule.min_grade = min_grade

    # Claims that were waiting for a rule can be decided now.
    waiting = db.scalars(
        select(TutorCourse).where(
            TutorCourse.course_id == course_id, TutorCourse.status == "pending"
        )
    ).all()
    for claim in waiting:
        claim.status, claim.reason = decide_claim(claim.claimed_grade, min_grade)

    db.commit()
    db.refresh(rule)
    return rule_detail(rule, course)


def submit_claim(db: Session, tutor: User, course_id: int, claimed_grade: str) -> dict:
    course = get_course(db, course_id)
    existing = db.scalar(
        select(TutorCourse).where(
            TutorCourse.tutor_id == tutor.id, TutorCourse.course_id == course_id
        )
    )
    if existing is not None:
        raise ConflictError("You already applied for this course")

    rule = db.scalar(select(Prerequisite).where(Prerequisite.course_id == course_id))
    status, reason = decide_claim(claimed_grade, rule.min_grade if rule else None)

    claim = TutorCourse(
        tutor_id=tutor.id,
        course_id=course_id,
        claimed_grade=claimed_grade,
        status=status,
        reason=reason,
    )
    db.add(claim)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ConflictError("You already applied for this course")
    db.refresh(claim)
    return claim_detail(claim, tutor, course)


def list_claims(db: Session, status: str | None = None, tutor_id: int | None = None) -> list[dict]:
    query = (
        select(TutorCourse, User, Course)
        .join(User, TutorCourse.tutor_id == User.id)
        .join(Course, TutorCourse.course_id == Course.id)
        .order_by(TutorCourse.created_at.desc(), TutorCourse.id.desc())
    )
    if status is not None:
        query = query.where(TutorCourse.status == status)
    if tutor_id is not None:
        query = query.where(TutorCourse.tutor_id == tutor_id)
    rows = db.execute(query).all()
    return [claim_detail(claim, tutor, course) for claim, tutor, course in rows]


def review_claim(db: Session, admin: User, claim_id: int, status: str, reason: str | None) -> dict:
    claim = db.get(TutorCourse, claim_id)
    if claim is None:
        raise NotFoundError("Claim not found")

    claim.status = status
    claim.reason = reason or f"Decided by admin {admin.name}."
    claim.reviewed_by_id = admin.id
    claim.reviewed_at = "CURRENT_TIMESTAMP"
    db.commit()
    db.refresh(claim)

    tutor = db.get(User, claim.tutor_id)
    course = db.get(Course, claim.course_id)
    return claim_detail(claim, tutor, course)