from datetime import date
import requests

from src.models import Meal

SODEXO_URL = (
    "https://www.sodexo.fi/"
    "ruokalistat/output/weekly_json/111"
)

SODEXO_DIET_LABELS = {
    "G": "Gluten-free",
    "L": "Lactose-free",
    "M": "Milk-free",
    "VL": "Low-lactose",
}

FINNISH_WEEKDAYS = [
    "Maanantai",
    "Tiistai",
    "Keskiviikko",
    "Torstai",
    "Perjantai",
    "Lauantai",
    "Sunnuntai",
]

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

def fetch_sodexo_week() -> dict:
    response = requests.get(
        SODEXO_URL,
        timeout=10
    )
    response.raise_for_status()
    response.encoding = "utf-8"

    return response.json()

def parse_hertsi_meals_for_date(
    data: dict,
    requested_date: date,
) -> list[Meal]:
    weekday_name = FINNISH_WEEKDAYS[
        requested_date.weekday()
    ]

    selected_day = None

    for meal_date in data.get("mealdates") or []:
        if meal_date.get("date") == weekday_name:
            selected_day = meal_date
            break

    if selected_day is None:
        return []

    courses = selected_day.get("courses")

    if not courses:
        return []

    meals = []

    for course in courses.values():
        additional_diet_info = (
            course.get("additionalDietInfo") or {}
        )
        allergen_text = (
            additional_diet_info.get("allergens_en") or ""
        )
        diets = parse_sodexo_diets(course)
        student_price = parse_sodexo_student_price(course)

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
            allergen_details_available=bool(allergens),
            price=student_price,
        )

        meals.append(meal)

    return meals

    
def parse_sodexo_student_price(
    course: dict,
) -> float | None:
    raw_price = course.get("price") or ""

    if not raw_price:
        return None

    student_price = raw_price.split("/")[0]

    number_text = (
        student_price
        .replace("€", "")
        .strip()
        .replace(",", ".")
    )

    try:
        return float(number_text)
    except ValueError:
        return None

def get_hertsi_meal(
    selected_date: str,
) -> list[Meal]:
    requested_date = date.fromisoformat(selected_date)
    current_date = date.today()

    request_week = requested_date.isocalendar()
    current_week = current_date.isocalendar()

    if (
        request_week.year,
        request_week.week
    ) != (
        current_week.year,
        current_week.week,
    ):
        return []

    data = fetch_sodexo_week()

    return parse_hertsi_meals_for_date(
        data,
        requested_date,
    )