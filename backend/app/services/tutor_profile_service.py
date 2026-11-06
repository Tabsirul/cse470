from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.tutor_course import TutorCourse
from app.models.tutor_profile import TutorProfile
from app.models.user import User
from app.services.errors import NotFoundError


def _find_profile(db: Session, user: User) -> TutorProfile | None:
    return db.scalar(select(TutorProfile).where(TutorProfile.user_id == user.id))


def _profile_detail(db: Session, profile: TutorProfile, user: User) -> dict:
    codes = db.scalars(
        select(Course.code)
        .join(TutorCourse, TutorCourse.course_id == Course.id)
        .where(TutorCourse.tutor_id == user.id, TutorCourse.status == "approved")
        .order_by(Course.code)
    ).all()
    return {
        "user_id": user.id,
        "tutor_name": user.name,
        "bio": profile.bio,
        "hourly_rate": profile.hourly_rate,
        "approved_courses": list(codes),
    }


def get_profile(db: Session, user: User) -> dict:
    profile = _find_profile(db, user)
    if profile is None:
        raise NotFoundError("You have not made a tutor profile yet")
    return _profile_detail(db, profile, user)


def save_profile(db: Session, user: User, bio: str | None, hourly_rate: int) -> dict:
    bio = (bio or "").strip() or None
    profile = _find_profile(db, user)
    if profile is None:
        profile = TutorProfile(user_id=user.id, bio=bio, hourly_rate=hourly_rate)
        db.add(profile)
    else:
        profile.bio = bio
        profile.hourly_rate = hourly_rate
    db.commit()
    db.refresh(profile)
    return _profile_detail(db, profile, user)