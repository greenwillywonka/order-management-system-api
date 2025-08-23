from sqlmodel import create_engine, SQLModel, Session
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

# For scripts (direct usage)
def get_session_direct():
    return Session(engine)


# below is the updated db.py file after adding connection pool parameters
# from sqlmodel import create_engine, Session, SQLModel
# from config import DATABASE_URL

# engine = create_engine(
#     DATABASE_URL,
#     echo=True,
#     pool_size=3,
#     max_overflow=0,
#     pool_timeout=30
# )

# def get_session():
#     session = Session(engine, autocommit=False, autoflush=False)
#     try:
#         yield session
#     finally:
#         session.close()
