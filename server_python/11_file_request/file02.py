# 다중 파일 업로드 
# 여러파일을 동시에 업로드 할 수 있습니다.
# 폼데이터를 사용하여 전송된 동일한 폼필드에 연결됩니다. 

from typing import List

from fastapi import FastAPI, File, UploadFile       # File, UploadFile 가져오기 
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/files/")
async def create_files(files: List[bytes] = File(...)):     # List 타입으로 File 정의 
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile]):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)