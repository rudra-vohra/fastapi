from sqlmodel import SQLModel, Field,Relationship
from typing import Optional

# Database model for the Book table
class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    author: str = Field(index=True)
    price: int
    is_sold: bool = Field(default=False)

    user_id: int = Field(default=None, foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="books")


# Models for creating and reading Book data
class CreateBook(SQLModel):
    title: str
    author: str
    price: int
    user_id: int

class ReadBook(SQLModel):
    id: int
    title: str
    author: str
    price: int
    is_sold: bool
    user_id: int

class UpdateBook(SQLModel):
    price: Optional[int] = None
    is_sold: Optional[bool] = None


from models.user import User
Book.model_rebuild()


