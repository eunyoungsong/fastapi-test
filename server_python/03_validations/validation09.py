# Query Parameters and String Validations
# 매개변수 별칭 만들기 : alias 사용 

from typing import Optional

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(q: Optional[str] = Query(None, alias="item-query")):    # item-query 라는 별칭 설정
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 예시) http://127.0.0.1:8000/items/?item-query=foobaritems