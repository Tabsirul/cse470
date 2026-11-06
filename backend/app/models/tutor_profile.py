from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class TutorProfile(Base):
    __tablename__ = "tutor_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    hourly_rate: Mapped[int] = mapped_column()  # taka (BDT) per hour
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )