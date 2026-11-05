
GRADE_POINTS = {
    "A+": 4.0,
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
    "C-": 1.7,
    "D+": 1.3,
    "D": 1.0,
    "D-": 0.7,
    "F": 0.0,
}

GRADE_RANK = {
    grade: rank
    for rank, grade in enumerate(GRADE_POINTS)
}


def grade_points(grade: str) -> float:
    grade = grade.strip().upper()

    if grade not in GRADE_POINTS:
        raise ValueError("Invalid grade letter")

    return GRADE_POINTS[grade]


def meets_requirement(claimed_grade: str, min_grade: str) -> bool:
    claimed_grade = claimed_grade.strip().upper()
    min_grade = min_grade.strip().upper()

    if claimed_grade not in GRADE_RANK or min_grade not in GRADE_RANK:
        raise ValueError("Invalid grade letter")

    return GRADE_RANK[claimed_grade] <= GRADE_RANK[min_grade]


def decide_claim(claimed_grade: str, min_grade: str | None) -> tuple[str, str]:
    grade_points(claimed_grade)

    if min_grade is None:
        return ("pending", "No minimum grade requirement has been set.")

    if meets_requirement(claimed_grade, min_grade):
        return ("approved", "The claimed grade meets the minimum requirement.")

    return ("rejected", "The claimed grade is below the minimum requirement.")