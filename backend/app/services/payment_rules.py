
from datetime import datetime

PLATFORM_FEE_PERCENT = 10

# Allowed payment status transitions
TRANSITIONS = {
    ("held", "release"): "released",
    ("held", "refund"): "refunded",
}


def split_payment(amount: int) -> tuple[int, int]:
    """Split a payment into tutor share and platform fee."""

    if amount <= 0:
        raise ValueError("Amount must be above 0")

    fee = (amount * PLATFORM_FEE_PERCENT + 50) // 100
    tutor_share = amount - fee

    return tutor_share, fee


def next_status(current: str, action: str) -> str:
    """Return the new payment status after an action."""

    key = (current, action)

    if key not in TRANSITIONS:
        raise ValueError(f"Cannot {action} a payment that is {current}")

    return TRANSITIONS[key]


def payment_problem(
    booking_status: str,
    slot_status: str,
    starts_at: datetime,
    now: datetime,
    already_paid: bool,
) -> str | None:
    """Check whether a booking can be paid."""

    if booking_status != "booked":
        return "This booking is cancelled"

    if slot_status != "open":
        return "This session is not open"

    if starts_at <= now:
        return "Session already started"

    if already_paid:
        return "You already paid for this session"

    return None
