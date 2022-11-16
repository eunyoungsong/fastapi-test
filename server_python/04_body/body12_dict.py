# Body : dict 
# 아직 모르는 키를 수신하려는 경우 유용!

from fastapi import FastAPI

app = FastAPI()


@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):  # 요렇게 dict 형태로 선언!
    return weights

# JSON 은 str 형태의 키만 지원합니다.
# 하지만 Pydantic 에는 자동 데이터 변환 기능이 있습니다!!

# 이 예제에서 weights 은 실제로 int 키와 float 값을 가질 것 :)