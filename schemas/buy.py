from pydantic import BaseModel

class OrderSchema(BaseModel):
    total: str
    date_purchase: str
    products: str
    user_id: int

class OrderDetailSchema(BaseModel):
    order_id:int
    saucer_id:int