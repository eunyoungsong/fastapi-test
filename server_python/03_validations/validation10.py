# Query Parameters and String Validations
# 매개변수 지원 중단 :
# 사용하는 클라이언트가 있기 때문에 잠시 그대로 두어야 하지만 문서에서 사용되지 않는 것으로 명확하게 표시하기를 원할 때

from typing import Optional

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(
    q: Optional[str] = Query(
        None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,        # 매개변수 지원 중단 : deprecated=True 를 설정해준다. 
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results