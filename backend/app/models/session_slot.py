from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SessionSlot(Base):
    """A time a tutor offers for one course. capacity 1 = one-to-one, more = group."""

    __tablename__ = "session_slots"

    id: Mapped[int] = mapped_column(primary_key=True)
    tutor_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    starts_at: Mapped[datetime] = mapped_column(DateTime)
    duration_minutes: Mapped[int] = mapped_column()
    capacity: Mapped[int] = mapped_column(default=1)
    price: Mapped[int] = mapped_column()  # taka per student, fixed when the slot is made
    status: Mapped[str] = mapped_column(String(20), default="open")  # open / cancelled / completed
    created_at: Mapped[datetime] = mapped_column(DateTime, default=__import__('datetime').datetime.now)