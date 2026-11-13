from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Prerequisite(Base):
    __tablename__ = "prerequisites"

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), unique=True
    )
    min_grade: Mapped[str] = mapped_column(String(3))  # lowest grade allowed, e.g. "A-"
    created_at: Mapped[datetime] = mapped_column(DateTime, default=__import__('datetime').datetime.now)