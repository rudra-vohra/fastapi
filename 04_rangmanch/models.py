from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime,timezone

class Review(SQLModel, table = True):
    id: Optional[int] = Field(default=None,primary_key=True)
    play_name: str
    reviewer_name: str
    rating: int = Field(ge=1,le=5)
    comment: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

class CreateReview(SQLModel):
    play_name:str
    reviewer_name:str
    rating:int = Field(ge=1,le=5)
    comment:str

class ReadReview(SQLModel):
    id:int
    play_name:str
    reviewer_name:str
    rating:int = Field(ge=1,le=5)
    comment:str
    created_at: datetime

class UpdateReview(SQLModel):
    comment: Optional[str] = None
    rating: Optional[int] = Field(default=None,ge=1,le=5)
