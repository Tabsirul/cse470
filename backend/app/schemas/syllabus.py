from pydantic import BaseModel
from typing import Optional

class SyllabusResponse(BaseModel):
    id: int
    course_id: int
    midterm_topics: Optional[str] = None
    assignment_modules: Optional[str] = None
    lab_requirements: Optional[str] = None

    class Config:
        from_attributes = True