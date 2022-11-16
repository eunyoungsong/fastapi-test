# Security 04 : JWT(JSON Web Tokens)
# JWT 토큰과 보안 암호 해싱을 사용하여 애플리케이션을 실제로 안전하게 만들겠습니다.
# 이 코드는 실제로 애플리케이션에서 사용할 수 있는 코드이며 데이터베이스에 비밀번호 해시를 저장하는 등의 작업을 수행할 수 있습니다.


from datetime import datetime, timedelta
from typing import Optional
from urllib import response


from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext  # Passlib : 많은 보안 해싱 알고리즘 및 유틸리티를 지원 / CryptContext : 암호를 해시하고 확인하는데 사용
from pydantic import BaseModel


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "50ca06cf961b580f582ef725980b935ea20f0ced1c0c6b0f8c6ced69f746dd09"  # 위 명령어를 통해 보안키 생성 후 복붙하기 
ALGORITHM = "HS256" # JWT 토큰에 서명하는 데 사용되는 알고리즘으로 HS256 으로 설정 
ACCESS_TOKEN_EXPIRE_MINUTES = 30    # 토큰 만료기간 30 으로 설정


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


# 응답에 대한 토큰 Endpoint 에 사용한 Pydantic 모델 정의 
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")   

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


# 수신된 비밀번호가 저장된 해시와 일치하는지 확인
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


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
    user = get_user(fake_users_db, username=token_data.username)    
    if user is None:
        raise credentials_exception
    return user # 현재 사용자를 변환


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



# Update the "/token" path operation 
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
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



# 인증 GET
@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


# POST/PUT 을 위한 클래스
class Item(BaseModel):              
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


# 인증 POST 
@app.post("/items/")
async def create_item(item: Item, current_user: User = Depends(get_current_active_user)):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# 인증 PUT 
@app.put("/items/{item_id}") 
async def create_item(item_id: int, item: Item, q: Optional[str] = None, current_user: User = Depends(get_current_active_user)):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

