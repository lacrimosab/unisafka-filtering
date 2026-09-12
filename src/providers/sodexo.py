import requests

from src.models import Meal

SODEXO_DIET_LABELS = {
    "G": "Gluten-free",
    "L": "Lactose-free",
    "M": "Milk-free",
    "VL": "Low-lactose",
}

def parse_sodexo_diets(course: dict) -> set[str]:
    raw_codes = course.get("dietcodes") or ""
    diets = set()

    for raw_code in raw_codes.split(","):
        code = raw_code.strip()

        if not code:
            continue

        label = SODEXO_DIET_LABELS.get(code)

        if label:
            diets.add(label)

    category = course.get("category") or ""

    if "VEGAN" in category.upper():
        diets.add("Vegan")

    return diets

def get_hertsi_meal(date: str) -> list[Meal]:
    url = (
        "https://www.sodexo.fi/"
        f"ruokalistat/output/daily_json/111/{date}"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    meals = []
    for course in data["courses"].values():

        additional_diet_info = course.get("additionalDietInfo") or {}
        allergen_text = additional_diet_info.get("allergens_en") or ""
        diets = parse_sodexo_diets(course)
                
        allergens = set()
        for allergen in allergen_text.split(","):
            cleaned_allergen = allergen.strip()
            if cleaned_allergen:
                allergens.add(cleaned_allergen)

        meal = Meal(
            restaurant="Hertsi",
            name=course["title_en"],
            diets=diets,
            allergens=allergens,
        )

        meals.append(meal)

    return meals
