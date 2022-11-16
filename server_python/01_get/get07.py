# 쿼리 매겨변수 : 선택적 매개변수 

from typing import Optional     # 선택적 매겨변수 생성을 위해 

from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None): # None 으로 설정하면 선택사항 
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}