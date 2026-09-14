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