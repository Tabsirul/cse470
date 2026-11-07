from datetime import datetime, timedelta

from app.services.booking_rules import (
    booking_problem,
    can_cancel,
    seats_left,
    slots_overlap,
)

T = datetime(2026, 11, 10, 15, 0)  # a session start used in the tests
NOW = datetime(2026, 11, 9, 12, 0)


# ---------- slots_overlap ----------

def test_same_time_overlaps():
    assert slots_overlap(T, 60, T, 60) is True


def test_partial_overlap():
    assert slots_overlap(T, 60, T + timedelta(minutes=30), 60) is True


def test_one_inside_the_other():
    assert slots_overlap(T, 120, T + timedelta(minutes=30), 30) is True


def test_back_to_back_is_not_overlap():
    assert slots_overlap(T, 60, T + timedelta(minutes=60), 60) is False


def test_far_apart_is_not_overlap():
    assert slots_overlap(T, 60, T + timedelta(days=1), 60) is False


def test_overlap_works_in_either_order():
    later = T + timedelta(minutes=30)
    assert slots_overlap(later, 60, T, 60) is True


# ---------- seats_left ----------

def test_seats_left():
    assert seats_left(5, 2) == 3
    assert seats_left(1, 0) == 1


def test_seats_left_never_negative():
    assert seats_left(2, 5) == 0


# ---------- booking_problem ----------

def problem(**changes):
    base = dict(starts_at=T, now=NOW, capacity=3, booked=1, already_booked=False, has_clash=False)
    base.update(changes)
    return booking_problem(**base)


def test_no_problem_when_all_is_fine():
    assert problem() is None


def test_started_session_cannot_be_booked():
    assert problem(starts_at=NOW) == "Session already started"
    assert problem(starts_at=NOW - timedelta(hours=1)) == "Session already started"


def test_cannot_book_twice():
    assert problem(already_booked=True) == "You already booked this session"


def test_clash_is_refused():
    assert problem(has_clash=True) == "You have another session at this time"


def test_full_session_is_refused():
    assert problem(capacity=2, booked=2) == "Session is full"


def test_last_seat_can_be_booked():
    assert problem(capacity=2, booked=1) is None


def test_started_is_reported_before_full():
    assert problem(starts_at=NOW, capacity=1, booked=1) == "Session already started"


# ---------- can_cancel ----------

def test_cancel_allowed_with_time_left():
    assert can_cancel(T, T - timedelta(hours=3)) is True


def test_cancel_allowed_exactly_two_hours_before():
    assert can_cancel(T, T - timedelta(hours=2)) is True


def test_cancel_refused_too_late():
    assert can_cancel(T, T - timedelta(minutes=119)) is False


def test_cancel_refused_after_start():
    assert can_cancel(T, T + timedelta(minutes=5)) is False