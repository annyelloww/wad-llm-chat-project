from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.db.models import Chat, Message, User
from app.llm.service import ask_llm
async def list_chats(db:AsyncSession, user:User)->list[Chat]:
    result=await db.execute(select(Chat).where(Chat.owner_id==user.id).order_by(Chat.created_at.desc()))
    return list(result.scalars().all())
async def create_chat(db:AsyncSession, user:User, title:str)->Chat:
    chat=Chat(title=title or 'new chat', owner_id=user.id); db.add(chat); await db.commit(); await db.refresh(chat); return chat
async def get_chat(db:AsyncSession, user:User, chat_id:int)->Chat:
    result=await db.execute(select(Chat).options(selectinload(Chat.messages)).where(Chat.id==chat_id, Chat.owner_id==user.id))
    chat=result.scalar_one_or_none()
    if not chat: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='chat not found')
    return chat
async def add_message_and_answer(db:AsyncSession, user:User, chat_id:int, content:str)->list[Message]:
    chat=await get_chat(db,user,chat_id)
    user_message=Message(chat_id=chat.id, role='user', content=content); db.add(user_message); await db.commit(); await db.refresh(user_message)
    answer=ask_llm(content); assistant_message=Message(chat_id=chat.id, role='assistant', content=answer); db.add(assistant_message); await db.commit(); await db.refresh(assistant_message)
    return [user_message, assistant_message]
async def save_streamed_exchange(db:AsyncSession, user:User, chat_id:int, user_content:str, assistant_content:str)->None:
    chat=await get_chat(db,user,chat_id); db.add(Message(chat_id=chat.id, role='user', content=user_content)); db.add(Message(chat_id=chat.id, role='assistant', content=assistant_content)); await db.commit()
