# 쿼리 매겨변수 : 여러 경로/쿼리 매개변수 

from typing import Optional     # 선택적 매겨변수 생성을 위해 

from fastapi import FastAPI

app = FastAPI()


@app.get("users/{user_id}/items/{item_id}")  # 여러 경로 매개변수 동시 선언 가능, 순서 상관없음 
async def read_user_item(user_id: int, item_id: str, q: Optional[str] = None, short: bool = False): # 이름으로 감지
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item