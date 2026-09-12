from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.providers.sodexo import get_hertsi_meal

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    meals = get_hertsi_meal("2026-09-11")

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"meals": meals},
    )
