
def average_rating(ratings: list[int]) -> float | None:
    if len(ratings) == 0:
        return None

    count = len(ratings)
    tenths = (sum(ratings) * 20 + count) // (2 * count)

    return tenths / 10


def star_counts(ratings: list[int]) -> dict[int, int]:
    return {
        star: ratings.count(star)
        for star in (5, 4, 3, 2, 1)
    }


def review_problem(
    booking_status: str,
    slot_status: str,
    payment_status: str | None,
    already_reviewed: bool,
) -> str | None:
    if booking_status != "booked":
        return "This booking was cancelled"

    if slot_status != "completed":
        return "You can review after the session is completed"

    if payment_status != "released":
        return "Only students who paid can review"

    if already_reviewed:
        return "You already reviewed this session"

    return None
