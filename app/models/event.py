from sqlmodel import SQLModel,Field
from datetime import date,time

class Event(SQLModel,table = True):
    id : int | None = Field(default=None, primary_key=True)
    title: str = Field(unique = True)
    description : str 
    date : date
    time: time
    location : str
    is_active : bool = True