# from .base import Base
from sqlalchemy import String, Date, Numeric
from sqlmodel import Field, Column
from sqlmodel import SQLModel
from datetime import date
from sqlalchemy.dialects.postgresql import VARCHAR as varchar
from sqlalchemy.dialects.postgresql import NUMERIC as numeric

class Orders(SQLModel, table=True):
    __tablename__: str = "orders"

    orderid: int = Field(primary_key=True)
    customer: str = Field(sa_column=Column(String))
    orderdate: date = Field(sa_column=Column(Date))
    po: str = Field(sa_column=Column(String))
    status: str = Field(sa_column=Column(String))
    total: float = Field(sa_column=Column(Numeric))
