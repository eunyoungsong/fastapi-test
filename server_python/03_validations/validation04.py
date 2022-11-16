# Query Parameters and String Validations
# 쿼리변수 기본값 설정하기 

from typing import Optional

from fastapi import FastAPI, Query 

app = FastAPI()


@app.get("/items/")
async def read_items(q: str = Query("fixedquery", min_length=3)): # 입력하지 않아도 fixedquery 기본값
    results = {"items" : [{"item_id" : "Foo"}, {"item_id" : "Bar"}]}
    if q:
        results.update({"q": q})
    return results