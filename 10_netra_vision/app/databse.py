from sqlmodel import Session, create_engine, SQLModel

DATABASE_URL = "sqlite:///./netra_vision.db"


engine = create_engine(DATABASE_URL, echo=True)

def create_tables():
    """Create database tables based on the defined models."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get a new database session."""
    with Session(engine) as session:
        yield session




