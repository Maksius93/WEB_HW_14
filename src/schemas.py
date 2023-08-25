from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: str
    avatar: str

    class Config:
        from_attributes = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ContactsSchema(BaseModel):
    name: str = Field(max_length=50, min_length=3)
    surname: str = Field(max_length=100, min_length=3)
    email: str = Field(max_length=50, min_length=3)
    phone: str = Field(max_length=20, min_length=5)
    bd: str
    city: str = Field(max_length=50, min_length=3)
    notes: str = Field(max_length=300, min_length=3)


class ContactsUpdateSchema(ContactsSchema):
    pass


class ContactsResponse(BaseModel):
    id: int = 1
    name: str
    surname: str
    email: str
    phone: str
    bd: str
    city: str
    notes: str
    created_at: datetime | None
    updated_at: datetime | None
    user: UserResponseSchema | None


    class Config:
        from_attributes = True