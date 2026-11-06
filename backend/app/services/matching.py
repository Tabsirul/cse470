from dataclasses import dataclass

from app.services.grade_rules import grade_points

# How much each part counts in the final score. The three numbers add up to 1.
WEIGHTS = {"rating": 0.4, "grade": 0.3, "price": 0.3}

DEFAULT_PRICE_CEILING = 1000  # taka per hour, used when the student gives no budget
NEW_TUTOR_RATING = 3.0        # a tutor with no reviews counts as 3 stars out of 5
MAX_GRADE_POINTS = 4.0


@dataclass
class Candidate:
    tutor_id: int
    name: str
    hourly_rate: int       # taka per hour
    grade: str             # the tutor's approved grade in the course, like "A-"
    rating: float | None   # average review stars from 1 to 5, None if no reviews


def is_eligible(candidate: Candidate, max_rate: int | None = None, min_rating: float | None = None) -> bool:
    """Return False if the tutor breaks a limit the student set.

    A tutor over the budget is not eligible. A tutor below the lowest rating is not eligible.
    A tutor with no rating at all is not eligible when a lowest rating is set.
    Exactly equal to a limit is allowed.
    """
    if max_rate is not None and candidate.hourly_rate > max_rate:
        return False

    if min_rating is not None:
        if candidate.rating is None or candidate.rating < min_rating:
            return False

    return True


def match_score(candidate: Candidate, max_rate: int | None = None) -> float:
    """Return a score from 0 to 100, rounded to 1 decimal place.

    Turn each part into a number from 0 to 1:
      rating part = rating / 5            (use NEW_TUTOR_RATING when there is no rating)
      grade part  = grade points / MAX_GRADE_POINTS
      price part  = 1 - rate / ceiling    (ceiling is max_rate, or DEFAULT_PRICE_CEILING)
                    and never below 0
    Then add them with the WEIGHTS and multiply by 100.
    Raise ValueError if the grade letter is not valid.
    """
    ceiling = max_rate if max_rate is not None else DEFAULT_PRICE_CEILING

    rating = candidate.rating
    if rating is None:
        rating = NEW_TUTOR_RATING

    rating_score = rating / 5
    grade_score = grade_points(candidate.grade) / MAX_GRADE_POINTS
    price_score = max(0.0, 1 - candidate.hourly_rate / ceiling)

    total = (
        WEIGHTS["rating"] * rating_score
        + WEIGHTS["grade"] * grade_score
        + WEIGHTS["price"] * price_score
    )

    return round(total * 100, 1)


def rank_candidates(
    candidates: list[Candidate],
    max_rate: int | None = None,
    min_rating: float | None = None,
) -> list[tuple[Candidate, float]]:
    """Return (candidate, score) pairs for eligible tutors, best score first.

    If two scores are equal, the lower hourly rate comes first.
    If that is also equal, sort by name.
    """
    ranked = []

    for candidate in candidates:
        if is_eligible(candidate, max_rate, min_rating):
            score = match_score(candidate, max_rate)
            ranked.append((candidate, score))

    ranked.sort(key=lambda item: (-item[1], item[0].hourly_rate, item[0].name))

    return ranked