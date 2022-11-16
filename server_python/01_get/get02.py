# 경로 매개변수(Prameters)

from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id):
#async def read_item(item_id: int):  # 경로 매개변수의 타입을 설정할 수 있음
    return {"item_id": item_id}

# 127.0.0.1:8000/items/5 실행 