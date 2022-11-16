# Request data Example 선언

# Pydantic 모델 내부에 예제를 추가하기
# 1. 해당 Pydantic 모델에 대한 JSON schema_extra 에 사용
# 2. Field(example="something")해당 예제가 추가


# 1. 해당 Pydantic 모델에 대한 JSON schema_extra 에 사용
# 예시일뿐 동작시 오류남ㅡㅡ 


from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "pice": 35.4,
                "tax": 3.2,
            }
        }


@app.put("/items/{itme_id}")
async def update_item(item_id: int, item: Item):
    results = {"itme_id": item_id, "item": item}
    return results