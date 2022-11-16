# Body : field 
# 추가 유효성 검사 가능 
# Qurey, Path 와 같은 방식으로 사용 

from typing import Optional

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field   # Field import 

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = Field(   # field 모델 사용하기 
        None, title="The description of the item", max_length=300
    )
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: Optional[float] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
