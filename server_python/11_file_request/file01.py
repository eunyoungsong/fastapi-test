# File 요청 
# File 은 Form 으로부터 직접 상속된 클래스

from fastapi import FastAPI, File, UploadFile       # file 가져오기 

app = FastAPI()

@app.post("/files/")
async def create_file(file: bytes = File(...)):     # File 매개변수 정의 : 메모리에 저장 (작은파일에 적합)
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):     # UploadFile : 디스크에 저장 (대용량 파일에 적합)
    return {"filename": file.filename}



# File의 본문을 선언할 때, 
# 매개변수가 쿼리 매개변수 또는 본문(JSON) 매개변수로
# 해석되는 것을 방지하기 위해 File 을 사용해야합니다.

# 파일들은 "폼 데이터"의 형태로 업로드

# bytes 로 선언하는 경우 FastAPI는 파일을 읽고 bytes 형태의 내용을 전달
# 전체 내용이 메모리에 저장된다는 것을 의미
# 이는 작은 크기의 파일들에 적합

# UploadFile 장점 
# 스폴파일을 사용 : 최대 크기 제한까지만 메모리에 저장, 이를 초과하는 경우 디스크에 저장 됨
# 따라서 이미지, 동영상 같은 대용량 파일들을 많은 메모리를 소모하지 않고 처리하기에 적합 

'''

< UploadFile async 메소드 >

- write(data)
- read(size)
- seek(offset):
    파일 내 offset(int) 위치의 바이트로 이동합니다.
    예) await myfile.seek(0) 를 사용하면 파일의 시작부분으로 이동합니다.
        await myfile.read() 를 사용한 후 내용을 다시 읽을 때 유용합니다.
- close()

'''


