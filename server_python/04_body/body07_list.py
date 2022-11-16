# Body : List

from typing import Optional

#from typing import List, Optional
# 3.9(3.6 이상) 이전의 Python 버전에서는 먼저 표준 Python typing모듈 에서 List를 가져와야 함.

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    
    tags: list[str] = []
    #tags: List[str] = []   # 3.9이전 버전에서 


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
