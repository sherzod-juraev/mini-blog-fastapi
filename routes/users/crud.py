from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from uuid import UUID
from core import security
from . import schemas
from .model import User


async def save(db: AsyncSession, /):
    try:
        await db.commit()
    except IntegrityError as ex:
        await db.rollback()
        err_msg = str(ex.orig)
        if 'ix_users_username' in err_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username already exists'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating user'
        )


async def create(db: AsyncSession, user_schema: schemas.UserCreate, /) -> User:

    user_model = User(
        username=user_schema.username,
        password=security.get_hash_password(user_schema.password)
    )
    db.add(user_model)
    await save(db)
    return user_model


async def read(db: AsyncSession, user_id: UUID, /) -> User:
    user_model = await db.get(User, user_id)
    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return user_model


async def update(
        db: AsyncSession,
        user_id: UUID,
        user_schema: schemas.UserUpdateFull | schemas.UserUpdatePartial,
        /, *,
        exclude_unset: bool = False
) -> User:
    user_model = await read(db, user_id)
    for field, value in user_schema.model_dump(exclude_unset=exclude_unset).items():
        if field != 'password':
            setattr(user_model, field, value)
        else:
            setattr(user_model, field, security.get_hash_password(value))
    await save(db)
    return user_model


async def verify_fields(
        user_model: User,
        user_schema: schemas.UserCreate,
        /
):
    username = user_model.username == user_schema.username
    if not username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username is wrong'
        )
    password = security.verify_password(user_schema.password, user_model.password)
    if not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Password is wrong'
        )


async def delete(
        db: AsyncSession,
        user_id: UUID,
        user_schema: schemas.UserCreate,
        /
):
    user_model = await read(db, user_id)
    await verify_fields(user_model, user_schema)
    await db.delete(user_model)
    try:
        await db.commit()
    except Exception as ex:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error deleting user'
        )