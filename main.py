from fastapi import FastAPI,Request
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as animal_router
import uvicorn

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

config = dotenv_values(".env")
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/template/{name}", response_class=HTMLResponse)
def read_item(request: Request,name: str):
    return templates.TemplateResponse("index.html", {"request":request,"name": name})

@app.get('/')
def index():
    return 'WELCOME'

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(animal_router, prefix="/animals")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)