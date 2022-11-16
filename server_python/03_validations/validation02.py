# Query Parameters and String Validations
# 쿼리 매겨변수 및 문자열 유효성 검사 : 문자길이 설정 


from typing import Optional         # 선택적 매겨변수 생성을 위해 

from fastapi import FastAPI, Query  # Query 사용하여 문자열 유효성 검사 

app = FastAPI()

@app.get("/items/")
async def read_items(q: Optional[str] = Query(None, min_length=3, max_length=50)) :  # q선택적이지만 제공될 때마다 길이가 3자 이상 50자를 초과하지 않도록 설정 
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        #results.update({"q": q})
        results["q"] = q
    return results


# 기본 값을 None 에서 Query(None) : 동일한 작용