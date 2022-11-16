# 경로 매겨변수 및 숫자 검증 : 숫자 검증 

from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
    q: str,
    size: float = Query(..., gt=0, lt=10.5)
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

'''
ge : 크거나(greater) 같은(equal) 정수형 숫자 
gt : 크거나(greater)
le : 작거나(less) 같은(equal)  
lt : 작거나(less)
'''