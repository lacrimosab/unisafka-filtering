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

JUVENES_DIET_LABELS = {
    "G": "Gluten-free",
    "L": "Lactose-free",
    "M": "Milk-free",
    "VEG": "Vegan",
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

def parse_juvenes_diets(
    raw_codes: str | None,
) -> set[str]:
    diets = set()

    for raw_code in (raw_codes or "").split(","):
        code = raw_code.strip()
        label = JUVENES_DIET_LABELS.get(code)

        if label is not None:
            diets.add(label)

    return diets