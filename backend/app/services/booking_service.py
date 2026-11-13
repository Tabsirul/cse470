from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.course import Course
from app.models.payment import Payment
from app.models.review import Review
from app.models.session_slot import SessionSlot
from app.models.tutor_course import TutorCourse
from app.models.tutor_profile import TutorProfile
from app.models.user import User
from app.services.booking_rules import (
    MIN_CANCEL_HOURS,
    booking_problem,
    can_cancel,
    seats_left,
    slots_overlap,
)
from app.services import payment_service
from app.services.errors import ConflictError, NotFoundError


# ---------- helpers ----------

def _booked_counts(db: Session, slot_ids: list[int]) -> dict[int, int]:
    """How many students have a live booking, for each slot id."""
    if not slot_ids:
        return {}
    rows = db.execute(
        select(Booking.slot_id, func.count())
        .where(Booking.slot_id.in_(slot_ids), Booking.status == "booked")
        .group_by(Booking.slot_id)
    ).all()
    return dict(rows)


def _slot_responses(db: Session, rows) -> list[dict]:
    """rows are (SessionSlot, course_code, tutor_name) tuples."""
    counts = _booked_counts(db, [slot.id for slot, _, _ in rows])
    result = []
    for slot, course_code, tutor_name in rows:
        booked = counts.get(slot.id, 0)
        result.append(
            {
                "slot_id": slot.id,
                "tutor_id": slot.tutor_id,
                "tutor_name": tutor_name,
                "course_code": course_code,
                "starts_at": slot.starts_at,
                "duration_minutes": slot.duration_minutes,
                "capacity": slot.capacity,
                "booked_count": booked,
                "seats_left": seats_left(slot.capacity, booked),
                "price": slot.price,
                "status": slot.status,
            }
        )
    return result


def _slot_query():
    return (
        select(SessionSlot, Course.code, User.name)
        .join(Course, Course.id == SessionSlot.course_id)
        .join(User, User.id == SessionSlot.tutor_id)
    )


def _one_slot_response(db: Session, slot_id: int) -> dict:
    rows = db.execute(_slot_query().where(SessionSlot.id == slot_id)).all()
    return _slot_responses(db, rows)[0]


def _booking_response(db: Session, booking: Booking, now: datetime) -> dict:
    slot = _one_slot_response(db, booking.slot_id)
    return {
        "booking_id": booking.id,
        "status": booking.status,
        "can_cancel": booking.status == "booked"
        and slot["status"] == "open"
        and can_cancel(slot["starts_at"], now),
        "payment_status": db.scalar(
            select(Payment.status)
            .where(Payment.booking_id == booking.id)
            .order_by(Payment.id.desc())
            .limit(1)
        ),
        "review_rating": db.scalar(select(Review.rating).where(Review.booking_id == booking.id)),
        "slot": slot,
    }


def free_slot_counts(db: Session, course_id: int) -> dict[int, int]:
    """For one course: tutor id -> number of future open slots that still have a free seat."""
    slots = db.scalars(
        select(SessionSlot).where(
            SessionSlot.course_id == course_id,
            SessionSlot.status == "open",
            SessionSlot.starts_at > datetime.CURRENT_TIMESTAMP,
        )
    ).all()
    counts = _booked_counts(db, [slot.id for slot in slots])
    free: dict[int, int] = {}
    for slot in slots:
        if seats_left(slot.capacity, counts.get(slot.id, 0)) > 0:
            free[slot.tutor_id] = free.get(slot.tutor_id, 0) + 1
    return free


# ---------- tutor side ----------

def create_slot(
    db: Session,
    tutor: User,
    course_code: str,
    starts_at: datetime,
    duration_minutes: int,
    capacity: int,
) -> dict:
    course = db.scalar(select(Course).where(Course.code == course_code.strip().upper()))
    if course is None:
        raise NotFoundError("Course not found")

    approved = db.scalar(
        select(TutorCourse).where(
            TutorCourse.tutor_id == tutor.id,
            TutorCourse.course_id == course.id,
            TutorCourse.status == "approved",
        )
    )
    if approved is None:
        raise ConflictError("You are not approved to tutor this course")

    profile = db.scalar(select(TutorProfile).where(TutorProfile.user_id == tutor.id))
    if profile is None:
        raise ConflictError("Make your tutor profile first")

    if starts_at <= datetime.CURRENT_TIMESTAMP:
        raise ConflictError("The start time must be in the future")

    my_open = db.scalars(
        select(SessionSlot).where(SessionSlot.tutor_id == tutor.id, SessionSlot.status == "open")
    ).all()
    for other in my_open:
        if slots_overlap(starts_at, duration_minutes, other.starts_at, other.duration_minutes):
            raise ConflictError("You already have a session at this time")

    slot = SessionSlot(
        tutor_id=tutor.id,
        course_id=course.id,
        starts_at=starts_at,
        duration_minutes=duration_minutes,
        capacity=capacity,
        price=round(profile.hourly_rate * duration_minutes / 60),
        status="open",
    )
    db.add(slot)
    db.commit()
    return _one_slot_response(db, slot.id)


def my_slots(db: Session, tutor: User) -> list[dict]:
    rows = db.execute(
        _slot_query().where(SessionSlot.tutor_id == tutor.id).order_by(SessionSlot.starts_at)
    ).all()
    return _slot_responses(db, rows)


def _own_open_slot(db: Session, tutor: User, slot_id: int) -> SessionSlot:
    slot = db.get(SessionSlot, slot_id)
    if slot is None or slot.tutor_id != tutor.id:
        raise NotFoundError("Session not found")
    if slot.status != "open":
        raise ConflictError(f"This session is already {slot.status}")
    return slot


def cancel_slot(db: Session, tutor: User, slot_id: int) -> dict:
    slot = _own_open_slot(db, tutor, slot_id)
    slot.status = "cancelled"
    # every student who booked it is released, and gets their money back
    for booking in db.scalars(
        select(Booking).where(Booking.slot_id == slot.id, Booking.status == "booked")
    ):
        booking.status = "cancelled"
        payment_service.refund_held_for_booking(db, booking.id)
    db.commit()
    return _one_slot_response(db, slot.id)


def complete_slot(db: Session, tutor: User, slot_id: int) -> dict:
    slot = _own_open_slot(db, tutor, slot_id)
    if slot.starts_at > datetime.CURRENT_TIMESTAMP:
        raise ConflictError("The session has not started yet")
    if _booked_counts(db, [slot.id]).get(slot.id, 0) == 0:
        raise ConflictError("Nobody booked this session")
    slot.status = "completed"
    payment_service.release_for_slot(db, slot.id)  # pay the tutor
    db.commit()
    return _one_slot_response(db, slot.id)


# ---------- student side ----------

def list_open_slots(db: Session, course_code: str | None) -> list[dict]:
    query = _slot_query().where(
        SessionSlot.status == "open", SessionSlot.starts_at > datetime.CURRENT_TIMESTAMP
    )
    if course_code:
        query = query.where(Course.code == course_code.strip().upper())
    rows = db.execute(query.order_by(SessionSlot.starts_at)).all()
    return _slot_responses(db, rows)


def book_slot(db: Session, student: User, slot_id: int) -> dict:
    # with_for_update locks this slot row until we commit, so two students
    # cannot take the last seat at the same moment (PostgreSQL).
    slot = db.scalar(select(SessionSlot).where(SessionSlot.id == slot_id).with_for_update())
    if slot is None:
        raise NotFoundError("Session not found")
    if slot.status != "open":
        raise ConflictError("This session is not open for booking")

    now = datetime.CURRENT_TIMESTAMP
    booked = _booked_counts(db, [slot.id]).get(slot.id, 0)

    existing = db.scalar(
        select(Booking).where(Booking.slot_id == slot.id, Booking.student_id == student.id)
    )

    # Does the student already have a live booking that overlaps this slot?
    others = db.scalars(
        select(SessionSlot)
        .join(Booking, Booking.slot_id == SessionSlot.id)
        .where(
            Booking.student_id == student.id,
            Booking.status == "booked",
            SessionSlot.status == "open",
            SessionSlot.id != slot.id,
        )
    ).all()
    has_clash = any(
        slots_overlap(slot.starts_at, slot.duration_minutes, o.starts_at, o.duration_minutes)
        for o in others
    )

    problem = booking_problem(
        starts_at=slot.starts_at,
        now=now,
        capacity=slot.capacity,
        booked=booked,
        already_booked=existing is not None and existing.status == "booked",
        has_clash=has_clash,
    )
    if problem is not None:
        raise ConflictError(problem)

    if existing is not None:  # an old cancelled booking: switch it back on
        existing.status = "booked"
        booking = existing
    else:
        booking = Booking(slot_id=slot.id, student_id=student.id, status="booked")
        db.add(booking)
    db.commit()
    return _booking_response(db, booking, now)


def my_bookings(db: Session, student: User) -> list[dict]:
    now = datetime.CURRENT_TIMESTAMP
    bookings = db.scalars(
        select(Booking)
        .join(SessionSlot, SessionSlot.id == Booking.slot_id)
        .where(Booking.student_id == student.id)
        .order_by(SessionSlot.starts_at)
    ).all()
    return [_booking_response(db, booking, now) for booking in bookings]


def cancel_booking(db: Session, student: User, booking_id: int) -> dict:
    booking = db.get(Booking, booking_id)
    if booking is None or booking.student_id != student.id:
        raise NotFoundError("Booking not found")
    if booking.status != "booked":
        raise ConflictError("This booking is already cancelled")
    slot = db.get(SessionSlot, booking.slot_id)
    now = datetime.CURRENT_TIMESTAMP
    if not can_cancel(slot.starts_at, now):
        raise ConflictError(
            f"Too late to cancel: cancel at least {MIN_CANCEL_HOURS} hours before the start"
        )
    booking.status = "cancelled"
    payment_service.refund_held_for_booking(db, booking.id)  # money back, same commit
    db.commit()
    return _booking_response(db, booking, now)