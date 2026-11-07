from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.services.course_service import get_filtered_courses

router = APIRouter(prefix="/api/courses", tags=["Courses & Syllabus"])

@router.get("/")
def list_courses(
    search: Optional[str] = Query(None, description="Filter by code, title, or syllabus topics"),
    db: Session = Depends(get_db)
):
    return get_filtered_courses(db, search=search)