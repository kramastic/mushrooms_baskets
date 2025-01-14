from fastapi import HTTPException, status


class BaseException(HTTPException):
    status_code=500,
    detail=''

    def __init__(self):
        super().__init__(status_code=self.status_code,detail=self.detail)


class MushroomNotFoundException(BaseException):
    status_code=status.HTTP_404_NOT_FOUND
    detail='The mushroom is not found'

class BasketNotFoundException(BaseException):
    status_code=status.HTTP_404_NOT_FOUND
    detail='The basket is not found'

class BasketCapacityExceededException(BaseException):
    status_code=status.HTTP_404_NOT_FOUND
    detail='The basket capacity exceeded'

class MushroomNotInBasketException(BaseException):
    status_code=status.HTTP_404_NOT_FOUND
    detail='The mushroom is not in this basket'

class MushroomIsAlreadyInBasketException(BaseException):
    status_code=status.HTTP_404_NOT_FOUND
    detail='The mushroom is already in this basket'