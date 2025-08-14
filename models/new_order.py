from pydantic import BaseModel
from datetime import date

class OrderCreate(BaseModel):
    orderid: str
    customer: str
    orderdate: date
    po: str
    status: str
    total: float
