from datetime import date, timedelta
from time import monotonic

from src.models import Meal
from src.providers.compass import (
    fetch_reaktori_page,
    parse_reaktori_meals_for_date,
    parse_reaktori_page,
)
from src.providers.sodexo import (
    fetch_sodexo_week,
    parse_hertsi_meals_for_date,
)


CACHE_LIFETIME_SECONDS = 10 * 60

MealsByDate = dict[str, list[Meal]]

_week_cache: dict[
    str,
    tuple[float, MealsByDate],
] = {}

def copy_meals_by_date(
    meals_by_date: MealsByDate,
) -> MealsByDate:
    return {
        menu_date: meals.copy()
        for menu_date, meals in meals_by_date.items()
    } 

def get_meals_for_week(
    week_start: date,
) -> MealsByDate:
    week_key = week_start.isoformat()
    cached_entry = _week_cache.get(week_key)

    # caching saves time here because of the return
    # it doesn't have to download data from scratch
    if cached_entry is not None:
        cached_at, cached_meals_by_date = cached_entry
        cache_age = monotonic() - cached_at

        if cache_age < CACHE_LIFETIME_SECONDS:
            return copy_meals_by_date(
                cached_meals_by_date
            )

    week_dates = [
        week_start + timedelta(days=day_offset)
        for day_offset in range(6)
    ]

    sodexo_data = fetch_sodexo_week()

    reaktori_html = fetch_reaktori_page()
    reaktori_soup = parse_reaktori_page(reaktori_html)

    current_week = date.today().isocalendar()
    meals_by_date: MealsByDate = {}

    for requested_date in week_dates:
        requested_week = requested_date.isocalendar()

        if (
            requested_week.year,
            requested_week.week,
        ) == (
            current_week.year,
            current_week.week,
        ):
            hertsi_meals = parse_hertsi_meals_for_date(
                sodexo_data,
                requested_date,
            )
        else:
            hertsi_meals = []

        reaktori_meals = parse_reaktori_meals_for_date(
            reaktori_soup,
            requested_date,
        )

        date_key = requested_date.isoformat()

        meals_by_date[date_key] = (
            hertsi_meals + reaktori_meals
        )

    _week_cache[week_key] = (
        monotonic(),
        copy_meals_by_date(meals_by_date),
    )

    return meals_by_date

def get_meals_for_date(
    selected_date: str,
) -> list[Meal]:
    requested_date = date.fromisoformat(selected_date)

    week_start = requested_date - timedelta(
        days=requested_date.weekday()
    )

    meals_by_date = get_meals_for_week(week_start)

    return meals_by_date.get(
        selected_date,
        [],
    ).copy()

