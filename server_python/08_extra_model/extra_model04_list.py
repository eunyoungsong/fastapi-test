# List of models : 목록만들기 

from fastapi import FastAPI
from pydantic import BaseModel

#from typing import List, Optional
# 3.9(3.6 이상) 이전의 Python 버전에서는 먼저 표준 Python typing모듈 에서 List를 가져와야 함.


app = FastAPI()


class Item(BaseModel):
    name: str
    description: str


items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]


@app.get("/items/", response_model=list[Item])
async def read_items():
    return items
