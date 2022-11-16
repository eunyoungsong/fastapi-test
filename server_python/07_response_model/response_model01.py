# Response Model : 응답모델
'''
경로 작업 데코레이터의 매개변수 response_model 사용하여
응답 모델을 정의하고 특히 개인 데이터가 필터링되도록 합니다.
'''

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


@app.post("/user/", response_model=UserIn)     # response_model 사용하여 UserIn 클래스로 응답하게 데이터생성 
async def create_user(user: UserIn):
    return user