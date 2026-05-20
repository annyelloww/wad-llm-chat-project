from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import decode_access_token
from app.db.models import User
from app.db.session import get_db
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='/api/auth/login')
async def get_current_user(token:str=Depends(oauth2_scheme), db:AsyncSession=Depends(get_db))->User:
    user_id=decode_access_token(token)
    if not user_id: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid access token')
    user=await db.get(User, user_id)
    if not user: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not found')
    return user
