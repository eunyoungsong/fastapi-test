# Query Parameters and String Validations
# OpenAPI에서 제외 : include_in_schema 설정

from typing import Optional

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(
    hidden_query: Optional[str] = Query(None, include_in_schema=False)   # OpenAPI에서 제외
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}