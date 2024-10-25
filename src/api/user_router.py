from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schema.user_schema import UserRequestBody
from src.infrastructure.services.user_service import UserService
from src.infrastructure.repositories.user import UserRepository
from src.infrastructure.repositories.message import MessageRepository
from src.domain.models import User
from src.domain.exceptions.user import UserAlreadyExistsException, UserNotFoundException
from src.config import get_session

# FastAPI Router for user operations
user_router = APIRouter(prefix="", tags=["users"])


# Dependency injection for UserService
async def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(user_repository=UserRepository(session), message_repository=MessageRepository(session))


# POST: Create a new user
@user_router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserRequestBody, service: UserService = Depends(get_user_service)):
    try:
        created_user = await service.create_user(User(**user.dict()))
        return created_user
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# GET: Get a user by their email
@user_router.get("/email/{email}", response_model=Optional[User])
async def get_user_by_email(email: str, service: UserService = Depends(get_user_service)):
    user = await service.get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


# PATCH: Update a user's details
@user_router.patch("/{user_id}", response_model=User)
async def update_user(user_id: UUID, user: UserRequestBody, service: UserService = Depends(get_user_service)):
    try:
        updated_user = await service.update_user(user_id, User(**user.dict()))
        return updated_user
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# DELETE: Soft delete a user by their ID
@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    try:
        await service.delete_user(user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
