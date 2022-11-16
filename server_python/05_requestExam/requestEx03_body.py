# Request data Example 선언 : Body 사용하여 추가 정보 선언하기 


from typing import Optional

from fastapi import FastAPI, Body   # Body 가져오기 
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    

@app.put("/items/{itme_id}")
async def update_item(
    item_id: int,
    item: Item = Body(
        ...,
        example={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
        },
    ),
):
    results = {"itme_id": item_id, "item": item}
    return results