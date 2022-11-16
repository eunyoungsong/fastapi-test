# Request data Example 선언 : Field 사용하여 추가정보 선언하기 


from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field   # Field 가져오기  

app = FastAPI()


class Item(BaseModel):
    name: str = Field(..., example="Foo")
    description: Optional[str] = Field(None, example="A vert nice Item")
    price: float = Field(..., example=35.4)
    tax: Optional[float] = Field(None, example=3.2)


@app.put("/items/{itme_id}")
async def update_item(item_id: int, item: Item):
    results = {"itme_id": item_id, "item": item}
    return results