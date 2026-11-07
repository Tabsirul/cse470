from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_role
from app.models.user import User
from app.schemas.payment import EarningsResponse, PaymentResponse, PayRequest
from app.services import payment_service

router = APIRouter(prefix="/api/payments", tags=["payments"])


@router.post(
    "/bookings/{booking_id}/pay",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
def pay_booking(
    booking_id: int,
    data: PayRequest,
    db: Session = Depends(get_db),
    student: User = Depends(require_role("student")),
):
    return payment_service.pay_booking(db, student, booking_id, data.method, data.account)


@router.get("/my-payments", response_model=list[PaymentResponse])
def my_payments(
    db: Session = Depends(get_db),
    student: User = Depends(require_role("student")),
):
    return payment_service.my_payments(db, student)


@router.get("/earnings", response_model=EarningsResponse)
def earnings(
    db: Session = Depends(get_db),
    tutor: User = Depends(require_role("tutor")),
):
    return payment_service.earnings(db, tutor)