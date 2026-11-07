from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from app.database import Base # Adjust import based on your existing database.py location
import enum

class IssueType(enum.Enum):
    MISSED_APPOINTMENT = "missed_appointment"
    LATE_ARRIVAL = "late_arrival"
    UNHELPFUL_SESSION = "unhelpful_session"
    OTHER = "other"

class DisputeStatus(enum.Enum):
    PENDING = "pending"
    REVIEWING = "reviewing"
    ESCALATED = "escalated"
    RESOLVED = "resolved"

class Dispute(Base):
    __tablename__ = "disputes"

    id = Column(Integer, primary_key=True, index=True)
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    
    issue_type = Column(Enum(IssueType), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum(DisputeStatus), default=DisputeStatus.PENDING)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())