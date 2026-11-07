from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.syllabus import Syllabus
from app.models.tutor_course import TutorCourse
from app.models.tutor_profile import TutorProfile
from app.models.user import User
from app.services.booking_service import free_slot_counts
from app.services.errors import NotFoundError
from app.services.matching import Candidate, rank_candidates
from app.services.review_service import rating_stats


def search_tutors(
    db: Session,
    course_code: str,
    max_rate: int | None,
    min_rating: float | None,
    only_with_free_session: bool = False,
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

    stats = rating_stats(db, [user.id for _, _, user in rows])  # tutor id -> (average, count)
    bios = {}
    candidates = []
    for profile, claim, user in rows:
        bios[user.id] = profile.bio
        average = stats[user.id][0] if user.id in stats else None
        candidates.append(
            Candidate(
                tutor_id=user.id,
                name=user.name,
                hourly_rate=profile.hourly_rate,
                grade=claim.claimed_grade,
                rating=average,
            )
        )

    free = free_slot_counts(db, course.id)
    if only_with_free_session:
        candidates = [c for c in candidates if free.get(c.tutor_id, 0) > 0]

    ranked = rank_candidates(candidates, max_rate, min_rating)
    return [
        {
            "tutor_id": candidate.tutor_id,
            "tutor_name": candidate.name,
            "bio": bios[candidate.tutor_id],
            "hourly_rate": candidate.hourly_rate,
            "grade": candidate.grade,
            "rating": candidate.rating,
            "review_count": stats[candidate.tutor_id][1] if candidate.tutor_id in stats else 0,
            "score": score,
            "free_sessions": free.get(candidate.tutor_id, 0),
        }
        for candidate, score in ranked
    ]