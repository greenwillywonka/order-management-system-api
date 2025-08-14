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
from models.orders import Orders  

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
    statement = select(Orders)
    print(f"SQL Statement is: {statement}")
    results = session.exec(statement).all()
    print(f"Results: {results}")
    return results

# READ data


# @app.get("/urls/{id}")
# async def get_single_url(id: str, session: Session = Depends(get_session)):
#     statement = select(Urls).where(Urls.id == id)
#     result = session.exec(statement).one()

#     return result

# # CREATE data


@app.post("/orders")
async def add_order(payload:OrderCreate, session: Session = Depends(get_session)):
    print(f"Payload received: {payload}")
    new_order = Orders(orderid=payload.orderid, customer=payload.customer, orderdate=payload.orderdate, po=payload.po, status=payload.status, total=payload.total
    )
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return {"message": f"Added new url with ID: {new_order.id}"}


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