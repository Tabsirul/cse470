from datetime import datetime
from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, Field

from app.services.grade_rules import grade_points


def clean_grade(value: str) -> str:
    value = value.strip().upper()
    grade_points(value)  # raises ValueError for an unknown letter, so the API answers 422
    return value


Grade = Annotated[str, AfterValidator(clean_grade)]


class RuleRequest(BaseModel):
    min_grade: Grade


class RuleResponse(BaseModel):
    course_id: int
    course_code: str
    course_title: str
    min_grade: str


class ClaimRequest(BaseModel):
    course_id: int
    claimed_grade: Grade


class ReviewRequest(BaseModel):
    status: Literal["approved", "rejected"]
    reason: str | None = Field(default=None, max_length=255)


class ClaimResponse(BaseModel):
    id: int
    tutor_id: int
    tutor_name: str
    tutor_email: str
    course_id: int
    course_code: str
    claimed_grade: str
    status: str
    reason: str | None
    reviewed_at: datetime | None
    created_at: datetime