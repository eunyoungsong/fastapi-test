# Request Body  : 클라이언트가 API로 보낸 데이터
# Response Body : API가 클라이언트에 보내는 데이터

# 클라이언트 요청 
# Request Body 를 선언하려면 pydantic 모델을 사용합니다.
# 1. Request Body 를 JSON 으로 읽어옵니다.
# 2. (필요한 경우) 해당 유형을 변환합니다.
# 3. 데이터를 검증합니다.
# 4. item 매개변수에 수신된 데이터를 제공합니다.

from typing import Optional     # 선택적 매겨변수 생성을 위해 

from fastapi import FastAPI

# BaseModel 가져오기 
from pydantic import BaseModel      

# 데이터 모델 만들기 
class Item(BaseModel):              
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app = FastAPI()


# 데이터 모델 내용 변경 (price_with_tax 항목 추가)
@app.post("/items/")                            # POST : 데이터를 추가하기 위해 post 사용 
async def create_item(item: Item):              # 타입을 Item 클래스로 선언 : 매개변수에 수신된 데이터를 제공
    item_dict = item.dict()
    if item.tax: 
        price_with_tax = item.price + item.tax 
        item_dict.update({"price_with_tax": price_with_tax}) 
        # item_dict["price_with_tax"] = price_with_tax 
    return item_dict