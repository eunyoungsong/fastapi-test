# Extra Models : 추가모델 
'''
입력 모델 은 암호를 가질 수 있어야 합니다.
출력 모델 에는 암호가 없어야 합니다.
데이터베이스 모델 에는 해시된 암호가 있어야 합니다.
'''

from typing import Optional
from urllib import response

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: Optional[str] = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)    # **(kwargs)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def creat_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


# Python ----------------------------------------------------
# 파라미터를 몇개 받을지 모르는 경우 or 여러개의 파라미터를 받아야하는 경우
# *args     : args는 튜플 형태로 전달된다. 
# **kwargs  : 키-값의 딕셔너리 형태로 전달된다. 
#-------------------------------------------------------------

'''
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
user_dict = user_in.dict()
print(user_dict)

# {
#     'username': 'john',
#     'password': 'secret',
#     'email': 'john.doe@example.com',
#     'full_name': None,
# }

UserInDB(**user_dict)

# 결과
# UserInDB(
#     username="john",
#     password="secret",
#     email="john.doe@example.com",
#     full_name=None,
# )

# 더 정확하게는 
# UserInDB(
#     username = user_dict["username"],
#     password = user_dict["password"],
#     email = user_dict["email"],
#     full_name = user_dict["full_name"],
# )


'''