# 경로 매겨변수 및 숫자 검증 : q 필수선언 버전  

from fastapi import FastAPI, Path 

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    q: str, item_id: int = Path(..., title="The ID of the item to get") # 파이썬 : 기본값없음 + 기본값있음 
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
