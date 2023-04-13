from typing import Optional
from pydantic import BaseModel

class Animal(BaseModel):
    name: str
    scientificname: str


class AnimalUpdate(BaseModel):
    name: str
    scientificname: str