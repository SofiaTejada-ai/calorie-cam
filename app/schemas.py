from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    name: str
    calories: float
    grams: float

class Prediction(BaseModel):
    items: List[Item]
    total_calories: float
