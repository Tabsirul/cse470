from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models.user import User
from app.schemas.review import ReviewRequest, TutorReviewsResponse
from app.services import review_service

router = APIRouter(prefix="/api/reviews", tags=["reviews"])


@router.post("/bookings/{booking_id}", status_code=status.HTTP_201_CREATED)
def create_review(
    booking_id: int,
    data: ReviewRequest,
    db: Session = Depends(get_db),
    student: User = Depends(require_role("student")),
):
    return review_service.create_review(db, student, booking_id, data.rating, data.comment)


@router.get("/tutors/{tutor_id}", response_model=TutorReviewsResponse)
def tutor_reviews(
    tutor_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return review_service.tutor_reviews(db, tutor_id)