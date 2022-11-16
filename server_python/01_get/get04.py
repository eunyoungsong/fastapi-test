# 경로 매개변수 : 사전정의 값 Enum(열거형)

from enum import Enum   # Enum import

from fastapi import FastAPI


# str 과 Enum을 상속하는 열거형 클래스 생성 
class ModelName(str, Enum) : 
    alexnet = "alexnet"
    resent = "resent"
    lenet = "lenet"


app = FastAPI()


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName) :    # ModelName 클래스를 사용하는 경로 매겨변수 생성
    # 열거형 클래스 멤버 비교하기
    # 1. 
    if model_name == ModelName.alexnet :
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    # 2. 실제 값으로 비교하기
    if model_name.value == "lenet" :
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}