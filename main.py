import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
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
    )
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
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
    updated_order = Order(
        order_customer=payload.order_customer,
        order_po=payload.order_po, 
        order_date=payload.order_date, 
        order_created_by=payload.order_created_by,
        order_created_at=payload.order_created_at,
        requested_date=payload.requested_date, 
        order_product=payload.order_product, 
        order_product_quantity=payload.order_product_quantity,  
        order_status=payload.order_status,
        order_total=payload.order_total,
    )
    statement = select(Order).where(Order.id == id)
    existing_order = session.exec(statement).first()
    
    if not existing_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {id} not found"
        )
    
    existing_order.order_customer = updated_order.order_customer
    existing_order.order_po = updated_order.order_po
    existing_order.order_date = updated_order.order_date
    existing_order.order_created_by = updated_order.order_created_by
    existing_order.order_created_at = updated_order.order_created_at
    existing_order.requested_date = updated_order.requested_date
    existing_order.order_product = updated_order.order_product
    existing_order.order_product_quantity = updated_order.order_product_quantity
    existing_order.order_status = updated_order.order_status
    existing_order.order_total = updated_order.order_total

    session.add(existing_order)
    session.commit()
    session.refresh(existing_order)
    return {"message:" f"Order updated: {existing_order.id}"}


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


# @app.post('/register', response_model=UserSchema)
# def register_user(payload: UserRegistrationSchema, session: Session = Depends(get_session)):
#     """Processes request to register user account."""
#     payload.hashed_password = User.hash_password(payload.hashed_password)
#     return create_user(user=payload, session=session)


# @app.post('/login', status_code=200)
# async def login(payload: UserAccountSchema, session: Session = Depends(get_session)):
#     try:
#         user: User = get_user(email=payload.email, session=session)
#     except:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid user credentials"
#         )

#     is_validated: bool = user.validate_password(payload.hashed_password)
#     print(f"Is user validated? {is_validated}")
#     if not is_validated:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid user credentials"
#         )

#     access_token_expires = timedelta(
#         minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"email": user.email}, expires_delta=access_token_expires
#     )
#     return Token(access_token=access_token, token_type="bearer")


# @app.get('/getUser', status_code=200)
# async def get_user_id(current_user: User = Depends(get_current_user_token)):
#     return {"email": current_user.email, "id": current_user.id}


# @app.get('/logout', status_code=200)
# def logout(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
#     try:
#         blacklisted_token = BlacklistedToken(
#             created_at=datetime.now(timezone.utc), token=token)
#         session.add(blacklisted_token)
#         session.commit()
#     except IntegrityError as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token"
#         )
#     return {"details:": "Logged out"}

if __name__ == "__main__":
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)