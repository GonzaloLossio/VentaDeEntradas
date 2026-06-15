from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends,HTTPException
from datetime import date
from app.schemas.event import EventCreate,EventResponse
from app.models.event import Event
from app.core.security import get_admin_user
from app.database import get_db

router = APIRouter()

@router.post('/events', response_model=EventResponse)
async def create_events(event : EventCreate, db : AsyncSession = Depends(get_db), admin_user = Depends(get_admin_user)):
    new_event = Event(
        title = event.title,
        description = event.description,
        date = event.date,
        time = event.time,
        location = event.location
    )

    db.add(new_event)
    await db.commit()
    await db.refresh(new_event)
    return new_event

@router.get('/events',response_model=list[EventResponse])
async def get_list_of_events(db : AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event).where(Event.date >= date.today(), Event.is_active == True))
    events = result.scalars().all()
    if not events:
        raise HTTPException(status_code=404, detail="There are no events registered")
    return events

@router.get('/events/{event_id}',response_model=EventResponse)
async def get_event(event_id : int, db : AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalars().first()
    if not event:
        raise HTTPException(status_code=404, detail="There is no events with this id")
    return event

@router.put('/events/{event_id}',response_model=EventResponse)
async def update_event(event_id : int , event_update : EventCreate, db : AsyncSession = Depends(get_db), admin_user = Depends(get_admin_user)):
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalars().first()
    if not event:
        raise HTTPException(status_code=404, detail="There is no events with this id")
    
    for key, value in event_update.dict().items():
        setattr(event,key,value)

    await db.commit()
    await db.refresh(event)    

    return event

@router.delete('/events/{event_id}')
async def delete_event(event_id : int, db: AsyncSession = Depends(get_db) , admin_user = Depends(get_admin_user)):
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalars().first()
    if not event:
        raise HTTPException(status_code=404, detail="There is no events with this id")
    event.is_active = False
    await db.commit()
    await db.refresh(event)
    return event