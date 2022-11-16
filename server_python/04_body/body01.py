# Body : Multiple Parameters

from typing import Optional

from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
    q: Optional[str] = None,
    item: Optional[Item] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

'''
BODY
{
  "item_id": 10,
  "q": "test",          # 경로변수 item_id, q 도 추가되었고
  "item": {             # item 모델도 추가되었다.
    "name": "string",
    "description": "string",
    "price": 0,
    "tax": 0
  }
}
'''