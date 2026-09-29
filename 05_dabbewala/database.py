from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./dabbewala.db"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    '''Return a new database session per request'''
    with Session(engine) as session:
        yield session   

def create_table():
    '''Create the database tables if they don't exist'''
    SQLModel.metadata.create_all(engine)

