# Body update
# PATCH 부분업데이트 + (exclude_unset 파라미터 사용하기)

from typing import List, Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.patch("/items/{item_id}", response_model=Item)   # PATCH 사용하여 부분 업데이트 하기 
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)     # exclude_unset 사용하기 
    updated_item = stored_item_model.copy(update=update_data) # .copy 사용해서 복사본 생성, 업데이트 할 데이터가 포함된 파라미터 전달
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item