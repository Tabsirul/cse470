from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models.user import User
from app.schemas.tutor_profile import ProfileRequest, ProfileResponse
from app.schemas.tutor_search import TutorMatchResponse
from app.services import tutor_profile_service, tutor_search_service

router = APIRouter(prefix="/api/tutors", tags=["tutors"])


@router.get("/me/profile", response_model=ProfileResponse)
def my_profile(
    db: Session = Depends(get_db),
    tutor: User = Depends(require_role("tutor")),
):
    return tutor_profile_service.get_profile(db, tutor)


@router.put("/me/profile", response_model=ProfileResponse)
def save_my_profile(
    data: ProfileRequest,
    db: Session = Depends(get_db),
    tutor: User = Depends(require_role("tutor")),
):
    return tutor_profile_service.save_profile(db, tutor, data.bio, data.hourly_rate)


@router.get("/search", response_model=list[TutorMatchResponse])
def search_tutors(
    course: str = Query(min_length=2, max_length=20),
    max_rate: int | None = Query(default=None, gt=0),
    min_rating: float | None = Query(default=None, ge=1, le=5),
    free_session: bool = Query(default=False),
    syllabus: str | None = Query(default=None, description="Filter by midterm topics, modules, or labs"),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return tutor_search_service.search_tutors(db, course, max_rate, min_rating, free_session, syllabus_query=syllabus)
