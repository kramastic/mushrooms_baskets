from typing import Optional
from pydantic import BaseModel, ConfigDict


class SMushroomBase(BaseModel):
    title: str
    eatable: bool
    weight: float
    freshness: int

    model_config = ConfigDict(from_attributes=True)


class SMushroomOut(SMushroomBase):
    id: int
    basket_id: Optional[int]


class SMushroomUpdate(BaseModel):
    title: Optional[str] = None
    eatable: Optional[bool] = None
    weight: Optional[int] = None
    freshness: Optional[int] = None
    basket_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class SAddMushroomToBasket(BaseModel):
    basket_id: int 

    model_config = ConfigDict(from_attributes=True)