# Request data Example 선언 : Body 여러예제 사용하기  


from typing import Optional

from fastapi import FastAPI, Body   # Body 가져오기 
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    

@app.put("/items/{itme_id}")
async def update_item(
    *,
    item_id: int,
    item: Item = Body(
        ...,
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "name": "Bar",
                    "price": "35.4",
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results

'''
summary: 예제에 대한 간단한 설명입니다.
description: 마크다운 텍스트를 포함할 수 있는 긴 설명입니다.
value: 이것은 표시된 실제 예입니다(예: dict)
externalValue: 대체 value, 예제를 가리키는 URL. 이것은 value 처럼 많은 도구에서 지원되지 않을 수 있습니다.
'''