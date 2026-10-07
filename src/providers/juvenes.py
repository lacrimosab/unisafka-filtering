import requests

JUVENES_URL = (
    "https://fi.jamix.cloud/apps/menuservice/"
    "rest/haku/menu/93077/6"
)

JUVENES_RESTAURANTS = {
    56: "Newton",
    110: "Newton",
    112: "Konehuone",
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