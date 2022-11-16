# 종속성으로서의 클래스 

from typing import Optional

from fastapi import Depends, FastAPI  

app = FastAPI()


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/")
# async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):   
async def read_items(commons = Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response

# CommonQueryParams : 해당 클래스의 인스턴스가 생성되고 인스턴스가 commons함수에 매개변수로 전달 됨 

# commons: CommonQueryParams = Depends(CommonQueryParams) # 종속성을 잘 보여주는 예시, 실제로는 밑에 처럼 사용
# --> commons = CommonQueryParams

# FastAPI가 클래스 자체의 인스턴스를 만들기 위해 호출하는 클래스인 경우 :
# commons: CommonQueryParams = Depends()