import uvicorn
from fastapi import FastAPI
from app.baskets.routers import router as baskets_routers
from app.mushrooms.routers import router as mushrooms_routers

app = FastAPI()

app.include_router(baskets_routers)
app.include_router(mushrooms_routers)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=9000, reload=True)
