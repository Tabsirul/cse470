from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

class DisputeCreate(BaseModel):
    booking_id: int
    issue_type: Literal['missed_appointment', 'late_arrival', 'unhelpful_session', 'other']
    description: str = Field(min_length=10, max_length=1000)

class DisputeOut(BaseModel):
    id: int
    booking_id: int
    reporter_id: int
    issue_type: str
    description: str
    status: str
    
    model_config = ConfigDict(from_attributes=True)