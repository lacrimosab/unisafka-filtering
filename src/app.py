from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import date
from src.providers.sodexo import get_hertsi_meal
from src.providers.compass import get_reaktori_meals
from src.filtering import filter_meals



app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    menu_date: str | None = None,
    vegan_only: bool = False,
    gluten_free_only: bool = False,
    lactose_free_only: bool = False,
):

    selected_date = menu_date or date.today().isoformat()
    requested_date = date.fromisoformat(selected_date)

    hertsi_meals = get_hertsi_meal(selected_date)
    reaktori_meals = get_reaktori_meals(requested_date)

    meals = hertsi_meals + reaktori_meals

    meals = filter_meals(
    meals=meals,
    vegan_only=vegan_only,
    gluten_free_only=gluten_free_only,
    lactose_free_only=lactose_free_only,
)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"meals": meals,
                "selected_date": selected_date,
                "vegan_only": vegan_only, # added to keep checkbox even after page reload
                "gluten_free_only": gluten_free_only,
                "lactose_free_only": lactose_free_only,
        },
    )
