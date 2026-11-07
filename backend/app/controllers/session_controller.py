from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models.user import User
from app.schemas.booking import BookingResponse, SlotCreateRequest, SlotResponse
from app.services import booking_service

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


# ----- tutor -----

@router.post("/slots", response_model=SlotResponse, status_code=status.HTTP_201_CREATED)
def create_slot(
    data: SlotCreateRequest,
    db: Session = Depends(get_db),
    tutor: User = Depends(require_role("tutor")),
):
    return booking_service.create_slot(
        db, tutor, data.course, data.starts_at, data.duration_minutes, data.capacity
    )


@router.get("/my-slots", response_model=list[SlotResponse])
def my_slots(
    db: Session = Depends(get_db),
    tutor: User = Depends(require_role("tutor")),
):
    return booking_service.my_slots(db, tutor)


@router.post("/slots/{slot_id}/cancel", response_model=SlotResponse)
def cancel_slot(
    slot_id: int,
    db: Session = Depends(get_db),
    tutor: User = Depends(require_role("tutor")),
):
    return booking_service.cancel_slot(db, tutor, slot_id)


@router.post("/slots/{slot_id}/complete", response_model=SlotResponse)
def complete_slot(
    slot_id: int,
    db: Session = Depends(get_db),
    tutor: User = Depends(require_role("tutor")),
):
    return booking_service.complete_slot(db, tutor, slot_id)


# ----- students -----

@router.get("/slots", response_model=list[SlotResponse])
def open_slots(
    course: str | None = Query(default=None, max_length=20),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return booking_service.list_open_slots(db, course)


@router.post(
    "/slots/{slot_id}/book", response_model=BookingResponse, status_code=status.HTTP_201_CREATED
)
def book_slot(
    slot_id: int,
    db: Session = Depends(get_db),
    student: User = Depends(require_role("student")),
):
    return booking_service.book_slot(db, student, slot_id)


@router.get("/my-bookings", response_model=list[BookingResponse])
def my_bookings(
    db: Session = Depends(get_db),
    student: User = Depends(require_role("student")),
):
    return booking_service.my_bookings(db, student)


@router.post("/bookings/{booking_id}/cancel", response_model=BookingResponse)
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    student: User = Depends(require_role("student")),
):
    return booking_service.cancel_booking(db, student, booking_id)