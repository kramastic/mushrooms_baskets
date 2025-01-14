from typing import List
from pydantic import BaseModel, ConfigDict
from app.mushrooms.schemas import SMushroomOut


class SBasketBase(BaseModel):
    owner: str
    capacity: float

    model_config = ConfigDict(from_attributes=True)


class SBasketOut(SBasketBase):
    id: int
    mushrooms: List[SMushroomOut] = []


