from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class TutorCourse(Base):
    __tablename__ = "tutor_courses"
    __table_args__ = (UniqueConstraint("tutor_id", "course_id", name="uq_tutor_course"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    tutor_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"))
    claimed_grade: Mapped[str] = mapped_column(String(3))  # grade the tutor says they got
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, approved, rejected
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    reviewed_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())