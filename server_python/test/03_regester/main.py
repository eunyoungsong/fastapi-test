from datetime import datetime, timedelta
from typing import Optional
from urllib import response
from urllib.request import Request
import json

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext  # Passlib : 많은 보안 해싱 알고리즘 및 유틸리티를 지원 / CryptContext : 암호를 해시하고 확인하는데 사용
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response

from encrypt_user import encrypt_user
#import join_user

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "50ca06cf961b580f582ef725980b935ea20f0ced1c0c6b0f8c6ced69f746dd09"  # 위 명령어를 통해 보안키 생성 후 복붙하기 
ALGORITHM = "HS256" # JWT 토큰에 서명하는 데 사용되는 알고리즘으로 HS256 으로 설정 
ACCESS_TOKEN_EXPIRE_MINUTES = 30    # 토큰 만료기간 30 으로 설정


# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": False,
#     }
# }


# 응답에 대한 토큰 Endpoint 에 사용한 Pydantic 모델 정의 
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class CreatUser(BaseModel):
    username: str
    password: str


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


class UsernameOldNewPassword(BaseModel):
    username: str
    old_password: str
    new_password: str


class UserDB(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")   

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


# 수신된 비밀번호가 저장된 해시와 일치하는지 확인
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def read_user_db():
    with open('./user_db.json') as json_file:
        return json.load(json_file)


# 사용자로부터 오는 암호를 해시 
def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


# 사용자를 인증하고 반환
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# 새 액세스 토큰을 생성
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 종속성 업데이트 : 이전과 동일한 토큰을 받도록 업데이트 (다른점은 JWT 토큰을 사용한다는 것)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # HTTP 오류 정의 
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # 토큰이 유효하지 않으면 즉시 HTTP 오류 반환
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # 받은 토큰을 복호화
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)   
    except JWTError:
        raise credentials_exception
    user_db = read_user_db()
    user = get_user(user_db, username=token_data.username)    
    if user is None:
        raise credentials_exception
    return user # 현재 사용자를 변환


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



# ---------------------------------------------------------------------------------------
#
#
# 사용자 등록
@app.post("/creat/user")
async def creat_user(form_data: CreatUser):
    encrypt_user(form_data.username, form_data.password, form_data.password)
    return encrypt_user


# 로그인
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    users_db = read_user_db()
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # timedelta으로 토큰 만료시간을 생성 
    access_token = create_access_token(                                   # 실제 JWT 액세스 토큰을 생성 및 반환 
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



# 로그인 확인
@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


# 사용자 정보 변경
@app.put("/users/update_db", response_model=User)
async def patch_user(form_data: UserDB, current_user: User = Depends(get_current_active_user)):
    return encrypt_user(current_user.username, None, None, form_data.email, form_data.full_name)


# 사용자 비밀번호 변경
@app.put("/users/update_password", response_model=Token)
async def patch_user_password(request: Request, form_data: UsernameOldNewPassword):
    users_db = read_user_db()
    user = authenticate_user(users_db, form_data.username, form_data.old_password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},            
        )

    encrypt_user(form_data.username, form_data.new_password, form_data.new_password)

    users_db = read_user_db()
    user = authenticate_user(users_db, form_data.username, form_data.new_password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},            
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
