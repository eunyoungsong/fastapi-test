# Query Parameters and String Validations
# 쿼리 매겨변수 및 문자열 유효성 검사 : 정규 표현식 설정

from typing import Optional

from fastapi import FastAPI, Query  # Query 사용하여 문자열 유효성 검사 

app = FastAPI()


@app.get("/items/")
async def read_items(q: Optional[str] = Query(None, min_length=3, max_length=50, regex="^fixedquery$")): # q 값 필요한경우 fixedquery 만 가능
    results = {"items" : [{"item_id" : "Foo"}, {"item_id" : "Bar"}]}
    if q:
        results.update({"q": q})
    return results



# regex 정규 표현식 
# ^x : x 로 시작
# x$ : x 로 끝