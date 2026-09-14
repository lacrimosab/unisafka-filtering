from src.models import Meal


def filter_meals(
    meals: list[Meal],
    vegan_only: bool = False,
    gluten_free_only: bool = False,
    lactose_free_only: bool = False,
) -> list[Meal]:
    matching_meals = []

    for meal in meals:
        if vegan_only and "Vegan" not in meal.diets:
            continue

        if gluten_free_only and "Gluten-free" not in meal.diets:
            continue

        if lactose_free_only and not (
            "Lactose-free" in meal.diets
            or "Milk-free" in meal.diets
        ):
            continue

        matching_meals.append(meal)

    return matching_meals