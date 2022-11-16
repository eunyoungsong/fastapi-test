# Security 02 : Get Current User
# 현재 유저 정보 가져오기 (실제로 돌아가는 코드가 아닌 중간이해를 돕기 위한 예제코드)

from typing import Optional

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer # OAuth2PasswordBearer : Bearer토큰을 사용하여 Password Flow과 함께 OAuth2를 사용
from pydantic import BaseModel

app = FastAPI()

# URL에 토큰 포함시키기 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 유저모델 생성하기
class User(BaseModel): 
    username : str
    email : Optional[str] = None
    full_name : Optional[str] = None
    disabled : Optional[bool] = None


def fake_decode_token(token):
    return User(
        username = token + "fakedecoded",
        email = "john@example.com",
        full_name = "John Doe",
    )


# 종속성(의존성) 생성하기
async def get_current_user(token: str = Depends(oauth2_scheme)):   # sub-dependencies : 이전에 생성한 것과 동일한 종속성을 갖게 됨. 
    user = fake_decode_token(token)
    return user


@app.get("/user/me")
async def read_user_me(current_user: User = Depends(get_current_user)): 
    return current_user