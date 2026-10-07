import logging
from datetime import date, timedelta
from time import monotonic

from requests import RequestException
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
from src.providers.juvenes import (
    fetch_juvenes_week,
    parse_juvenes_meals_for_date,
)

logger = logging.getLogger(__name__)

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

def _remove_expired_cache_entries() -> None:
    current_time = monotonic()

    cached_entries = list(_week_cache.items())

    for week_key, (cached_at, _) in cached_entries:
        cache_age = current_time - cached_at

        if cache_age >= CACHE_LIFETIME_SECONDS:
            _week_cache.pop(week_key, None)

def get_meals_for_week(
    week_start: date,
) -> MealsByDate:
    _remove_expired_cache_entries()
    
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

    providers_succeeded = True

    try:
        sodexo_data = fetch_sodexo_week()
    except RequestException:
        logger.exception("Could not download Sodexo menu")
        sodexo_data = None
        providers_succeeded = False

    try:
        reaktori_html = fetch_reaktori_page()
        reaktori_soup = parse_reaktori_page(reaktori_html)
    except RequestException:
        logger.exception("Could not download Reaktori menu")
        reaktori_soup = None
        providers_succeeded = False

    try:
        juvenes_data = fetch_juvenes_week()
    except RequestException:
        logger.exception("Could not download Juvenes menu")
        juvenes_data = None
        providers_succeeded = False


    current_week = date.today().isocalendar()
    meals_by_date: MealsByDate = {}

    for requested_date in week_dates:
        requested_week = requested_date.isocalendar()

        is_current_week = (
            requested_week.year,
            requested_week.week,
        ) == (
            current_week.year,
            current_week.week,
        )

        if sodexo_data is not None and is_current_week:
            hertsi_meals = parse_hertsi_meals_for_date(
                sodexo_data,
                requested_date,
            )
        else:
            hertsi_meals = []

        if reaktori_soup is not None:
            reaktori_meals = parse_reaktori_meals_for_date(
                reaktori_soup,
                requested_date,
            )
        else:
            reaktori_meals = []

        if juvenes_data is not None:
            juvenes_meals = parse_juvenes_meals_for_date(
                juvenes_data,
                requested_date,
            )
        else:
            juvenes_meals = []

        date_key = requested_date.isoformat()

        meals_by_date[date_key] = (
            hertsi_meals + 
            reaktori_meals +
            juvenes_meals
        )

    # caching only a complete successful week
    if providers_succeeded:
        _week_cache[week_key] = (
            monotonic(),
            copy_meals_by_date(meals_by_date),
        )

    return meals_by_date

