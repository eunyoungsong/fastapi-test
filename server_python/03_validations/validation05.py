# Query Parameters and String Validations
# 쿼리변수 필수로 만들기 

from typing import Optional

from fastapi import FastAPI, Query  # Query 사용

app = FastAPI()


@app.get("/items/")
async def read_items(q: str = Query(..., min_length=3)):                # Qurey(...) : 필수로 설정 
    results = {"items" : [{"item_id" : "Foo"}, {"item_id" : "Bar"}]}
    if q:
        results.update({"q": q})
    return results  