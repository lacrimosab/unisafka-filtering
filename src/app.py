from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import date, timedelta
from src.menu_service import get_meals_for_week
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

    week_start = requested_date - timedelta(days=requested_date.weekday())
    week_dates = [
        week_start + timedelta(days=day_offset)
        for day_offset in range(6)
    ]

    meals_by_date = get_meals_for_week(week_start)

    all_meals = meals_by_date.get(
        selected_date,
        [],
    ).copy()

    visible_meals = filter_meals(
        meals=all_meals,
        vegan_only=vegan_only,
        gluten_free_only=gluten_free_only,
        lactose_free_only=lactose_free_only,
    )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "meals": all_meals,
            "meals_by_date": meals_by_date,
            "visible_meals": visible_meals,
            "selected_date": selected_date,
            "week_dates": week_dates,
            "vegan_only": vegan_only, # added to keep checkbox even after page reload
            "gluten_free_only": gluten_free_only,
            "lactose_free_only": lactose_free_only,
        },
    )
