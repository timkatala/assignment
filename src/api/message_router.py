from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schema.message_schema import MessageRequestBody
from src.infrastructure.repositories.message import MessageRepository
from src.infrastructure.repositories.user import UserRepository
from src.infrastructure.services.message_service import MessageService
from src.domain.models import Message
from src.domain.exceptions.user import UserNotFoundException
from src.domain.exceptions.message import MessageNotFoundException
from src.config import get_session

message_router = APIRouter(prefix="", tags=["messages"])


async def get_message_service(session: AsyncSession = Depends(get_session)) -> MessageService:
    return MessageService(user_repository=UserRepository(session), message_repository=MessageRepository(session))


# POST: Create a new message
@message_router.post("/", response_model=Message, status_code=status.HTTP_201_CREATED)
async def create_message(message: MessageRequestBody, service: MessageService = Depends(get_message_service)):
    try:
        created_message = await service.create_message(Message(**message.dict()))
        return created_message
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# GET: Get messages sent by a particular user
@message_router.get("/sender/{sender_id}", response_model=List[Message])
async def get_messages_by_sender_id(sender_id: UUID, service: MessageService = Depends(get_message_service)):
    messages = await service.get_mesages_by_sender_id(sender_id)
    return messages


# DELETE: Soft delete a message by its ID
@message_router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(message_id: UUID, service: MessageService = Depends(get_message_service)):
    try:
        await service.delete_message(message_id)
    except MessageNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
