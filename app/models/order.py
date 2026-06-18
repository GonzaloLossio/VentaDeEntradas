from sqlmodel import SQLModel, Field
from datetime import datetime,timezone

class Order(SQLModel, table = True):
    id : int | None = Field (default = None,primary_key=True)
    user_id : int | None = Field(foreign_key="user.id")
    zone_id: int | None = Field(foreign_key="zone.id")
    tickets: int = 0
    stripe_payment_id : str | None = None
    total_price : float = 0.0
    order_state : str  = Field(default = "Pending")
    created_at: datetime = Field(default_factory = lambda: datetime.now(timezone.utc))

    