from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Payment(Base):
    """Money a student paid for one booking. It is held until the session is done."""

    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id", ondelete="CASCADE"))
    amount: Mapped[int] = mapped_column()  # taka the student paid
    status: Mapped[str] = mapped_column(String(20), default="held")  # held / released / refunded
    method: Mapped[str] = mapped_column(String(20))  # bkash / nagad (sandbox)
    account_last4: Mapped[str] = mapped_column(String(4))  # we never store the full number
    reference: Mapped[str] = mapped_column(String(40))  # the gateway's transaction id
    refund_reference: Mapped[str | None] = mapped_column(String(40), nullable=True)
    tutor_amount: Mapped[int | None] = mapped_column(nullable=True)  # filled when released
    platform_fee: Mapped[int | None] = mapped_column(nullable=True)  # filled when released
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )