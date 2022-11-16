# Form Data
# JSON 대신 양식 필드를 수신해야 하는 경우 Form을 사용할 수 있습니다.

from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username" : username}