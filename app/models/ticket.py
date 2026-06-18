from sqlmodel import SQLModel,Field
from datetime import datetime,timezone

class Ticket(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key=True)
    order_id : int | None = Field(foreign_key="order.id")
    zone_id : int | None = Field(foreign_key="zone.id")
    unique_code : str = Field(unique = True)
    created_at : datetime = Field(default_factory= lambda: datetime.now(timezone.utc))