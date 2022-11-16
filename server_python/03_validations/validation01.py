# Query Parameters and String Validations
# 쿼리 매겨변수 및 문자열 유효성 검사 : 선택사항 만들기 

from typing import Optional     # 선택적 매겨변수 생성을 위해 

from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")
async def read_items(q: Optional[str] = None):  # q 는 None 이므로 필수가 아닌 선택사항
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results