from datetime import date

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

def get_reaktori_foods(selected_date: date) -> list[str]:
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
            foods_by_category[current_category].append(food_text)

    return foods_by_category

