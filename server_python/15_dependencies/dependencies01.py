# 의존성(Dependencies) 주입 

from typing import Optional

from fastapi import Depends, FastAPI   # Import Depends

app = FastAPI()


async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):  # depends 단일매겨변수만 제공 
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons


# Depneds는 전달하기만 하면 FastAPI가 나머지를 알아서 수행 
# 특수 클래스를 생성하고 전달할때 등록하는 작업등을 할 필요 없음