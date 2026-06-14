from sqlmodel import SQLModel
from datetime import date,time

class EventCreate(SQLModel):
    title: str 
    description : str 
    date : date
    time: time
    location : str

class EventResponse(SQLModel):
    id : int 
    title: str 
    description : str 
    date : date
    time: time
    location : str