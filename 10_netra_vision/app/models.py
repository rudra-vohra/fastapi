from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class Result(SQLModel):
    crop_detected: str
    severity: str
    diseases: list[dict]
    treatments: list[dict]
    overall_health: str = ""
    additional_notes: str = ""

class Analysis(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    image_name: str
    result: dict = Field(default_factory=dict, sa_column=Column(JSON))

