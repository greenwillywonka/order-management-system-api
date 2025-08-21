from models.orders import Order  
from models.customers import Customer
import config
from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from db import get_session_direct
from models.new_order import OrderCreate

def create_customers_from_orders(session: Session):
    statement = select(Order)
    orders = session.exec(statement).all()
    
    customer_dict = {}
    
    for order in orders:
        if order.order_customer not in customer_dict:
            customer_dict[order.order_customer] = {
                "created_at": order.order_created_at,
                "order_quantity": 1,
                "last_order_date": order.order_date,
                "average_order_total": order.order_total,
                "assigned_representative": order.order_created_by,
                "customer_name": order.order_customer,
                "customer_notes": "",
                "purchaser": "",
                "email": "",
                "phonenumber": "",
                "address": "",
                "city": "",
                "state": "",
                "zipcode": ""
            }
        else:
            customer_info = customer_dict[order.order_customer]
            customer_info["order_quantity"] += 1
            customer_info["last_order_date"] = max(customer_info["last_order_date"], order.order_date)
            total_orders = customer_info["average_order_total"] * (customer_info["order_quantity"] - 1) + order.order_total
            customer_info["average_order_total"] = total_orders / customer_info["order_quantity"]
    
    for cust_data in customer_dict.values():
        existing_customer = session.exec(select(Customer).where(Customer.customer_name == cust_data["customer_name"])).first()
        if not existing_customer:
            new_customer = Customer(**cust_data)
            session.add(new_customer)
            print(f"Creating customer: {new_customer}")
    
    session.commit()

if __name__ == "__main__":
    session=get_session_direct()
    create_customers_from_orders(session)
