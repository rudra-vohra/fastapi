from typing import List
from pydantic import BaseModel

class MenuItems(BaseModel):
    id : int
    name : str
    category : str
    price : float
    description : str
    available : bool

class MenuResponse(BaseModel):
    status: str = "success"
    count: int
    items: List[MenuItems]

