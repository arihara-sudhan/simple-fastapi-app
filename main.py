import uvicorn
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as animal_router
from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

config = dotenv_values(".env")


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.mount('/static',StaticFiles(directory='static'),name='static')
templates = Jinja2Templates(directory='templates')

@app.get("/")
def read_main(req: Request):
    return templates.TemplateResponse('index.html',{'request':req})

app.include_router(animal_router, prefix="/animals")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)


