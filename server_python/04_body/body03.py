# Body : Body 특이값 

from typing import Optional

from fastapi import Body, FastAPI
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
async def update_item(
    item_id: int, item: Item, user: User, importance: int = Body(...)  # body에 importance 추가 
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


# 이전 모델을 확장하여 body에 다른키를 갖도록 설정할 수 있음
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
    },
    "importance": 5    # importance가 추가된것을 확인할 수 있다.
}
'''