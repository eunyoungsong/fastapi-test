# Security 01 : 구성 

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer # OAuth2PasswordBearer : Bearer토큰을 사용하여 Password Flow과 함께 OAuth2를 사용

app = FastAPI()

# URL에 토큰 포함시키기 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):   # 토큰을 str로 제공 (유용하지않음)
    return {"token": token}



'''
# Password Flow : 보안 및 인증을 처리하기 위해 OAuth2에 정의된 방식 중 하나
# 1. 사용자는 프론트엔드에 username 및 password를 입력하고 누릅니다 
# 2. 프론트엔드는 username과 password를 API의 특정URL로 보냅니다. (tokenUrl="token")
# 3. API는 username과 password을 확인하고 토큰 응답으로 확인합니다.
#    토큰은 나중에 사용자를 확인하는 데 사용할 수 있는 일부 콘텐츠가 포함된 문자열입니다.
#    일반적으로 토큰은 일정 시간이 지나면 만료되도록 설정됩니다.
#    따라서 사용자는 나중에 다시 로그인해야 합니다.
# 4. 프론트엔드는 해당 토큰을 어딘가에 임시로 저장합니다.
# 5. 사용자가 프론트엔드를 클릭하여 프론트엔드 웹 앱의 다른 섹션으로 이동합니다.
# 6. 프론트엔드는 API에서 더 많은 데이터를 가져와야 합니다.
#    그러나 특정 엔드포인트에 대한 인증이 필요합니다.
#    따라서 API로 인증하기 위해 Bearer 값에 토큰을 더한 Authorization 헤더를 보냅니다.
#    토큰에 foobar가 포함된 경우 Authorization 헤더의 내용은 Bearer foobar입니다.
'''