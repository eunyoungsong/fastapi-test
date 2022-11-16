# 경로 매개변수 : 고정경로

from fastapi import FastAPI

app = FastAPI()


@app.get("/users/me")     # 순서문제 : 고정경로 먼저 설정해줘야함 
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str): # 매개변수 string 타입
    return {"user_id": user_id}