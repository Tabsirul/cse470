from sqlalchemy.orm import Session
from app.models.dispute import Dispute
from app.models.booking import Booking
from app.schemas.issue import DisputeCreate
from app.services.errors import NotFoundError, ConflictError

def create_dispute(db: Session, dispute_in: DisputeCreate, user_id: int) -> Dispute:
    # 1. Check if the booking exists
    booking = db.get(Booking, dispute_in.booking_id)
    if not booking:
        raise NotFoundError(f"Booking {dispute_in.booking_id} not found")
    
    # Note: You may need to adjust 'student_id' depending on your Booking model's exact column name.
    # if user_id != booking.student_id:
    #    raise ValueError("You are not authorized to report this booking.")

    # 2. Check for duplicate open reports by this user for this booking
    existing_report = db.query(Dispute).filter_by(
        booking_id=dispute_in.booking_id,
        reporter_id=user_id,
        status="pending"
    ).first()

    if existing_report:
        raise ConflictError("You already have an open report for this booking.")

    # 3. Create the dispute
    new_dispute = Dispute(
        booking_id=dispute_in.booking_id,
        reporter_id=user_id,
        issue_type=dispute_in.issue_type,
        description=dispute_in.description
    )
    db.add(new_dispute)
    db.commit()
    db.refresh(new_dispute)
    return new_dispute

def get_my_reports(db: Session, user_id: int):
    return db.query(Dispute).filter(Dispute.reporter_id == user_id).all()