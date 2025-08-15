from pydantic import BaseModel
from datetime import date
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, Session, select
from .base import Base


class Order(Base):
    order_id: str
    created_at: timestamp
    order_customer: str
    order_date: date
    requested_date: str
    order_po: str
    order_product: str  
    order_product_quantity: int
    order_created_by: str
    order_status: str
    order_total: float
