
from datetime import datetime, timedelta

MIN_CANCEL_HOURS = 2


def slots_overlap(start_a: datetime, minutes_a: int, start_b: datetime, minutes_b: int) -> bool:
    """Check whether two sessions overlap."""

    end_a = start_a + timedelta(minutes=minutes_a)
    end_b = start_b + timedelta(minutes=minutes_b)

    if start_a < end_b and start_b < end_a:
        return True

    return False


def seats_left(capacity: int, booked: int) -> int:
    """Return the number of available seats."""

    return max(0, capacity - booked)


def booking_problem(
    starts_at: datetime,
    now: datetime,
    capacity: int,
    booked: int,
    already_booked: bool,
    has_clash: bool,
) -> str | None:
    """Check whether a student can book a session."""

    if starts_at <= now:
        return "Session already started"

    if already_booked:
        return "You already booked this session"

    if has_clash:
        return "You have another session at this time"

    if seats_left(capacity, booked) == 0:
        return "Session is full"

    return None


def can_cancel(starts_at: datetime, now: datetime) -> bool:
    """Check whether cancellation is allowed."""

    time_left = starts_at - now

    if time_left >= timedelta(hours=MIN_CANCEL_HOURS):
        return True

    return False
