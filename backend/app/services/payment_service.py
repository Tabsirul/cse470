from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, aliased

from app.models.booking import Booking
from app.models.course import Course
from app.models.payment import Payment
from app.models.session_slot import SessionSlot
from app.models.user import User
from app.services import payment_gateway
from app.services.errors import ConflictError, NotFoundError
from app.services.payment_rules import next_status, payment_problem, split_payment


def _payment_query():
    tutor = aliased(User)
    return (
        select(Payment, SessionSlot, Course.code, tutor.name)
        .join(Booking, Booking.id == Payment.booking_id)
        .join(SessionSlot, SessionSlot.id == Booking.slot_id)
        .join(Course, Course.id == SessionSlot.course_id)
        .join(tutor, tutor.id == SessionSlot.tutor_id)
    )


def _payment_response(payment: Payment, slot: SessionSlot, course_code: str, tutor_name: str) -> dict:
    return {
        "payment_id": payment.id,
        "booking_id": payment.booking_id,
        "course_code": course_code,
        "tutor_name": tutor_name,
        "starts_at": slot.starts_at,
        "amount": payment.amount,
        "status": payment.status,
        "method": payment.method,
        "account_last4": payment.account_last4,
        "reference": payment.reference,
    }


# ---------- student: pay ----------

def pay_booking(db: Session, student: User, booking_id: int, method: str, account: str) -> dict:
    # lock the booking row, so a double click cannot create two payments
    booking = db.scalar(select(Booking).where(Booking.id == booking_id).with_for_update())
    if booking is None or booking.student_id != student.id:
        raise NotFoundError("Booking not found")
    slot = db.get(SessionSlot, booking.slot_id)

    already_paid = (
        db.scalar(
            select(Payment.id).where(
                Payment.booking_id == booking.id, Payment.status.in_(["held", "released"])
            )
        )
        is not None
    )
    problem = payment_problem(booking.status, slot.status, slot.starts_at, datetime.now(), already_paid)
    if problem is not None:
        raise ConflictError(problem)

    result = payment_gateway.charge(method, account, slot.price)
    if not result.ok:
        raise ConflictError(result.message)

    payment = Payment(
        booking_id=booking.id,
        amount=slot.price,
        status="held",  # escrow: the platform holds it, the tutor does not have it yet
        method=method,
        account_last4=account[-4:],
        reference=result.reference,
    )
    db.add(payment)
    db.commit()

    row = db.execute(_payment_query().where(Payment.id == payment.id)).one()
    return _payment_response(*row)


def my_payments(db: Session, student: User) -> list[dict]:
    rows = db.execute(
        _payment_query().where(Booking.student_id == student.id).order_by(Payment.id.desc())
    ).all()
    return [_payment_response(*row) for row in rows]


# ---------- called by booking_service (they do NOT commit; the caller commits) ----------

def refund_held_for_booking(db: Session, booking_id: int) -> None:
    """Give the money back for one booking, if it is held."""
    for payment in db.scalars(
        select(Payment).where(Payment.booking_id == booking_id, Payment.status == "held")
    ):
        payment.refund_reference = payment_gateway.refund(payment.reference)
        payment.status = next_status(payment.status, "refund")


def release_for_slot(db: Session, slot_id: int) -> None:
    """The session is done: pay the tutor for every held payment in this slot."""
    payments = db.scalars(
        select(Payment)
        .join(Booking, Booking.id == Payment.booking_id)
        .where(
            Booking.slot_id == slot_id,
            Booking.status == "booked",
            Payment.status == "held",
        )
    )
    for payment in payments:
        tutor_amount, fee = split_payment(payment.amount)
        payment.tutor_amount = tutor_amount
        payment.platform_fee = fee
        payment.status = next_status(payment.status, "release")


# ---------- tutor: earnings ----------

def earnings(db: Session, tutor: User) -> dict:
    student = aliased(User)
    rows = db.execute(
        select(Payment, SessionSlot, Course.code, student.name)
        .join(Booking, Booking.id == Payment.booking_id)
        .join(SessionSlot, SessionSlot.id == Booking.slot_id)
        .join(Course, Course.id == SessionSlot.course_id)
        .join(student, student.id == Booking.student_id)
        .where(SessionSlot.tutor_id == tutor.id, Payment.status.in_(["held", "released"]))
        .order_by(Payment.id.desc())
    ).all()

    items = []
    released_total = 0
    pending_total = 0
    for payment, slot, course_code, student_name in rows:
        if payment.status == "released":
            tutor_amount, fee = payment.tutor_amount, payment.platform_fee
            released_total += tutor_amount
        else:  # held: show what the tutor WILL get
            tutor_amount, fee = split_payment(payment.amount)
            pending_total += tutor_amount
        items.append(
            {
                "payment_id": payment.id,
                "course_code": course_code,
                "starts_at": slot.starts_at,
                "student_name": student_name,
                "amount": payment.amount,
                "platform_fee": fee,
                "tutor_amount": tutor_amount,
                "status": payment.status,
            }
        )
    return {"released_total": released_total, "pending_total": pending_total, "items": items}