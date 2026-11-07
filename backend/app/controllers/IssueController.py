from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.models.dispute import Dispute, IssueType, DisputeStatus
from app.database import get_db

class DisputeCreate(BaseModel):
    session_id: int
    issue_type: IssueType
    description: str

class DisputeResponse(BaseModel):
    id: int
    session_id: int
    issue_type: IssueType
    description: str
    status: DisputeStatus
    
    class Config:
        from_attributes = True

router = APIRouter(prefix="/api/issues", tags=["Issues"])

@router.post("/report", response_model=DisputeResponse, status_code=status.HTTP_201_CREATED)
def report_issue(dispute_data: DisputeCreate, db: Session = Depends(get_db)):
    current_user_id = 1 # Placeholder for auth dependency
    
    new_dispute = Dispute(
        reporter_id=current_user_id,
        session_id=dispute_data.session_id,
        issue_type=dispute_data.issue_type,
        description=dispute_data.description
    )
    
    db.add(new_dispute)
    db.commit()
    db.refresh(new_dispute)
    
    return new_dispute

@router.get("/my-reports", response_model=List[DisputeResponse])
def get_user_reports(db: Session = Depends(get_db)):
    current_user_id = 1
    reports = db.query(Dispute).filter(Dispute.reporter_id == current_user_id).all()
    return reports