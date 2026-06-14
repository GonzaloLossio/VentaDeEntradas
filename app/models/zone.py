from sqlmodel import SQLModel,Field

class Zone(SQLModel,table = True):
    id: int | None = Field(default=None, primary_key=True)
    event_id : int | None = Field(foreign_key="event.id")
    name : str
    price: float = 100.0
    capacity : int = 10000
    tickets_sold : int = 0
