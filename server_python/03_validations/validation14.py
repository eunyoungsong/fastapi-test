# 경로 매겨변수 및 숫자 검증 : 매겨변수 정렬 트릭  
# 기본값 없는 매개변수 순서 바꿔서 사용하고 싶을때?

from fastapi import FastAPI, Path

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    *, item_id: int = Path(..., title="The ID of the item to get"), q: str # * 을 첫번째 매겨변수로 전달
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

'''
파이썬  *args : 여러개의 인수를 받을때, 키워드 인수를 받을때 사용 (튜플형태)
    **kwargs : 키워드 - 특정 값 형태로 호출 (딕셔너리형태)

파이썬은 * 으로 아무런 행동도 하지 않지만,
따르는 매개변수들은 kwargs 로도 알려진 키워드 인자(키-값 쌍)여야 함을 인지
'''

# http://127.0.0.1:8000/items/123?q=test