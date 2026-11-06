import pytest

from app.services.matching import Candidate, is_eligible, match_score, rank_candidates


def make(tutor_id=1, name="Tina", rate=400, grade="A", rating=4.0):
    return Candidate(tutor_id=tutor_id, name=name, hourly_rate=rate, grade=grade, rating=rating)


# ---------- is_eligible ----------

def test_eligible_without_filters():
    assert is_eligible(make()) is True


def test_budget_boundary():
    assert is_eligible(make(rate=500), max_rate=500) is True   # exactly the budget
    assert is_eligible(make(rate=501), max_rate=500) is False  # one taka over


def test_min_rating_boundary():
    assert is_eligible(make(rating=4.0), min_rating=4.0) is True   # exactly the minimum
    assert is_eligible(make(rating=3.9), min_rating=4.0) is False


def test_unrated_tutor_is_dropped_when_min_rating_is_set():
    assert is_eligible(make(rating=None), min_rating=3.0) is False


def test_unrated_tutor_is_allowed_without_min_rating():
    assert is_eligible(make(rating=None)) is True


# ---------- match_score ----------

def test_best_possible_score_is_100():
    assert match_score(make(rate=0, grade="A", rating=5.0)) == pytest.approx(100.0)


def test_worked_example():
    # rating 4.0 -> 0.8, grade B -> 3.0/4 = 0.75, rate 500 of budget 1000 -> 0.5
    # 0.4*0.8 + 0.3*0.75 + 0.3*0.5 = 0.695
    assert match_score(make(rate=500, grade="B", rating=4.0), max_rate=1000) == pytest.approx(69.5)


def test_unrated_tutor_counts_as_three_stars():
    # rating part 3.0/5 = 0.6, so 0.4*0.6 + 0.3*1 + 0.3*1 = 0.84
    assert match_score(make(rate=0, grade="A", rating=None)) == pytest.approx(84.0)


def test_default_price_ceiling_is_used_without_a_budget():
    # price part 1 - 250/1000 = 0.75, so 0.4*1 + 0.3*1 + 0.3*0.75 = 0.925
    assert match_score(make(rate=250, grade="A", rating=5.0)) == pytest.approx(92.5)


def test_price_part_never_goes_below_zero():
    assert match_score(make(rate=2000, grade="A", rating=5.0)) == pytest.approx(70.0)


def test_better_rating_scores_higher():
    assert match_score(make(rating=4.8)) > match_score(make(rating=3.5))


def test_cheaper_tutor_scores_higher():
    assert match_score(make(rate=300)) > match_score(make(rate=600))


def test_better_grade_scores_higher():
    assert match_score(make(grade="A")) > match_score(make(grade="B"))


def test_invalid_grade_raises():
    with pytest.raises(ValueError):
        match_score(make(grade="Q"))


# ---------- rank_candidates ----------

def test_rank_puts_best_score_first():
    weak = make(tutor_id=1, name="Weak", rate=900, grade="C", rating=3.0)
    best = make(tutor_id=2, name="Best", rate=200, grade="A", rating=4.9)
    middle = make(tutor_id=3, name="Middle", rate=500, grade="B", rating=4.0)
    ranked = rank_candidates([weak, best, middle])
    assert [c.name for c, _ in ranked] == ["Best", "Middle", "Weak"]


def test_rank_returns_the_score_with_each_candidate():
    ranked = rank_candidates([make()])
    candidate, score = ranked[0]
    assert score == match_score(candidate)


def test_rank_drops_tutors_who_fail_the_filters():
    cheap = make(tutor_id=1, name="Cheap", rate=300)
    pricey = make(tutor_id=2, name="Pricey", rate=800)
    ranked = rank_candidates([cheap, pricey], max_rate=500)
    assert [c.name for c, _ in ranked] == ["Cheap"]


def test_rank_tie_is_broken_by_name():
    zed = make(tutor_id=1, name="Zed")
    amy = make(tutor_id=2, name="Amy")
    ranked = rank_candidates([zed, amy])
    assert [c.name for c, _ in ranked] == ["Amy", "Zed"]


def test_rank_of_empty_list_is_empty():
    assert rank_candidates([]) == []