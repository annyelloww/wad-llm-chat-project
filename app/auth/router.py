from fastapi import APIRouter, Depends, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.service import authenticate_user, github_callback, github_login_url, issue_tokens, logout, refresh_tokens, register_user
from app.db.session import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, TokenPair
router=APIRouter(prefix='/auth', tags=['auth'])
@router.post('/register', response_model=TokenPair)
async def register(payload:RegisterRequest, db:AsyncSession=Depends(get_db)):
    user=await register_user(db, payload.login, payload.password); return issue_tokens(user.id)
@router.post('/login', response_model=TokenPair)
async def login(payload:LoginRequest, db:AsyncSession=Depends(get_db)):
    user=await authenticate_user(db, payload.login, payload.password); return issue_tokens(user.id)
@router.post('/refresh', response_model=TokenPair)
async def refresh(refresh_token:str=Query(...)): return refresh_tokens(refresh_token)
@router.post('/logout')
async def logout_route(refresh_token:str=Query(...)): logout(refresh_token); return {'status':'ok'}
@router.get('/github/login')
async def github_login(): return RedirectResponse(github_login_url())
@router.get('/github/callback')
async def github_oauth_callback(code:str, db:AsyncSession=Depends(get_db)):
    tokens=await github_callback(db, code); return RedirectResponse(f"/?access_token={tokens['access_token']}&refresh_token={tokens['refresh_token']}")
