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
