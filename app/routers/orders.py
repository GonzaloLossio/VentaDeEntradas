from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends,HTTPException
from app.schemas.order import OrderCreate,OrderResponse
from app.models.zone import Zone
from app.models.order import Order
from app.core.security import get_current_user
from app.database import get_db

router = APIRouter()

@router.post('/orders',response_model=OrderResponse)
async def create_order(order : OrderCreate, db : AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    result = await db.execute(select(Zone).where(Zone.id == order.zone_id, Zone.is_active == True).with_for_update())
    zone = result.scalars().first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")

    if zone.capacity-order.tickets-zone.tickets_sold < 0 :  
     raise HTTPException(status_code=400, detail="Not enough tickets available")
    
    total_price  = zone.price * order.tickets

    new_order = Order(
        user_id = current_user.id, 
        zone_id = zone.id ,
        tickets = order.tickets,
        total_price  = total_price ,
        order_state  = "Pending",
    )

    zone.tickets_sold = zone.tickets_sold + order.tickets

    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order

@router.get('/orders/me', response_model=list[OrderResponse])
async def get_all_orders_for_an_user(db : AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Order).where(Order.user_id==current_user.id))
    all_orders = result.scalars().all()
    if not all_orders:
        raise HTTPException(status_code=404, detail= "There are no orders for this user")
    return all_orders