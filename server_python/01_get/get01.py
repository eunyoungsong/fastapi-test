# First Step

from fastapi import FastAPI

app = FastAPI()


@app.get("/")       # 경로 동작 데코레이터(@) 정의 : FastAPI에게 아래함수가 경로(/)에 해당하는 get동작을 하라고 알려줌
async def root():
    return {"message": "Hello World"}

'''
< HTTP 메소드(동작) >
GET : 데이터 조회 (URL을 통해 데이터를 받음, 데이터가 눈에 보임, Body값과 Content-Type 이 비워져있음)
POST: 데이터 생성/변경 (URL을 통해 데이터를 받지 않고 Body을 통해 받음, 대용량 전송가능, Body값에 성공응답)
PUT : 데이터 생성/변경 (URL을 통해 어떤 데이터를 수정할지 받고 Body값을 통해 수정할 데이터 값을 받음, Body값에 성공응답) 
DELETE : 데이터 삭제  (URL을 통해 어떤 데이터를 삭제할지 받고 Body값 없이 성공응답만 보냄)

OPTIONS
HEAD
PATCH
TRACE

GET vs POST : GET은 캐싱을 하기 때문에 여러번 요청시 저장된 데이터를 활용하므로 POST보다 빠르다. POST는 데이터가 눈에 보이지 않아 GET 보다 안전하다. 
POST vs PUT  : POST는 요청시마다 데이터를 생성, PUT은 해당 데이터를 지정하여 수정하기 때문에 데이터가 계속 생성되지 않는다. (post새로추가/put덮어쓰기)
PATCH vs PUT : PUT은 지정한 데이터를 전부 수정하는 Method이지만 PATCH는 정보의 일부분이 변경되는 방법
'''