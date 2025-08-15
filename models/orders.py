from pydantic import BaseModel
from datetime import date
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, Session, select
from .base import Base
from datetime import datetime
from sqlalchemy import String, Column, Date, DateTime, Float, Numeric #added this to import sa_column types

class Order(Base):  #added fields to see if this would work. 
                    #they were not invluded in what i took from new order model
    order_id: str               #= Field(sa_column=Column(String), primary_key=True, index=True)
    created_at: datetime                #= Field(sa_column=Column(DateTime))
    order_customer: str                 #= Field(sa_column=Column(String))
    order_date: date                #= Field(sa_column=Column(Date))
    requested_date: date                #= Field(sa_column=Column(Date))
    order_po: str               #= Field(sa_column=Column(String))
    order_product: str              #= Field(sa_column=Column(String))
    order_product_quantity: int                 #= Field(sa_column=Column(Numeric))
    order_created_by: str               #= Field(sa_column=Column(String))
    order_status: str               #= Field(sa_column=Column(String))
    order_total: float              #= Field(sa_column=Column(Float))            #
