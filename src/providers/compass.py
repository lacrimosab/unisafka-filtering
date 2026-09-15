from datetime import date
from src.models import Meal

from bs4 import BeautifulSoup
import requests


REAKTORI_URL = (
    "https://www.compass-group.fi/en/"
    "ravintolat-ja-ruokalistat/food--co/"
    "kaupungit/tampere/reaktori/"
)

COMPASS_DIET_LABELS = {
    "G": "Gluten-free",
    "L": "Lactose-free",
    "M": "Milk-free",
    "VL": "Low-lactose",
    "Veg": "Vegan",
}

def parse_compass_food(
    food_text: str,
) -> tuple[str, set[str]]:
    # rpartition here is partition from the right side
    name, separator, codes_text = food_text.rpartition(" (")

    if not separator or not codes_text.endswith(")"):
        return food_text.strip(), set()

    codes_text = codes_text.removesuffix(")")

    codes = {
        code.strip()
        for code in codes_text.split(",")
    }

    diets = {
        COMPASS_DIET_LABELS[code]
        for code in codes
        if code in COMPASS_DIET_LABELS
    }

    return name.strip(), diets

def fetch_reaktori_page() -> str:
    response = requests.get(
        REAKTORI_URL,
        timeout=10,
    )

    response.raise_for_status()

    return response.text

# foods in the format {"So Good": [("Minced meat sauce", {"Lactose-free", "Milk-free"})]}
def get_reaktori_foods(
        selected_date: date
    ) -> dict[str, list[tuple[str, set[str]]]]:

    html = fetch_reaktori_page()
    soup = BeautifulSoup(html, "html.parser")

    date_text = (
        f"{selected_date.day}."
        f"{selected_date.month}."
        f"{selected_date.year}"
    )

    selected_day_heading = None

    for heading in soup.find_all("h3"):
        heading_text = heading.get_text(" ", strip = True)

        if date_text in heading_text:
            selected_day_heading = heading
            break   

    if selected_day_heading is None:
        return {}

    foods_by_category = {}
    current_category = None

    elements = selected_day_heading.find_all_next(
        ["h3", "h4", "li"]
    )

    for element in elements:
        if element.name == "h3":
            break

        if element.name == "h4":
            current_category = element.get_text(" ", strip=True,)
            foods_by_category[current_category] = []
            continue

        if element.name == "li" and current_category is not None:
            food_text = element.get_text(" ", strip=True)
            food_name, diets = parse_compass_food(food_text)

            foods_by_category[current_category].append(
                (food_name, diets)
            )

    return foods_by_category

def get_reaktori_meals(
    selected_date: date,
) -> list[Meal]:
    foods_by_category = get_reaktori_foods(selected_date)

    meals = []

    for foods in foods_by_category.values():
        if not foods:
            continue

        food_names = [
            food_name
            for food_name, _ in foods
        ]

        shared_diets = foods[0][1].copy()

        for _, diets in foods[1:]:
            shared_diets.intersection_update(diets)

        meal_name = " and ".join(food_names)

        meal = Meal(
            restaurant="Reaktori",
            name=meal_name,
            diets=shared_diets,
        )

        meals.append(meal)

    return meals