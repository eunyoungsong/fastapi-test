# 쿼리 매개변수 

from fastapi import FastAPI

app = FastAPI()

# List 생성 
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):  # 기본값설정, 타입설정 안할시 문자열
    return fake_items_db[skip : skip + limit]


# URL : http://127.0.0.1:8000/items/?skip=0&limit=10
# ? 후에 쿼리가 나오고 & 로 키-값쌍을 구분합니다. 