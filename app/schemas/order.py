from sqlmodel import SQLModel
from datetime import datetime

class OrderCreate(SQLModel):
    tickets: int 
    zone_id: int 

class OrderResponse(SQLModel):
    id : int 
    user_id : int 
    zone_id: int 
    tickets: int 
    stripe_payment_id : str 
    total_price : float 
    order_state : str  
    created_at: datetime 