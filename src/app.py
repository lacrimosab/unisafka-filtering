from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from src.providers.sodexo import get_hertsi_meal

from datetime import date


app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request,
         menu_date: str | None = None,
         vegan_only: bool = False, ):

    selected_date = menu_date or date.today().isoformat()
    meals = get_hertsi_meal(selected_date)
    if vegan_only:
        vegan_meals = []

        for meal in meals:
            if "Vegan" in meal.diets:
                vegan_meals.append(meal)

        meals = vegan_meals

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"meals": meals,
                "selected_date": selected_date,
                "vegan_only": vegan_only, # added to keep checkbox even after page reload
        },
    )
