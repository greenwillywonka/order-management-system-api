import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from db import get_session
from models.new_order import OrderCreate

# from models.urls import Urls
# from models.users import User, UserSchema, UserAccountSchema, UserRegistrationSchema
# from models.tokens import Token, BlacklistedToken, create_access_token
from models.orders import Order  
from models.customers import Customer

import config

from services import get_current_user_token, create_user, get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()



origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# change below to my go with my API information

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/orders")
async def get_all_orders(session: Session = Depends(get_session)):
    statement = select(Order)
    print(f"SQL Statement is: {statement}")
    results = session.exec(statement).all()
    print(f"Results: {results}")
    return results

@app.get("/customers")
async def get_all_customers(session: Session = Depends(get_session)):
    statement = select(Customer)
    print(f"SQL Statement is: {statement}")
    results = session.exec(statement).all()
    print(f"Results: {results}")
    return results

#Below is for searchbar functionality in the frontend on new orders page for custoer
@app.get("/customers/search")
def search_customers(q: str = Query(..., min_length=1), session: Session = Depends(get_session)):
    results = session.exec(
        select(Customer).where(Customer.customer_name.ilike(f"%{q}%"))
    ).all()
    return results
# READ data

# # CREATE data


@app.post("/orders")
async def add_order(payload:Order, session: Session = Depends(get_session)):
    new_order = Order( 
        order_customer=payload.order_customer,
        order_po=payload.order_po, 
        order_date=payload.order_date, 
        order_created_by=payload.order_created_by,
        order_created_at=datetime.now(timezone.utc),
        requested_date=payload.requested_date, 
        order_product=payload.order_product, 
        order_product_quantity=payload.order_product_quantity,  
        order_status=payload.order_status,
        order_total=payload.order_total,
        tracking_number=payload.tracking_number,
    )
    session.add(new_order)
    session.commit()
    session.refresh(new_order)

        # 2. Find the customer and update their stats
    statement = select(Customer).where(Customer.customer_name == new_order.order_customer)
    customer = session.exec(statement).first()

    if customer:
        # Increment order quantity
        customer.order_quantity = (customer.order_quantity or 0) + 1

        # Update last order date
        customer.last_order_date = new_order.order_date

        # Recalculate average order total
        # orders_for_customer = session.exec(
        #     select(Order).where(Order.order_customer == customer.customer_name)
        # ).all()

        # if orders_for_customer:
        #     total_spent = sum(order.order_total for order in orders_for_customer if order.order_total)
        #     customer.average_order_total = total_spent / len(orders_for_customer)
        orders_for_customer = session.exec(
            select(Order).where(Order.order_customer == customer.customer_name)
        ).all()

        # Filter out orders that don’t have a numeric total
        totals = [order.order_total for order in orders_for_customer if order.order_total is not None]

        if totals:
            customer.average_order_total = sum(totals) / len(totals)
        else:
            customer.average_order_total = 0
            
        session.add(customer)
        session.commit()
        session.refresh(customer)

    return {"message:" f"New order created: {new_order.id}"}

@app.post("/customers")
async def add_customer(payload:Customer, session: Session = Depends(get_session)):
    new_customer = Customer( 
       created_at=payload.created_at,
       order_quantity=payload.order_quantity,
       last_order_date=payload.last_order_date,
       average_order_total=payload.average_order_total,
       assigned_representative=payload.assigned_representative,
       customer_name=payload.customer_name,
       customer_notes=payload.customer_notes,
       purchaser=payload.purchaser,
       email=payload.email,
       phonenumber=payload.phonenumber,
       address=payload.address,
       city=payload.city,
       state=payload.state,
       zipcode=payload.zipcode,
    )
    session.add(new_customer)
    session.commit()
    session.refresh(new_customer)
    return {"message:" f"New customer created: {new_customer.id}"}


@app.get("/orders/{id}")
async def get_order(id: int, session: Session = Depends(get_session)):
    statement = select(Order).where(Order.id == id)
    result = session.exec(statement).one()

    return result

@app.get("/customers/{id}")
async def get_customer(id: int, session: Session = Depends(get_session)):
    statement = select(Customer).where(Customer.id == id)
    result = session.exec(statement).one()

    return result

@app.put("/orders/{id}")
async def update_order(id: int, payload: Order, session: Session = Depends(get_session)):
    # 1️⃣ Find the existing order
    statement = select(Order).where(Order.id == id)
    existing_order = session.exec(statement).first()
    
    if not existing_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {id} not found"
        )

    # 2️⃣ Update fields (use order_customer string, not customer_id)
    existing_order.order_customer = payload.order_customer
    existing_order.order_po = payload.order_po
    existing_order.order_date = payload.order_date
    existing_order.order_created_by = payload.order_created_by
    existing_order.order_created_at = payload.order_created_at
    existing_order.requested_date = payload.requested_date
    existing_order.order_product = payload.order_product
    existing_order.order_product_quantity = payload.order_product_quantity
    existing_order.order_status = payload.order_status
    existing_order.order_total = payload.order_total
    existing_order.tracking_number = payload.tracking_number

    session.add(existing_order)
    session.commit()
    session.refresh(existing_order)

    # 3️⃣ Update customer stats
    customer = session.exec(
        select(Customer).where(Customer.customer_name == existing_order.order_customer)
    ).first()

    if customer:
        # Get all orders for this customer
        orders_for_customer = session.exec(
            select(Order).where(Order.order_customer == customer.customer_name)
        ).all()

        # Update order quantity
        customer.order_quantity = len(orders_for_customer)

        # Update last order date
        if orders_for_customer:
            customer.last_order_date = max(o.order_date for o in orders_for_customer if o.order_date)

        # Update average order total (ignore orders without a numeric total)
        totals = [o.order_total for o in orders_for_customer if o.order_total is not None]
        customer.average_order_total = sum(totals) / len(totals) if totals else 0

        session.add(customer)
        session.commit()
        session.refresh(customer)

    return {"message": f"Order updated: {existing_order.id}"}


@app.put("/customers/{id}")
async def update_customer(id: int, payload: Customer, session: Session = Depends(get_session)):
    updated_customer = Customer(
        created_at=payload.created_at,
        order_quantity=payload.order_quantity,
        last_order_date=payload.last_order_date,
        average_order_total=payload.average_order_total,
        assigned_representative=payload.assigned_representative,
        customer_name=payload.customer_name,
        customer_notes=payload.customer_notes,
        purchaser=payload.purchaser,
        email=payload.email,
        phonenumber=payload.phonenumber,
        address=payload.address,
        city=payload.city,
        state=payload.state,
        zipcode=payload.zipcode,
    )
    statement = select(Customer).where(Customer.id == id)
    existing_customer = session.exec(statement).first()
    
    if not existing_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with id {id} not found"
        )
    
    existing_customer.created_at = updated_customer.created_at
    existing_customer.order_quantity = updated_customer.order_quantity
    existing_customer.last_order_date = updated_customer.last_order_date
    existing_customer.average_order_total = updated_customer.average_order_total
    existing_customer.assigned_representative = updated_customer.assigned_representative
    existing_customer.customer_name = updated_customer.customer_name
    existing_customer.customer_notes = updated_customer.customer_notes
    existing_customer.purchaser = updated_customer.purchaser
    existing_customer.email = updated_customer.email
    existing_customer.phonenumber = updated_customer.phonenumber
    existing_customer.address = updated_customer.address
    existing_customer.city = updated_customer.city
    existing_customer.state = updated_customer.state
    existing_customer.zipcode = updated_customer.zipcode

    session.add(existing_customer)
    session.commit()
    session.refresh(existing_customer)
    return {"message:" f"Customer updated: {existing_customer.id}"}

if __name__ == "__main__":
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)