from datetime import date
from time import monotonic

from src.models import Meal
from src.providers.compass import get_reaktori_meals
from src.providers.sodexo import get_hertsi_meal

CACHE_LIFETIME_SECONDS = 10 * 60

_meal_cache: dict[str, tuple[float, list[Meal]]] = {}

def get_meals_for_date(
    selected_date: str,
) -> list[Meal]:
    cached_entry = _meal_cache.get(selected_date)

    if cached_entry is not None:
        cached_at, cached_meals = cached_entry
        cache_age = monotonic() - cached_at

        if cache_age < CACHE_LIFETIME_SECONDS:
            return cached_meals.copy()

    requested_date = date.fromisoformat(selected_date)

    hertsi_meals = get_hertsi_meal(selected_date)
    reaktori_meals = get_reaktori_meals(requested_date)

    all_meals = hertsi_meals + reaktori_meals

    _meal_cache[selected_date] = (
        monotonic(),
        all_meals.copy(),
    )

    return all_meals