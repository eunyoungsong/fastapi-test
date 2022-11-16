# Handling Errors (오류처리)

from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items :
        raise HTTPException(status_code=404, detail="Item not found") # raise 에러발생시키기 
    return {"item": items[item_id]}