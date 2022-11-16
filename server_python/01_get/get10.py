# 쿼리 매겨변수 : 필수 쿼리 매개변수 

from typing import Optional     # 선택적 매겨변수 생성을 위해 

from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: Optional[int] = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item


# 필수 매개변수는 기본값을 설정할 수 없다.

# needy : 필수
# skip  : 기본 설정
# limit : 선택적