from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends,HTTPException
from app.models.order import Order
from app.models.ticket import Ticket
from app.database import get_db
from app.core.security import get_current_user
from app.schemas.ticket import TicketResponse

router = APIRouter()

@router.get('/tickets/me',response_model=list[TicketResponse])
async def get_all_tickets(db : AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    result = await db.execute(select(Ticket).join(Order,Ticket.order_id == Order.id).where(Order.user_id == current_user.id))
    tickets = result.scalars().all()
    if not tickets:
        raise HTTPException(status_code=404, detail="There is no tickets for this user")
    
    return tickets

