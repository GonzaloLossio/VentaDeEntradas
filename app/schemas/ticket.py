from sqlmodel import SQLModel,Field
from datetime import datetime

class TicketResponse(SQLModel):
    id : int 
    order_id : int 
    zone_id : int 
    unique_code : str 
    created_at : datetime 