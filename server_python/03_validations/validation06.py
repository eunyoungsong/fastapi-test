# Query Parameters and String Validations
# 쿼리변수 여러개 받기 

from typing import List, Optional   # List 사용

from fastapi import FastAPI, Query  # Query 사용


app = FastAPI()


@app.get("/items/")
async def read_items(q: Optional[List[str]] = Query(None)):
    query_items = {"q": q}
    return query_items