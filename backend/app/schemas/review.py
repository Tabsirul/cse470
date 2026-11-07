from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class ReviewRequest(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str | None = Field(default=None, max_length=500)

    @field_validator("comment")
    @classmethod
    def blank_comment_is_none(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None


class ReviewResponse(BaseModel):
    review_id: int
    rating: int
    comment: str | None
    student_name: str  # first name only, for privacy
    course_code: str
    created_at: datetime


class TutorReviewsResponse(BaseModel):
    tutor_id: int
    tutor_name: str
    average: float | None
    count: int
    stars: dict[int, int]  # how many reviews gave 5, 4, 3, 2, 1 stars
    reviews: list[ReviewResponse]