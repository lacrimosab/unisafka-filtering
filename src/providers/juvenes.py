from datetime import date

import requests

from src.models import Meal

JUVENES_URL = (
    "https://fi.jamix.cloud/apps/menuservice/"
    "rest/haku/menu/93077/6"
)

JUVENES_RESTAURANTS = {
    56: "Newton",
    110: "Newton",
    112: "Konehuone",
}

JUVENES_DIET_LABELS = {
    "G": "Gluten-free",
    "L": "Lactose-free",
    "M": "Milk-free",
    "VEG": "Vegan",
}

def fetch_juvenes_week() -> list[dict]:
    response = requests.get(
        JUVENES_URL,
        params={
            "lang": "en",
            "type": "json",
        },
        timeout = 10,
    )

    response.raise_for_status()

    return response.json()

def parse_juvenes_diets(
    raw_codes: str | None,
) -> set[str]:
    diets = set()

    for raw_code in (raw_codes or "").split(","):
        code = raw_code.strip()
        label = JUVENES_DIET_LABELS.get(code)

        if label is not None:
            diets.add(label)

    return diets

def parse_juvenes_meal_option(
    meal_option: dict,
    restaurant: str,
) -> Meal | None:
    # converts one grouped meal option into one Meal object
    menu_items = [
        item 
        for item in meal_option.get("menuItems") or []
        if (item.get("name") or "").strip()
    ]

    if not menu_items:
        return None

    food_names = [
        item["name"].strip()
        for item in menu_items
    ]

    shared_diets = parse_juvenes_diets(
        menu_items[0].get("diets")
    )

    for item in menu_items[1:]:
        item_diets = parse_juvenes_diets(
            item.get("diets")
        )
        shared_diets.intersection_update(item_diets)

    return Meal(
        restaurant=restaurant,
        name=" and ".join(food_names),
        diets=shared_diets,
    )

def parse_juvenes_meals_for_date(
    data: list[dict],
    requested_date: date,
) -> list[Meal]:
    # navigates the Jamix hierarchy and find the correct 
    # restaurant and date
    date_number = int(requested_date.strftime("%Y%m%d"))
    meals = []

    for kitchen in data:
        for menu_type in kitchen.get("menuTypes") or []:
            restaurant = JUVENES_RESTAURANTS.get(
                menu_type.get("menuTypeId")
            )

            if restaurant is None:
                continue

            for menu in menu_type.get("menus") or []:
                for day in menu.get("days") or []:
                    if day.get("date") != date_number:
                        continue

                    for meal_option in day.get("mealoptions") or []:
                        meal = parse_juvenes_meal_option(
                            meal_option,
                            restaurant,
                        )

                        if meal is not None:
                            meals.append(meal)

    return meals
