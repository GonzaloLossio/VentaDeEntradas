from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.order import Order
from app.models.zone import Zone
from app.models.ticket import Ticket
from app.core.config import settings
import stripe
import uuid

router = APIRouter()

@router.post('/webhook/stripe')
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    payment_intent_id = event["data"]["object"]["id"]

    result = await db.execute(select(Order).where(Order.stripe_payment_id == payment_intent_id))
    order = result.scalars().first()
    if not order:
        return {"status": "ok"}

    if event["type"] == "payment_intent.succeeded":
        order.order_state = "Completed"
        for _ in range(order.tickets):
            ticket = Ticket(
                order_id=order.id,
                zone_id=order.zone_id,
                unique_code=str(uuid.uuid4())
            )
            db.add(ticket)

    elif event["type"] == "payment_intent.payment_failed":
        order.order_state = "Failed"
        result = await db.execute(select(Zone).where(Zone.id == order.zone_id))
        zone = result.scalars().first()
        if zone:
            zone.tickets_sold -= order.tickets

    await db.commit()
    return {"status": "ok"}