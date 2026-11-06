from pydantic import BaseModel


class TutorMatchResponse(BaseModel):
    tutor_id: int
    tutor_name: str
    bio: str | None
    hourly_rate: int
    grade: str
    rating: float | None
    score: float