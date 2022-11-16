# Security 03 : Simple OAuth2 with Password and Bearer (비밀번호와 전달자가 있는 간단한 OAuth2)
# Password flow에서 유저는 반드시 username과 password를 보내야 한다.
# field 이름은 반드시 username과 password 이여야 한다.
# 데이터형태는 JSON데이터가 아닌 form 데이터로 보내져야 한다.

from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

fake_users_db = {
    "johndoe" : {
        "username" : "johndoe",
        "full_name" : "John Doe",
        "email" : "johndoe@example.com",
        "hashed_password" : "fakehashedsecret",
        "disabled" : False,
    },
    "alice" : {
        "username" : "alice",
        "full_name" : "Alice Wonderson",
        "email" : "alice@example.com",
        "hashed_password" : "fakehashedsecret2",
        "disabled" : False,
    }
}

app = FastAPI()


def fake_hash_password(password: str):
    return "fakehashed" + password


# URL에 토큰 포함시키기
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username : str
    email : Optional[str] = None
    full_name : Optional[str] = None
    disabled : Optional[bool] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


# 종속성 생성하기
async def get_current_user(token: str = Depends(oauth2_scheme)): 
    user = fake_decode_token(token)
    if not user : # 사용자가 존재하지 않으면 오류처리 
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid authentication credentials",
            headers = {"WWW-Authenticate" : "Bearer"},
        )
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):  # sub-dependencies
    if current_user.disabled:  # 활성 상태 확인
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return current_user



@app.post("/token/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):  # OAuth2PasswordRequestForm 의 종속성 사용 : username, password, grant_type(선택사항)
    # form 양식필드에 fake data 가져오기 
    user_dict = fake_users_db.get(form_data.username)
    # 해당 사용자가 없으면 오류처리 
    if not user_dict :
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # 패스워드 해싱
    user = UserInDB(**user_dict)                             # 먼저 해당 데이터를 UserInDB 모델에 넣기 
    hashed_password = fake_hash_password(form_data.password) # 일반 텍스트 암호를 저장해서는 안되므로 fake(가짜) 암호 해싱 시스템을 사용
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}  # JSON객체 토큰 반환 (토큰은 반드시 JSON객체 이여야하고 access_token과 token_type을 가져야 한다.)


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):   # 추가 종속성을 생성하여 종속성 업데이트 
    return current_user   # 현재 사용자 반환(사용자가 존재하고 올바르게 인증되었으며 활성 상태인 경우)