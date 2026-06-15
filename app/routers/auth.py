from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserResponse,UserCreate
from app.models.user import User
from app.core.security import hash_password,verify_password,create_access_token,get_current_user
from app.database import get_db

router = APIRouter()

@router.post("/register", response_model = UserResponse)
async def register(user : UserCreate , db : AsyncSession  = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == user.username))
    username = result.scalars().first()
    if username:
        raise HTTPException(status_code=400, detail="User already exist")
    
    result = await db.execute(select(User).where(User.email == user.email))
    email = result.scalars().first()
    if email:
        raise HTTPException(status_code=400, detail="Email already has been utilized")

    hashed_password = hash_password(user.password)

    new_user = User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_password,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user
    
@router.post("/login")
async def login(form_data : OAuth2PasswordRequestForm = Depends(), db : AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == form_data.username))
    valid_username = result.scalars().first()
    if not valid_username:
        raise HTTPException(status_code=401,detail="Invalid credentials")
    correct_password = verify_password(form_data.password,valid_username.hashed_password)
    if not correct_password:
        raise HTTPException(status_code=401,detail="Invalid credentials")
    
    access_token = create_access_token(data = {"sub" : valid_username.username })

    return {"access_token" : access_token, "token_type" : "bearer"}

@router.get("/me",response_model = UserResponse)
async def get_me(user : User = Depends(get_current_user)):
    return user