# Delete TEST


from fastapi import FastAPI, Response, status

from pydantic import BaseModel     


app = FastAPI()


@app.delete("/delete")
async def delete_item():
    delect_item = None;
    return Response(status_code=status.HTTP_204_NO_CONTENT) # 보통 EmptyResponse 사용, Starlette 에서는 204코드사용