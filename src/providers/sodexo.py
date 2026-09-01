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
    print(next(iter(data["courses"].values())))

    meals = []
    for course in data["courses"].values():
        meal = Meal(
            restaurant="Hertsi",
            name=course["title_en"],
        )

        meals.append(meal)

    return meals