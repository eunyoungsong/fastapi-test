# Body : Set
# set 을 사용하면 중복데이터가 포함된 요청을 수신하더라도 고유한 항목 집합으로 변환 가능

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: set[str] = set()  


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results