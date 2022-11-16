# Path Parameters and Numeric Validations (경로 매겨변수 및 숫자 검증)

from typing import Optional

from fastapi import FastAPI, Path, Query  # Path 를 사용하여 경로 매겨변수에 검증과 메타데이터를 같은 타입으로 선언

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(..., title="The ID of the item to get"),  # (...) : item_id 필수로 설정, title 메타데이터 선언 
    q: Optional[str] = Query(None, alias="item-query"),           # (None) 선택사항, alias 별칭
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results