from pydantic import BaseModel, Field


class ProfileRequest(BaseModel):
    bio: str | None = Field(default=None, max_length=1000)
    hourly_rate: int = Field(gt=0, le=10000)  # taka per hour


class ProfileResponse(BaseModel):
    user_id: int
    tutor_name: str
    bio: str | None
    hourly_rate: int
    approved_courses: list[str]