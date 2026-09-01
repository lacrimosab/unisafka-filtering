import requests

from src.models import Meal

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

        dietcodes = course.get("dietcodes") or ""
        additional_diet_info = course.get("additionalDietInfo") or {}
        allergen_text = additional_diet_info.get("allergens_en") or ""

        diets = set()
        for code in dietcodes.split(","):
            cleaned_code = code.strip()
            if cleaned_code:
                diets.add(cleaned_code)
                
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