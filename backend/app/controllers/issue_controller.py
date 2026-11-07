from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.issue import DisputeCreate, DisputeOut
from app.services import issue_service

router = APIRouter(prefix="/api/issues", tags=["Issues"])

@router.post("/report", response_model=DisputeOut)
def report_issue(
    dispute_in: DisputeCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)  # This enforces login!
):
    return issue_service.create_dispute(db=db, dispute_in=dispute_in, user_id=user.id)

@router.get("/my-reports", response_model=List[DisputeOut])
def get_my_reports(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return issue_service.get_my_reports(db=db, user_id=user.id)