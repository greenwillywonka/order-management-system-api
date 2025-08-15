from pydantic import BaseModel
from datetime import date
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, Session, select

class OrderCreate(SQLModel):
    # orderid: str
    customer: str
    # orderdate: date
    po: str
    product: str  # Assuming products is a list of product IDs or names
    quantity: int
    # status: str
    total: float




# This is code from order.py. I am making the order.py model like my new_order.py model. below is the unalterd code from orders.py before changing it.


# from .base import Base     .....these were commented out in original code

# from sqlalchemy import String, Date, Float
# from sqlmodel import Field, Column
# from sqlmodel import SQLModel
# from datetime import date

# from sqlalchemy.dialects.postgresql import VARCHAR as varchar     .....these were commented out in original code
# from sqlalchemy.dialects.postgresql import NUMERIC as numeric     .....these were commented out in original code
# from sqlalchemy.dialects.postgresql import DECIMAL as decimal     .....these were commented out in original code




# class Orders(SQLModel, table=True):
#     __tablename__: str = "orders"

#     orderid: int = Field(
#         default=None,
#         primary_key=True,
#         index=True,
#         nullable=False,
#     )
    
#     customer: str = Field(sa_column=Column(String))
#     orderdate: date = Field(sa_column=Column(Date))
#     po: str = Field(sa_column=Column(String))
#     status: str = Field(sa_column=Column(String))
#     total: float = Field(sa_column=Column(Float))
