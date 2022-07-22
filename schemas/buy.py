from pydantic import BaseModel

class OrderSchema(BaseModel):
    total: float
    date_purchase: str
    products: list
    user_id: int

class OrderDetailSchema(BaseModel):
    order_id:int
    saucer_id:int
