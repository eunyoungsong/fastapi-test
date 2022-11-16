# Cookie Parameters

from typing import Optional
from fastapi import Cookie, FastAPI    # Cookie 가져오기 

app = FastAPI()


@app.get("/items/")
async def read_items(ads_id: Optional[str] = Cookie(None)):
    return {"ads_id": ads_id}

# HTTP 쿠키 
# 서버가 사용자의 웹 브라우저에 전송하는 작은 데이터 조각
# 브라우저는 그 데이터 조각들을 저장해 놓았다가, 동일한 서버에 재요청시 저장된 데이터를 함께 전송