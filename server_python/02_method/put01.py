# Request Body : 요청 + 경로 + 쿼리 매개변수 
# request body 와 path parameters 그리고 qurey parameters 를 동시에 선언할 수 있다. 

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app = FastAPI()


# 데이터 모델 내용 변경 (q 값이 존재하면 q 항목 추가하기)
@app.put("/items/{item_id}") 
async def create_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result