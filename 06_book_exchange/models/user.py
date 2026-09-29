from sqlmodel import SQLModel, Field,Relationship
from typing import Optional

# Database model for the User table
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True)

    books: list["Book"] = Relationship(back_populates="owner")  # Relationship to the Book model


class CreateUser(SQLModel):
    name: str
    email: str
    college:str

class ReadUser(SQLModel):
    id: int
    name: str
    email: str
    college:str

    

from models.books import Book  
User.model_rebuild()

