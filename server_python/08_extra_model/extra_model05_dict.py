# 임의의 dict로 응답
'''
Pydantic 모델을 사용하지 않고
키와 값의 유형만 선언하는 일반 임의 사전을 사용하여 응답을 선언할 수도 있습니다.
이것은 유효한 필드/속성 이름(Pydantic 모델에 필요함)을 미리 모르는 경우에 유용합니다.
'''

from typing import Dict
from fastapi import FastAPI

app = FastAPI()

@app.get("/keyword-weights/", response_model=Dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}