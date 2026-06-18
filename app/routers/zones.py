from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends,HTTPException
from app.schemas.zone import ZoneCreate,ZoneResponse
from app.models.zone import Zone
from app.models.event import Event
from app.core.security import get_admin_user
from app.database import get_db

router = APIRouter()

@router.post('/events/{event_id}/zones',response_model=ZoneResponse)
async def create_zone(zone : ZoneCreate, event_id: int, db : AsyncSession = Depends(get_db), admin_user = Depends(get_admin_user)):
    result = await db.execute(select(Event).where(Event.id == event_id))
    valid_event = result.scalars().first()
    if not valid_event:
        raise HTTPException(status_code=404, detail= "Event not found")
    
    new_zone = Zone(
        event_id = event_id,
        name = zone.name,
        price = zone.price,
        capacity = zone.capacity
    )

    db.add(new_zone)
    await db.commit()
    await db.refresh(new_zone)

    return new_zone

@router.get('/events/{event_id}/zones/{zone_id}',response_model=ZoneResponse)
async def get_specific_zone_from_an_specific_event(event_id :int, zone_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Zone).where(Zone.event_id == event_id, Zone.id == zone_id, Zone.is_active == True))
    zone = result.scalars().first()
    if not zone:
        raise HTTPException(status_code=404, detail= "There is no specific zone in this event")
    return zone

@router.get('/events/{event_id}/zones', response_model=list[ZoneResponse])
async def get_all_zones_from_an_specific_event(event_id : int, db : AsyncSession = Depends(get_db)):
    result = await db.execute(select(Zone).where(Zone.event_id == event_id, Zone.is_active == True))
    zones = result.scalars().all()
    if not zones:
        raise HTTPException(status_code=404, detail= "There are no zones for this event")
    return zones

@router.put('/events/{event_id}/zones/{zone_id}',response_model=ZoneResponse)
async def update_zone(zone_id : int, zone_update : ZoneCreate,event_id: int, db : AsyncSession = Depends(get_db),admin_user = Depends(get_admin_user)):
    result = await db.execute(select(Zone).where(Zone.id == zone_id,Zone.event_id == event_id))
    zone = result.scalars().first()
    if not zone:
        raise HTTPException(status_code=404, detail= "Zone not found")
    for key,value in zone_update.model_dump().items():
        setattr(zone,key,value)
    await db.commit()
    await db.refresh(zone)    
    return zone

@router.delete('/events/{event_id}/zones/{zone_id}')
async def deactivate_zone(zone_id : int , event_id: int, db : AsyncSession = Depends(get_db), admin_user = Depends(get_admin_user)):
    result = await db.execute(select(Zone).where(Zone.id == zone_id,Zone.event_id == event_id))
    zone = result.scalars().first()
    if not zone:
        raise HTTPException(status_code=404, detail= "Zone not found")
    zone.is_active = False
    await db.commit()
    await db.refresh(zone)
    return zone