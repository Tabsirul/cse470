from sqlalchemy.orm import Session
from typing import Optional
from app.models.course import Course
from app.models.syllabus import Syllabus

def get_filtered_courses(db: Session, search: Optional[str] = None):
    query = db.query(Course).outerjoin(Course.syllabus)
    
    if search:
        keyword = f"%{search}%"
        query = query.filter(
            (Course.code.ilike(keyword)) |
            (Course.title.ilike(keyword)) |
            (Syllabus.midterm_topics.ilike(keyword)) |
            (Syllabus.assignment_modules.ilike(keyword)) |
            (Syllabus.lab_requirements.ilike(keyword))
        )
    return query.all()