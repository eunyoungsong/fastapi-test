# 경로 매겨변수 : 경로(file_path)를 포함하는 매겨변수 변환기

# OpenAPI는 경로를 포함하는 경로 매개변수를 내부에 선언하는 방법을 지원하지 않습니다.
# 그럼에도 Starlette의 내부 도구중 하나를 사용하여 FastAPI에서는 할 수 있습니다.
# 매개변수에 경로가 포함되어야 한다는 문서를 추가하지 않아도 문서는 계속 작동합니다

from fastapi import FastAPI

app = FastAPI()

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

# 매개변수가 /home/johndoe/myfile.txt 를 갖고 있어 슬다래시로 시작(/)해야 할 수 있습니다.
# 이 경우 URL은 /files//home/johndoe/myfile.txt 이며 files과 home 사이에 이중 슬래시(//)가 생깁니.