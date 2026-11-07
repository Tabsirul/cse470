from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Syllabus(Base):
    __tablename__ = "syllabi"

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), unique=True)
    midterm_topics: Mapped[str | None] = mapped_column(Text, nullable=True)
    assignment_modules: Mapped[str | None] = mapped_column(Text, nullable=True)
    lab_requirements: Mapped[str | None] = mapped_column(Text, nullable=True)

    course: Mapped["Course"] = relationship("Course", back_populates="syllabus")