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

def test_gluten_free_filter_keeps_only_gluten_free_meals():
    gluten_free_meal = Meal(
        restaurant="sample restoran",
        name="Gluten-free curry",
        diets={"Gluten-free"},
    )

    regular_meal = Meal(
        restaurant="sample restoran",
        name="Regular pasta",
        diets={"Lactose-free"},
    )

    meals = [
        gluten_free_meal,
        regular_meal,
    ]

    result = filter_meals(
        meals=meals,
        gluten_free_only=True,
    )

    assert result == [gluten_free_meal]