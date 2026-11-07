from datetime import datetime, timedelta

import pytest

from app.services.payment_rules import next_status, payment_problem, split_payment

NOW = datetime(2026, 11, 9, 12, 0)
LATER = NOW + timedelta(days=1)


# ---------- split_payment ----------

def test_split_450():
    assert split_payment(450) == (405, 45)


def test_split_100():
    assert split_payment(100) == (90, 10)


def test_fee_rounds_half_up():
    assert split_payment(305) == (274, 31)  # fee 30.5 -> 31
    assert split_payment(5) == (4, 1)       # fee 0.5 -> 1


def test_fee_rounds_down_below_half():
    assert split_payment(4) == (4, 0)       # fee 0.4 -> 0
    assert split_payment(1) == (1, 0)


def test_split_always_adds_up():
    for amount in range(1, 2001):
        tutor, fee = split_payment(amount)
        assert tutor + fee == amount
        assert tutor >= 0 and fee >= 0


def test_split_returns_whole_numbers():
    tutor, fee = split_payment(333)
    assert isinstance(tutor, int) and isinstance(fee, int)


def test_split_rejects_zero_and_negative():
    with pytest.raises(ValueError):
        split_payment(0)
    with pytest.raises(ValueError):
        split_payment(-50)


# ---------- next_status ----------

def test_held_can_be_released():
    assert next_status("held", "release") == "released"


def test_held_can_be_refunded():
    assert next_status("held", "refund") == "refunded"


@pytest.mark.parametrize(
    "current, action",
    [
        ("released", "refund"),   # tutor already got the money
        ("released", "release"),  # cannot pay the tutor twice
        ("refunded", "release"),
        ("refunded", "refund"),   # cannot refund twice
        ("held", "explode"),      # unknown action
    ],
)
def test_other_moves_are_refused(current, action):
    with pytest.raises(ValueError):
        next_status(current, action)


def test_error_message_names_the_move():
    with pytest.raises(ValueError, match="Cannot refund a payment that is released"):
        next_status("released", "refund")


# ---------- payment_problem ----------

def problem(**changes):
    base = dict(
        booking_status="booked", slot_status="open", starts_at=LATER, now=NOW, already_paid=False
    )
    base.update(changes)
    return payment_problem(**base)


def test_no_problem_when_all_is_fine():
    assert problem() is None


def test_cancelled_booking_cannot_be_paid():
    assert problem(booking_status="cancelled") == "This booking is cancelled"


def test_closed_session_cannot_be_paid():
    assert problem(slot_status="cancelled") == "This session is not open"
    assert problem(slot_status="completed") == "This session is not open"


def test_started_session_cannot_be_paid():
    assert problem(starts_at=NOW) == "Session already started"


def test_cannot_pay_twice():
    assert problem(already_paid=True) == "You already paid for this session"


def test_cancelled_is_reported_first():
    assert problem(booking_status="cancelled", slot_status="cancelled", already_paid=True) == (
        "This booking is cancelled"
    )


def test_started_is_reported_before_already_paid():
    assert problem(starts_at=NOW, already_paid=True) == "Session already started"