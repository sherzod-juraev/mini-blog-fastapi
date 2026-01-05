from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID


class ChatCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    title: str = Field(max_length=250)
    description: str | None = None


class ChatUpdateFull(BaseModel):
    model_config = ConfigDict(extra='forbid')
    title: str = Field(max_length=250)
    description: str


class ChatUpdatePartial(BaseModel):
    model_config = ConfigDict(extra='forbid')
    title: str | None = Field(None, max_length=250)
    description: str | None = None


class ChatRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    description: str | None = None