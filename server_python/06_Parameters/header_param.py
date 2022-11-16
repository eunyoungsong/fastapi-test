# Header Parameters

from typing import Optional
from fastapi import FastAPI, Header   # Header 가져오기 

app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}



# Header는 Path, Query 그리고 Cookie가 제공하는 것 외에 기능이 조금 더 있습니다.   ---> 언더스코어를 하이픈으로 자동 변환 !! 
'''
대부분의 표준 헤더는 "마이너스 기호" (-)라고도 하는 "하이픈" 문자로 구분됩니다.
그러나 파이썬에서 user-agent와 같은 형태의 변수는 유효하지 않습니다.
따라서 Header는 기본적으로 매개변수 이름을 언더스코어(_)에서 하이픈(-)으로 변환하여 헤더를 추출하고 기록합니다.
또한 HTTP 헤더는 대소문자를 구분하지 않으므로 "snake_case"로 알려진 표준 파이썬 스타일로 선언할 수 있습니다.
따라서, User_Agent 등과 같이 첫 문자를 대문자화할 필요없이 파이썬 코드에서처럼 user_agent로 사용합니다.
만약 언더스코어를 하이픈으로 자동 변환을 비활성화해야 할 어떤 이유가 있다면, Header의 convert_underscores 매개변수를 False로 설정하십시오
'''

from typing import Optional
from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(
    strange_header: Optional[str] = Header(None, convert_underscores=False)   # convert_underscores=False : 자동변환 비활성화 
):
    return {"strange_header": strange_header}




# 중복헤더 : list 로 수신 
from typing import List, Optional
from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(x_token: Optional[List[str]] = Header(None)):
    return {"X-Token values": x_token}