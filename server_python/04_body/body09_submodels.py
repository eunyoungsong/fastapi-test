# Body : 하위모델속성, 특수 유형 유효성 검사

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl  # HttpUrl : 문자열은 유효한 URL인지 확인하고 JSON 스키마/OpenAPI에 문서화

app = FastAPI()


# 이미지 모델 생성 
class Image(BaseModel):
    #url: str
    url: HttpUrl   # str 대신 HttpUrl 타입으로 선언 
    name: str


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: set[str] = []
    image: Optional[Image] = None  # 하위모델로 사용 가능


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

'''
하위모델 예상본문 
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}
'''