from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Request, Response, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from uuid import UUID
from core import security, get_setting
from database import get_db
from . import schemas, crud


user_router = APIRouter()
settings = get_setting()


@user_router.post(
    '/signup',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Token
)
async def create_user(
        response: Response,
        oauth_form: Annotated[OAuth2PasswordRequestForm, Depends()],
        db=Depends(get_db)
):
    user_schema = schemas.UserCreate(
        username=oauth_form.username,
        password=oauth_form.password
    )
    user_model = await crud.create(db, user_schema)
    response.set_cookie(
        key='refresh_token',
        value=security.create_refresh_token(user_model.id),
        max_age=60 * 60 * 24 * settings.rt_days,
        expires=datetime.now(timezone.utc) + timedelta(days=settings.rt_days)
    )
    token = schemas.Token(access_token=security.create_access_token(user_model.id))
    return token


@user_router.post(
    '/refresh',
    status_code=status.HTTP_200_OK,
    response_model=schemas.Token
)
async def update_token(
        request: Request,
        response: Response
):
    refresh_token = request.cookies.get('refresh_token')
    user_id = security.verify_refresh_token(refresh_token)
    response.set_cookie(
        key='refresh_token',
        value=security.create_refresh_token(user_id),
        max_age=60 * 60 * 24 * settings.rt_days,
        expires=datetime.now(timezone.utc) + timedelta(days=settings.rt_days)
    )
    token = schemas.Token(access_token=security.create_access_token(user_id))
    return token


@user_router.put(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserRead
)
async def full_update_user(
        user_id: Annotated[UUID, Depends(security.verify_access_token)],
        user_schema: schemas.UserUpdateFull,
        db=Depends(get_db)
):
    user_model = await crud.update(db, user_id, user_schema)
    return user_model


@user_router.patch(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserRead,
)
async def partial_update_user(
        user_id: Annotated[UUID, Depends(security.verify_access_token)],
        user_schema: schemas.UserUpdatePartial,
        db=Depends(get_db)
):
    user_model = await crud.update(db, user_id, user_schema, exclude_unset=True)
    return user_model


@user_router.get(
    '/me',
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserRead
)
async def read_user(
        user_id: Annotated[UUID, Depends(security.verify_access_token)],
        db=Depends(get_db)
):
    user_model = await crud.read(db, user_id)
    return user_model


@user_router.delete(
    '/',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
        response: Response,
        user_id: Annotated[UUID, Depends(security.verify_access_token)],
        user_schema: schemas.UserCreate,
        db=Depends(get_db)
):
    await crud.delete(db, user_id, user_schema)
    response.delete_cookie(key='refresh_token')