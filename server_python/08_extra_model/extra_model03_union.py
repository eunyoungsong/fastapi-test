# Union or anyOf
# 모델의 형식을 선언하거나 response model의 output 값으로 여러 개의 형식을 내보내고 싶을 경우

from typing import Union        # union 가져오기 

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int


items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])  # Union(합집합) 사용하기, 더 구체적인 plane 을 먼저 정의
async def read_item(item_id: str):
    return items[item_id]