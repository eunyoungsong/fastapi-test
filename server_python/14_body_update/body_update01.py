# Body update
# jsonable_encoder 를 사용하여 입력 데이터를 
# JSON 으로 저장할 수 있는 데이터로 변환 가능 

from typing import Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder   # jsonable_encoder 가져오기 
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name : Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float = 10.5
    tags: list[str] = []

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{itme_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.put("/items/{item_id}", response_model=Item)  # PUT 을 사용하여 업데이트 (기존데이터대체=덮어쓰기)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded
