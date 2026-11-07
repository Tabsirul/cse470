from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, index=True)  # e.g. CSE470
    title: Mapped[str] = mapped_column(String(200))