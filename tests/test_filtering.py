from src.filtering import filter_meals
from src.models import Meal

def test_vegan_filter_keeps_only_vegan_meals():
    vegan_meal = Meal(
        restaurant="sample restoran",
        name="Vegan curry",
        diets={"Vegan"},
    )

    non_vegan_meal = Meal(
        restaurant="sample restoran",
        name="Chicken curry",
        diets=set(),
    )

    meals = [
        vegan_meal,
        non_vegan_meal,
    ]

    result = filter_meals(
        meals=meals,
        vegan_only=True,
    )

    assert result == [vegan_meal]