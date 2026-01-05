from re import match
from pydantic import BaseModel, ConfigDict, Field, field_validator
from fastapi import HTTPException, status
from uuid import UUID

username_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d\-]{1,50}$'
password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[-_])[A-Za-z\d\-_]{8,25}$'
full_name_pattern = r'[A-Za-z- ]{1,100}$'

def verify_field(
        pattern: str,
        value: str,
        value_type: str,
        /
) -> str:
    if not match(pattern, value):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'{value_type} invalid'
        )
    return value


class UserCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    username: str = Field(max_length=50)
    password: str = Field(min_length=8, max_length=25)


    @field_validator('username')
    def verify_username(cls, value):
        return verify_field(username_pattern, value, 'Username')


    @field_validator('password')
    def verify_password(cls, value):
        return verify_field(password_pattern, value, 'Password')


class UserUpdateFull(BaseModel):
    model_config = ConfigDict(extra='forbid')
    username: str = Field(max_length=50)
    password: str = Field(min_length=8, max_length=25)
    full_name: str = Field(max_length=100)


    @field_validator('username')
    def verify_username(cls, value):
        return verify_field(username_pattern, value, 'Username')


    @field_validator('password')
    def verify_password(cls, value):
        return verify_field(password_pattern, value, 'Password')


    @field_validator('full_name')
    def verify_full_name(cls, value):
        return verify_field(full_name_pattern, value, 'Full name')


class UserUpdatePartial(BaseModel):
    model_config = ConfigDict(extra='forbid')
    username: str | None = Field(None, max_length=50)
    password: str | None = Field(None, min_length=8, max_length=25)
    full_name: str | None = Field(None, max_length=100)


    @field_validator('username')
    def verify_username(cls, value):
        if value is None:
            return value
        return verify_field(username_pattern, value, 'Username')


    @field_validator('password')
    def verify_password(cls, value):
        if value is None:
            return value
        return verify_field(password_pattern, value, 'Password')


    @field_validator('full_name')
    def verify_full_name(cls, value):
        if value is None:
            return value
        return verify_field(full_name_pattern, value, 'Full name')


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    username: str
    full_name: str | None = None


class Token(BaseModel):
    model_config = ConfigDict(extra='forbid')
    access_token: str
    token_type: str = 'bearer'