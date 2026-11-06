from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class PayRequest(BaseModel):
    method: Literal["bkash", "nagad"]
    account: str = Field(pattern=r"^01[3-9]\d{8}$")  # a Bangladeshi mobile number


class PaymentResponse(BaseModel):
    payment_id: int
    booking_id: int
    course_code: str
    tutor_name: str
    starts_at: datetime
    amount: int
    status: str
    method: str
    account_last4: str
    reference: str


class EarningItem(BaseModel):
    payment_id: int
    course_code: str
    starts_at: datetime
    student_name: str
    amount: int
    platform_fee: int
    tutor_amount: int
    status: str  # held = waiting for the session, released = paid to the tutor


class EarningsResponse(BaseModel):
    released_total: int
    pending_total: int
    items: list[EarningItem]