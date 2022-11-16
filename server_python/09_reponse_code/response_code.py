# 응답 코드 

from fastapi import FastAPI

app = FastAPI()


@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}



'''
status_code=201로 선언하여
api 함수가 정상적으로 종료되면
응답 코드로 201을 반환하게 만들 수 있다.
'''

# 보다 직관적인 코드 선언 방법 : status_code=status.HTTP_201_CREATED
# from fastapi import FastAPI, status # status 임포트 해줘야함 

# app = FastAPI()

# @app.post("/items/", status_code=status.HTTP_201_CREATED)
# async def create_item(name: str):
#     return {"name": name}