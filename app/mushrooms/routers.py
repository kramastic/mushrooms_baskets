from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from app.exceptions import MushroomNotFoundException
from app.mushrooms.models import Mushrooms as MushroomsModel
from app.mushrooms.schemas import SMushroomBase, SMushroomOut, SMushroomUpdate
from app.database import async_session_maker


router = APIRouter(
    prefix="/mushrooms",
    tags=["Mushrooms"]
)


@router.post("/create_mushroom/", response_model=SMushroomOut)
async def create_mushroom(mushroom: SMushroomBase):
    db_new_mushroom = MushroomsModel(
        title=mushroom.title,
        eatable=mushroom.eatable,
        weight=mushroom.weight,
        freshness=mushroom.freshness
    )
    async with async_session_maker() as session:
            session.add(db_new_mushroom)
            await session.commit()

    return db_new_mushroom

@router.put("/id_{mushroom_id}", response_model=SMushroomOut)
async def update_mushroom(old_mushroom_id: int, mushroom: SMushroomUpdate):
    async with async_session_maker() as session:
        old_mushroom = await session.execute(select(MushroomsModel).filter(MushroomsModel.id == old_mushroom_id))
        db_mushroom = old_mushroom.scalar_one_or_none()
        if not db_mushroom:
            raise MushroomNotFoundException
        if mushroom.title is not None:
            db_mushroom.title = mushroom.title
        if mushroom.eatable is not None:
            db_mushroom.eatable = mushroom.eatable
        if mushroom.weight is not None:
            db_mushroom.weight = mushroom.weight
        if mushroom.freshness is not None:
            db_mushroom.freshness = mushroom.freshness
        if mushroom.basket_id is not None:
            db_mushroom.basket_id = mushroom.basket_id
        session.add(db_mushroom)
        await session.commit()

        return db_mushroom


@router.get("/get_mushroom_{mushroom_id}", response_model=SMushroomOut)
async def get_mushroom_by_id(mushroom_id: int):
    async with async_session_maker() as session:
        old_mushroom = await session.execute(select(MushroomsModel).filter(MushroomsModel.id == mushroom_id))
        old_mushroom = old_mushroom.scalar_one_or_none()
        if not old_mushroom:
            raise MushroomNotFoundException
        
        return old_mushroom

