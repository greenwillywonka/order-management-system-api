from pydantic import BaseModel
from datetime import date
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, Session, select
from .base import Base #added this import to use Base class

class OrderCreate(Base):    #changed from SQLModel to Base 
    customer: str
    # orderdate: date
    po: str
    product: str  # Assuming products is a list of product IDs or names
    quantity: int
    # status: str
    total: float

