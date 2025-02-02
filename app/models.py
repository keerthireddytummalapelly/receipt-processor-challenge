from pydantic import BaseModel, Field
from typing import List

class Item(BaseModel):
    shortDescription: str
    price: str = Field(..., pattern=r"^\d+\.\d{2}$")

class Receipt(BaseModel):
    retailer: str
    purchaseDate: str 
    purchaseTime: str
    items: List[Item]
    total: str = Field(..., pattern=r"^\d+\.\d{2}$")

    class Config:
        json_schema_extra = {
            "example": {
              "retailer": "string",
                "purchaseDate": "string",
                "purchaseTime": "string",
                "items": [
                    {
                    "shortDescription": "string",
                    "price": "string"
                    }
                ],
                "total": "string"
            }
        }

class ReceiptId(BaseModel):
    id: str

class Points(BaseModel):
    points: int
