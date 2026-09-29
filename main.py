from database import Base, engine
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import models

# Crear las tablas en la base de datos automáticamente
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Control e Incidencias - Lab B")

# Montar estáticos y motor de plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
  return templates.TemplateResponse("base.html", {"request": request})