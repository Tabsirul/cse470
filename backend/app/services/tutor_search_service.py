from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.syllabus import Syllabus
from app.models.tutor_course import TutorCourse
from app.models.tutor_profile import TutorProfile
from app.models.user import User
from app.services.errors import NotFoundError
from app.services.matching import Candidate, rank_candidates


def _ratings_for(db: Session, tutor_ids: list[int]) -> dict[int, float]:
    """Average review stars for each tutor.

    Reviews (F13) do not exist yet, so nobody has a rating for now.
    This function will read the reviews table once F13 is built.
    """
    return {}


def search_tutors(
    db: Session,
    course_code: str,
    max_rate: int | None,
    min_rating: float | None,
    syllabus_query: str | None = None,
) -> list[dict]:
    course = db.scalar(select(Course).where(Course.code == course_code.strip().upper()))
    if course is None:
        raise NotFoundError("Course not found")

    # Only tutors with a profile AND an approved application for this course.
    stmt = (
        select(TutorProfile, TutorCourse, User)
        .join(TutorCourse, TutorCourse.tutor_id == TutorProfile.user_id)
        .join(User, User.id == TutorProfile.user_id)
        .outerjoin(Course, Course.id == TutorCourse.course_id)
        .outerjoin(Syllabus, Syllabus.course_id == Course.id)
        .where(TutorCourse.course_id == course.id, TutorCourse.status == "approved")
    )
    if syllabus_query:
        keyword = f"%{syllabus_query}%"
        stmt = stmt.where(
            or_(
                Syllabus.midterm_topics.ilike(keyword),
                Syllabus.assignment_modules.ilike(keyword),
                Syllabus.lab_requirements.ilike(keyword),
            )
        )
    rows = db.execute(stmt).all()

    ratings = _ratings_for(db, [user.id for _, _, user in rows])
    bios = {}
    candidates = []
    for profile, claim, user in rows:
        bios[user.id] = profile.bio
        candidates.append(
            Candidate(
                tutor_id=user.id,
                name=user.name,
                hourly_rate=profile.hourly_rate,
                grade=claim.claimed_grade,
                rating=ratings.get(user.id),
            )
        )

    ranked = rank_candidates(candidates, max_rate, min_rating)
    return [
        {
            "tutor_id": candidate.tutor_id,
            "tutor_name": candidate.name,
            "bio": bios[candidate.tutor_id],
            "hourly_rate": candidate.hourly_rate,
            "grade": candidate.grade,
            "rating": candidate.rating,
            "score": score,
        }
        for candidate, score in ranked
    ]