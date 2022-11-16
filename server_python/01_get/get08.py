# 쿼리 매겨변수 : 선택적 매개변수 

from typing import Optional     # 선택적 매겨변수 생성을 위해 

from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None, short: bool = False): # 형변환 가능, short 을 bool 형으로 선언 
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item