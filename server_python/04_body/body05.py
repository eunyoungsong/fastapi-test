# Body : 단일 body param

from typing import Optional

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)): # 특수 바디 매개변수 : embed
    results = {"item_id": item_id, "item": item}
    return results

'''
expect a BODY :
{
  "item_id": int,
  "item": {
    "name": "string",
    "description": "string",
    "price": 0,
    "tax": 0
  }
}

instead of:
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
'''