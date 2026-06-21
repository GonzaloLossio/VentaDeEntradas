import bcrypt
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError,jwt
from datetime import datetime, timedelta,timezone
from app.database import get_db
from app.core.config import settings
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

def verify_password(password : str, hashed_password : str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'),hashed_password.encode('utf-8'))

def create_access_token(data : dict, expire_delta : timedelta | None = None) -> str:
    to_encode = data.copy()
    if expire_delta : 
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes = settings.access_token_expire_minutes) 
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,settings.secret_key,algorithm=settings.algorithm)
    return encoded_jwt

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token,settings.secret_key,algorithms=[settings.algorithm])
        return payload
    except JWTError:
        raise ValueError("Invalid Token")
        
async def get_current_user(token:str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token,settings.secret_key,algorithms=[settings.algorithm])
        username = payload.get("sub")
        if not username:
            raise ValueError()
    except (JWTError,ValueError):
        raise HTTPException(status_code=401,detail="Invalid Token")
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=401,detail="User not found")
    return user
    
async def get_admin_user(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail = "Access denied. Administrator privileges required.")    
    return user