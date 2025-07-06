from typing import List, Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    calories: float
    grams: float

class Prediction(BaseModel):
    items: List[Item]
    total_calories: float
    overlay_png: Optional[str]  # ← new field (base-64 string)
