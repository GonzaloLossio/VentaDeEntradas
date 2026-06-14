from sqlmodel import SQLModel 

class ZoneCreate(SQLModel):
    event_id : int
    name : str
    price: float 
    capacity : int 

class ZoneResponse(SQLModel):
    id: int
    event_id : int
    name : str
    price: float 
    capacity : int 
    tickets_sold : int 