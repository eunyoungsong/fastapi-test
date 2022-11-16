# 기본 예외 처리기 재정의  

from fastapi import FastAPI, HTTPException  # 잘못된 데이터가 요청됬을때 기본 JSON 응답 반환
from fastapi.exceptions import RequestValidationError   # 재정의를 위해 가져오기 
from fastapi.responses import PlainTextResponse     
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}



# 예제 더 있지만 패쓰