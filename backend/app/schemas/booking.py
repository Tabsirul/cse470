from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class SlotCreateRequest(BaseModel):
    course: str = Field(min_length=2, max_length=20)  # course code, like CSE470
    starts_at: datetime
    duration_minutes: int = Field(ge=30, le=240)
    capacity: int = Field(ge=1, le=20)  # 1 = one-to-one, more = group session

    @field_validator("starts_at")
    @classmethod
    def must_be_local_time(cls, value: datetime) -> datetime:
        if value.tzinfo is not None:
            raise ValueError("Send the time without a time zone, like 2026-11-10T15:00")
        return value


class SlotResponse(BaseModel):
    slot_id: int
    tutor_id: int
    tutor_name: str
    course_code: str
    starts_at: datetime
    duration_minutes: int
    capacity: int
    booked_count: int
    seats_left: int
    price: int  # taka per student
    status: str


class BookingResponse(BaseModel):
    booking_id: int
    status: str
    can_cancel: bool
    slot: SlotResponse