from fastapi import APIRouter
from sqlalchemy import select
from app.database import async_session_maker
from app.baskets.schemas import SBasketBase, SBasketOut
from app.baskets.models import Baskets as BasketsModel
from app.exceptions import (BasketCapacityExceededException, 
                            BasketNotFoundException, 
                            MushroomIsAlreadyInBasketException, 
                            MushroomNotFoundException, 
                            MushroomNotInBasketException)
from app.mushrooms.schemas import SMushroomOut
from app.mushrooms.models import Mushrooms as MushroomsModel
from sqlalchemy.orm import subqueryload


router = APIRouter(
    prefix="/baskets",
    tags=["Baskets"]
)


@router.post("/create_basket", response_model=SBasketBase)
async def create_mushroom(basket: SBasketBase):
    db_new_basket = BasketsModel(
        owner=basket.owner,
        capacity=basket.capacity,
    )
    async with async_session_maker() as session:
            session.add(db_new_basket)
            await session.commit()

    return db_new_basket


@router.post("/change_basket", response_model=SMushroomOut)
async def add_mushroom_to_basket(mushroom_id: int, basket_id:int):

    async with async_session_maker() as session:
    # Проверяем наличие гриба
        result = await session.execute(select(MushroomsModel).filter(MushroomsModel.id == mushroom_id))
        mushroom = result.scalar_one_or_none()
        if mushroom is None:
            raise MushroomNotFoundException
    #Проверяем наличие корзинки
        result =  await session.execute(
            select(BasketsModel)
            .filter(BasketsModel.id == basket_id)
            .options(subqueryload(BasketsModel.mushrooms))  # Загружаем грибы, связанные с корзиной
        )
        basket = result.scalar_one_or_none()
        if basket is None:
            raise BasketNotFoundException
        if mushroom.basket_id == basket.id:
            raise MushroomIsAlreadyInBasketException
    # Проверяем, что вес гриба не превышает вместимость корзинки
        total_weight = sum(m.weight for m in basket.mushrooms) + mushroom.weight
        if total_weight > basket.capacity:
            raise BasketCapacityExceededException
    # Связываем гриб с корзинкой
        mushroom.basket_id = basket_id
        session.add(mushroom)
        await session.commit()

    return mushroom


@router.delete("/remove_mushroom", response_model=str)
async def remove_mushroom_from_basket(mushroom_id: int, basket_id: int):
    async with async_session_maker() as session:
        # Проверяем наличие гриба
        result = await session.execute(select(MushroomsModel).filter(MushroomsModel.id == mushroom_id))
        mushroom = result.scalar_one_or_none()
        if mushroom is None:
            raise MushroomNotFoundException()
        # Проверяем наличие корзинки
        result = await session.execute(select(BasketsModel).filter(BasketsModel.id == basket_id))
        basket = result.scalar_one_or_none()
        if basket is None:
            raise BasketNotFoundException()
        # Проверяем, что гриб действительно находится в корзине
        if mushroom.basket_id != basket_id:
            raise MushroomNotInBasketException
        # Убираем гриб из корзины
        mushroom.basket_id = None
        session.add(mushroom)
        await session.commit()

        return f"Mushroom {mushroom_id} removed from basket {basket_id}"
    

@router.get("/get_basket", response_model=SBasketOut)
async def get_basket(basket_id: int):
    async with async_session_maker() as session:
        result = await session.execute(
            select(BasketsModel)
            .filter(BasketsModel.id == basket_id)
            .options(subqueryload(BasketsModel.mushrooms))
        )
        basket = result.scalar_one_or_none()
        if basket is None:
            raise BasketNotFoundException()
        return basket
                                       