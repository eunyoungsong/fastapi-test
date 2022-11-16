# Body : Multiple body parameters

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):    # Item, User 두개의 body 매겨변수 선언
    results = {"item_id": item_id, "item": item, "user": user}
    return results


# FastAPI 는 함수에 둘 이상의 본문 매개변수(Pydantic 모델인 두 개의 매개변수)가 있음을 알아차립니다.
'''
BODY
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
'''