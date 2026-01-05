from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from fastapi import HTTPException, status
from uuid import UUID
from .model import Chat
from . import schemas


async def save(db: AsyncSession, err_name: str, /):
    try:
        await db.commit()
    except IntegrityError as ex:
        await db.rollback()
        err_msg = str(ex.orig)
        if 'chats_user_id_fkey' in err_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Error {err_name} chat'
        )


async def create(
        db: AsyncSession,
        user_id: UUID,
        chat_schema: schemas.ChatCreate,
        /
) -> Chat:
    chat_model = Chat(
        title=chat_schema.title,
        description=chat_schema.description,
        user_id=user_id
    )
    db.add(chat_model)
    await save(db, 'creating')
    return chat_model


async def read(
        db: AsyncSession,
        chat_id: UUID,
        /
) -> Chat:
    chat_model = await db.get(Chat, chat_id)
    if chat_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Chat not found'
        )
    return chat_model


async def read_by_user_id(
        db: AsyncSession,
        user_id: UUID,
        skip: int,
        limit: int,
        /
) -> list[Chat]:
    query = select(Chat).where(
        Chat.user_id == user_id
    ).order_by(
        Chat.created_at.desc()
    ).offset(
        skip
    ).limit(
        limit
    )
    result = await db.execute(query)
    chat_model_list = result.scalars().all()
    return chat_model_list


async def update(
        db: AsyncSession,
        chat_id: UUID,
        chat_schema: schemas.ChatUpdateFull | schemas.ChatUpdatePartial,
        /, *,
        exclude_unset: bool = False
) -> Chat:
    chat_model = await read(db, chat_id)
    for field, value in chat_schema.model_dump(exclude_unset=exclude_unset).items():
        setattr(chat_model, field, value)
    await save(db, 'updating')
    return chat_model


async def delete(
        db: AsyncSession,
        chat_id: UUID,
        /
):
    chat_model = await read(db, chat_id)
    await db.delete(chat_model)
    await save(db, 'deleting')