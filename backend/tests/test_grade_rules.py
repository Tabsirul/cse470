import pytest

from app.services.grade_rules import decide_claim, grade_points, meets_requirement


def test_grade_points_known_letters():
    assert grade_points("A+") == 4.0
    assert grade_points("A") == 4.0
    assert grade_points("A-") == 3.7
    assert grade_points("D-") == 0.7
    assert grade_points("F") == 0.0


def test_grade_points_ignores_case_and_spaces():
    assert grade_points(" a- ") == 3.7
    assert grade_points(" a+ ") == 4.0


@pytest.mark.parametrize("bad", ["Z", "", "  "])
def test_grade_points_unknown_letter_raises(bad):
    with pytest.raises(ValueError):
        grade_points(bad)


@pytest.mark.parametrize(
    "claimed, minimum, expected",
    [
        ("A+", "A", True),
        ("A", "A+", False),
        ("A", "A-", True),
        ("A-", "A-", True),
        ("B+", "A-", False),
        ("B", "B+", False),
        ("D", "F", True),
        ("F", "D", False),
        ("D-", "F", True),
        ("F", "D-", False),
    ],
)
def test_meets_requirement(claimed, minimum, expected):
    assert meets_requirement(claimed, minimum) is expected


def test_decide_claim_approved():
    status, reason = decide_claim("A", "A-")
    assert status == "approved"
    assert reason


def test_decide_claim_approved_on_exact_boundary():
    status, _ = decide_claim("A-", "A-")
    assert status == "approved"


def test_decide_claim_rejected():
    status, reason = decide_claim("B", "A-")
    assert status == "rejected"
    assert reason


def test_decide_claim_without_rule_is_pending():
    status, reason = decide_claim("A", None)
    assert status == "pending"
    assert reason


def test_decide_claim_invalid_grade_raises():
    with pytest.raises(ValueError):
        decide_claim("Q", "A-")


def test_decide_claim_invalid_rule_raises():
    with pytest.raises(ValueError):
        decide_claim("A", "Q")
# Keep this list in order from best grade to worst grade. GRADE_RANK uses the order.
def test_grade_scale_is_listed_from_best_to_worst():
    points = list(GRADE_POINTS.values())
    assert points == sorted(points, reverse=True)