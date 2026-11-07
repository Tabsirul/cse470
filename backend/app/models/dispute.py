from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Dispute(Base):
    """A report filed by a student or tutor about a booked session."""

    __tablename__ = "disputes"

    id: Mapped[int] = mapped_column(primary_key=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id", ondelete="CASCADE"))
    reporter_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    issue_type: Mapped[str] = mapped_column(String(30))   # missed_appointment / late_arrival / unhelpful_session / other
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending / reviewing / escalated / resolved
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())