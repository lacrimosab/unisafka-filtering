from datetime import date

from bs4 import BeautifulSoup
import requests


REAKTORI_URL = (
    "https://www.compass-group.fi/en/"
    "ravintolat-ja-ruokalistat/food--co/"
    "kaupungit/tampere/reaktori/"
)

def fetch_reaktori_page() -> str:
    response = requests.get(
        REAKTORI_URL,
        timeout=10,
    )

    response.raise_for_status()

    return response.text

def get_reaktori_meal_headings(selected_date: date) -> list[str]:
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
        return []

    meal_headings = []
    
    # h3 is day of the week, h4 is the meal category
    for heading in selected_day_heading.find_all_next(["h3", "h4"]):
        if heading.name == "h3":
            break

        meal_headings.append(heading.get_text(" ", strip = True))

    return meal_headings
