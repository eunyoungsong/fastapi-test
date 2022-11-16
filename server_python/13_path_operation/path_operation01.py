# 경로 작업 (Path Operation) 구성 

# 경로 작업 데코레이터에 파라미터를 전달하여
# 경로 작업에 대한 메타데이터를 쉽게 구성하고 추가 할 수 있다. 

# Response 상태 코드 

from typing import Optional

from fastapi import FastAPI, status     # status 가져오기 
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    name : str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: set[str] = set()


@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED) # 파라미터에 응답상태코드 넣기 
async def create_item(item: Item):
    return item