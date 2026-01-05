from typing import Annotated
from fastapi import APIRouter, Query, Depends, status
from uuid import UUID
from database import get_db
from core.security import verify_access_token
from . import schemas, crud


chat_router = APIRouter()


@chat_router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ChatRead
)
async def create_chat(
        user_id: Annotated[UUID, Depends(verify_access_token)],
        chat_schema: schemas.ChatCreate,
        db=Depends(get_db)
):
    chat_model = await crud.create(db, user_id, chat_schema)
    return chat_model


@chat_router.put(
    '/{chat_id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.ChatRead,
    dependencies=[Depends(verify_access_token)]
)
async def full_update_chat(
        chat_id: UUID,
        chat_schema: schemas.ChatUpdateFull,
        db=Depends(get_db)
):
    chat_model = await crud.update(db, chat_id, chat_schema)
    return chat_model


@chat_router.patch(
    '/{chat_id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.ChatRead,
    dependencies=[Depends(verify_access_token)]
)
async def partial_update_chat(
        chat_id: UUID,
        chat_schema: schemas.ChatUpdatePartial,
        db=Depends(get_db)
):
    chat_model = await crud.update(db, chat_id, chat_schema, exclude_unset=True)
    return chat_model


@chat_router.get(
    '/{chat_id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.ChatRead,
    dependencies=[Depends(verify_access_token)]
)
async def get_chat(
        chat_id: UUID,
        db=Depends(get_db)
):
    chat_model = await crud.read(db, chat_id)
    return chat_model


@chat_router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.ChatRead]
)
async def get_chats_by_user_id(
        user_id: Annotated[UUID, Depends(verify_access_token)],
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        db=Depends(get_db)
):
    chat_model_list = await crud.read_by_user_id(db, user_id, skip, limit)
    return chat_model_list


@chat_router.delete(
    '/{chat_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_access_token)]
)
async def delete_chat(
        chat_id: UUID,
        db=Depends(get_db)
):
    await crud.delete(db, chat_id)