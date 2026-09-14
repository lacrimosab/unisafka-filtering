from bs4 import BeautifulSoup
import requests

REAKTORI_URL = (
    "https://www.compass-group.fi/"
    "ravintolat-ja-ruokalistat/foodco/"
    "kaupungit/tampere/reaktori/"
)

def fetch_reaktori_page() -> str:
    response = requests.get(
        REAKTORI_URL,
        timeout=10,
    )

    response.raise_for_status()

    return response.text

def reaktori_day_headings() -> list[str]:
    html = fetch_reaktori_page()
    soup = BeautifulSoup(html, "html.parser")
    headings = soup.find_all("h3")

    day_headings = []
    for heading in headings:
        text = heading.get_text(" ", strip=True)
        day_headings.append(text)

    return day_headings