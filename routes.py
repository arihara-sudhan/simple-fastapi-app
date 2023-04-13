from fastapi import APIRouter, Request,HTTPException,Form
from fastapi.encoders import jsonable_encoder
from models import Animal,AnimalUpdate
from typing import List
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory='templates')

router = APIRouter()

@router.post("/")
def create_animal(request: Request):
    return templates.TemplateResponse('add.html',{'request':request})

@router.post("/add")
def created_animal(request: Request, name: str = Form(...),scientificname: str = Form(...)):
    animal = request
    new_animal = request.app.database["animals"].insert_one(animal) 
    return templates.TemplateResponse('added.html',{'request':request})

    """
    animal.name = name
    animal.scientificname = scientificname
    animal = jsonable_encoder(animal)
    new_animal = request.app.database["animals"].insert_one(animal)
    """
@router.get("/",response_model=List[Animal])
def get_animal(request: Request):
    animals = list(request.app.database["animals"].find())
    return templates.TemplateResponse('animals.html',{'request':request,'animals':animals})

@router.get("/{name}", response_model=Animal)
def find_book(name: str, request: Request):
    if (animal := request.app.database["animals"].find_one({"name": name})) is not None:
        return animal
    raise HTTPException(status_code=404, detail="Not found")


@router.put("/{name}", response_model=AnimalUpdate)
def update_animal(name: str, request: Request, animal: AnimalUpdate):
    animal = {k: v for k, v in animal.dict().items() if v is not None}
    if len(animal) >= 1:
        update_result = request.app.database["animals"].update_one(
            {"name": name}, {"$set": animal}
        )

@router.delete("/{name}")
def delete_animal(name: str, request: Request):
    delete_result = request.app.database["animals"].delete_one({"name": name})
    if delete_result.deleted_count == 1:
        return 'FINE'
    raise HTTPException(status_code=404, detail="Not found")
