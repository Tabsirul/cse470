from sqlalchemy import select
from sqlalchemy.orm import Session, aliased

from app.models.booking import Booking
from app.models.course import Course
from app.models.payment import Payment
from app.models.review import Review
from app.models.session_slot import SessionSlot
from app.models.user import User
from app.services.errors import ConflictError, NotFoundError
from app.services.review_rules import average_rating, review_problem, star_counts


def create_review(
    db: Session, student: User, booking_id: int, rating: int, comment: str | None
) -> dict:
    # lock the booking row, so a double click cannot create two reviews
    booking = db.scalar(select(Booking).where(Booking.id == booking_id).with_for_update())
    if booking is None or booking.student_id != student.id:
        raise NotFoundError("Booking not found")
    slot = db.get(SessionSlot, booking.slot_id)

    payment_status = db.scalar(
        select(Payment.status)
        .where(Payment.booking_id == booking.id)
        .order_by(Payment.id.desc())
        .limit(1)
    )
    already_reviewed = (
        db.scalar(select(Review.id).where(Review.booking_id == booking.id)) is not None
    )

    problem = review_problem(booking.status, slot.status, payment_status, already_reviewed)
    if problem is not None:
        raise ConflictError(problem)

    review = Review(
        booking_id=booking.id,
        tutor_id=slot.tutor_id,
        student_id=student.id,
        rating=rating,
        comment=comment,
    )
    db.add(review)
    db.commit()
    return {"review_id": review.id, "rating": review.rating}


def rating_stats(db: Session, tutor_ids: list[int]) -> dict[int, tuple[float, int]]:
    """tutor id -> (average stars, number of reviews). Tutors with no reviews are left out."""
    if not tutor_ids:
        return {}
    rows = db.execute(
        select(Review.tutor_id, Review.rating).where(Review.tutor_id.in_(tutor_ids))
    ).all()
    by_tutor: dict[int, list[int]] = {}
    for tutor_id, rating in rows:
        by_tutor.setdefault(tutor_id, []).append(rating)
    return {tid: (average_rating(r), len(r)) for tid, r in by_tutor.items()}


def tutor_reviews(db: Session, tutor_id: int) -> dict:
    tutor = db.get(User, tutor_id)
    if tutor is None or tutor.role != "tutor":
        raise NotFoundError("Tutor not found")

    student = aliased(User)
    rows = db.execute(
        select(Review, student.name, Course.code)
        .join(Booking, Booking.id == Review.booking_id)
        .join(SessionSlot, SessionSlot.id == Booking.slot_id)
        .join(Course, Course.id == SessionSlot.course_id)
        .join(student, student.id == Review.student_id)
        .where(Review.tutor_id == tutor_id)
        .order_by(Review.id.desc())
    ).all()

    ratings = [review.rating for review, _, _ in rows]
    return {
        "tutor_id": tutor.id,
        "tutor_name": tutor.name,
        "average": average_rating(ratings),
        "count": len(ratings),
        "stars": star_counts(ratings),
        "reviews": [
            {
                "review_id": review.id,
                "rating": review.rating,
                "comment": review.comment,
                "student_name": name.split()[0],
                "course_code": course_code,
                "created_at": review.created_at,
            }
            for review, name, course_code in rows
        ],
    }