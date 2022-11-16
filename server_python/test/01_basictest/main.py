from typing import Optional
from enum import Enum

from fastapi import FastAPI, Response, status
from pydantic import BaseModel 


# GET 열거형 테스트를 위한 모델 클래스
class ModelName(str, Enum) : 
    alexnet = "alexnet"
    resent = "resent"
    lenet = "lenet"


# POST 테스트를 위한 데이터 모델 클래스  
class Item(BaseModel):              
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app = FastAPI()


# GET 고정 경로 테스트 
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}



# GET 열거형 테스트 
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet :
        return {"model_name": model_name, "message": "alexnet"}
    if model_name.value == "lenet" :
        return {"model_name": model_name, "message": "lenet"}
    return {"model_name": model_name, "message": "resent"}


# POST 테스트 
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# PUT 테스트 
@app.put("/items/{item_id}") 
async def create_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


# DELETE 테스트 
@app.delete("/delete")
async def delete_item():
    delect_item = None;
    return Response(status_code=status.HTTP_204_NO_CONTENT)

