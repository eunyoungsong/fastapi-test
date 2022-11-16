# Body : 
# 예상본문 최상위 값이 JSON array(Python list)인 경우 
# Pydantic 모델에서와 같이 함수의 매개변수에서 유형 선언 가능 


from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):  # 요렇게! 
    return images
