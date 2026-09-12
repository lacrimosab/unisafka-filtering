from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.providers.sodexo import get_hertsi_meal

from datetime import date

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request,
        menu_date: str | None = None):

    selected_date = menu_date or date.today().isoformat()
    meals = get_hertsi_meal(selected_date)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"meals": meals,
                "selected_date": selected_date
        },
    )
