from typing import Literal

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models.user import User
from app.schemas.verify import (
    ClaimRequest,
    ClaimResponse,
    CourseRuleResponse,
    ReviewRequest,
    RuleRequest,
    RuleResponse,
)
from app.services import verify_service

router = APIRouter(prefix="/api/verify", tags=["prerequisite verification"])

@router.get("/grades", response_model=list[str])
def list_grades(user: User = Depends(get_current_user)):
    return verify_service.list_grades()


@router.get("/courses", response_model=list[CourseRuleResponse])
def list_courses(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return verify_service.list_courses(db)

@router.get("/rules", response_model=list[RuleResponse])
def list_rules(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return verify_service.list_rules(db)


@router.put("/courses/{course_id}/rule", response_model=RuleResponse)
def set_rule(
    course_id: int,
    data: RuleRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role("admin")),
):
    return verify_service.set_rule(db, course_id, data.min_grade)


@router.post("/claims", response_model=ClaimResponse, status_code=status.HTTP_201_CREATED)
def submit_claim(
    data: ClaimRequest,
    db: Session = Depends(get_db),
    tutor: User = Depends(require_role("tutor")),
):
    return verify_service.submit_claim(db, tutor, data.course_id, data.claimed_grade)


@router.get("/my-claims", response_model=list[ClaimResponse])
def my_claims(
    db: Session = Depends(get_db),
    tutor: User = Depends(require_role("tutor")),
):
    return verify_service.list_claims(db, tutor_id=tutor.id)


@router.get("/claims", response_model=list[ClaimResponse])
def all_claims(
    status: Literal["pending", "approved", "rejected"] | None = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role("admin")),
):
    return verify_service.list_claims(db, status=status)


@router.patch("/claims/{claim_id}", response_model=ClaimResponse)
def review_claim(
    claim_id: int,
    data: ReviewRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role("admin")),
):
    return verify_service.review_claim(db, admin, claim_id, data.status, data.reason)