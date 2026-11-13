from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base 

class Material(Base):
    __tablename__ = "materials"

    material_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    course_code = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    file_type = Column(String) 
    version = Column(Integer, default=1)
    uploader_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), default=__import__('datetime').datetime.now)