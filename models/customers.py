from pydantic import BaseModel
from datetime import date
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, Session, select
from .base import Base
from datetime import datetime
from sqlalchemy import String, Column, Date, DateTime, Float, Numeric #added this to import sa_column types

class Customer(Base, table=True):
    __tablename__: str = 'customers'   

    created_at: datetime
    order_quantity: int
    last_order_date: date
    average_order_total: float
    assigned_representative: str
    customer_name: str
    customer_notes: str
    purchaser: str
    email: str
    phonenumber: str
    address: str
    city: str
    state: str
    zipcode: str
