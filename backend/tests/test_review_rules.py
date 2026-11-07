import pytest

from app.services.review_rules import average_rating, review_problem, star_counts


# ---------- average_rating ----------

def test_no_ratings_gives_none():
    assert average_rating([]) is None


def test_single_rating():
    assert average_rating([4]) == 4.0


def test_simple_average():
    assert average_rating([5, 4]) == 4.5


def test_average_rounds_down_below_half():
    assert average_rating([5, 4, 4]) == 4.3  # 4.333...


def test_average_rounds_up_above_half():
    assert average_rating([5, 5, 4]) == 4.7  # 4.666...


def test_average_rounds_half_up_not_to_even():
    # 4.25 must become 4.3. Python's round(4.25, 1) gives 4.2, which is the trap.
    assert average_rating([4, 4, 4, 5]) == 4.3
    assert average_rating([2, 2, 2, 3]) == 2.3  # 2.25 -> 2.3


def test_average_of_all_same():
    assert average_rating([3, 3, 3]) == 3.0


def test_average_is_a_float():
    assert isinstance(average_rating([5, 5]), float)


# ---------- star_counts ----------

def test_star_counts_example():
    assert star_counts([5, 5, 3]) == {5: 2, 4: 0, 3: 1, 2: 0, 1: 0}


def test_star_counts_empty_has_all_keys():
    assert star_counts([]) == {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}


def test_star_counts_keys_go_from_five_down_to_one():
    assert list(star_counts([1, 2, 3])) == [5, 4, 3, 2, 1]


# ---------- review_problem ----------

def problem(**changes):
    base = dict(
        booking_status="booked",
        slot_status="completed",
        payment_status="released",
        already_reviewed=False,
    )
    base.update(changes)
    return review_problem(**base)


def test_no_problem_when_all_is_fine():
    assert problem() is None


def test_cancelled_booking_cannot_review():
    assert problem(booking_status="cancelled") == "This booking was cancelled"


@pytest.mark.parametrize("slot_status", ["open", "cancelled"])
def test_session_must_be_completed(slot_status):
    assert problem(slot_status=slot_status) == "You can review after the session is completed"


@pytest.mark.parametrize("payment_status", [None, "held", "refunded"])
def test_only_paid_students_can_review(payment_status):
    assert problem(payment_status=payment_status) == "Only students who paid can review"


def test_cannot_review_twice():
    assert problem(already_reviewed=True) == "You already reviewed this session"


def test_cancelled_is_reported_first():
    assert problem(
        booking_status="cancelled", slot_status="open", payment_status=None, already_reviewed=True
    ) == "This booking was cancelled"


def test_not_completed_is_reported_before_unpaid():
    assert problem(slot_status="open", payment_status=None) == (
        "You can review after the session is completed"
    )


def test_unpaid_is_reported_before_already_reviewed():
    assert problem(payment_status="held", already_reviewed=True) == "Only students who paid can review"