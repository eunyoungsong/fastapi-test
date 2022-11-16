# Response Model : 응답 출력 따로 

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None
    
class UserOut(BaseModel):
    username : str
    email : EmailStr
    full_name : Optional[str] = None



@app.post("/user/", response_model=UserOut) # 출력은 UserOut 으로 응답 (password가 제외됨)
async def create_user(user: UserIn): # 입력은 UserIn 클래스로  
    return user