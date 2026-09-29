from sqlmodel import SQLModel,create_engine,Session

DATABASE_URL = "sqlite:///./rangmanch.db"

engine = create_engine(DATABASE_URL,echo=True)

def createTable():
    '''Creates tables defined by SQLModel class'''
    SQLModel.metadata.create_all(engine)

def getSession():
    with Session(engine) as session:
        yield session

