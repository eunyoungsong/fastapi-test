# Body : 중첩된 하위 모델

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: set[str] = set()
    images: Optional[list[Image]] = None


class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    items: list[Item]


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer

'''
예상본문
{
  "name": "string",
  "description": "string",
  "price": 0,
  "items": [
    {
      "name": "string",
      "description": "string",
      "price": 0,
      "tax": 0,
      "tags": [],
      "images": [
        {
          "url": "string",
          "name": "string"
        }
      ]
    }
  ]
}
'''