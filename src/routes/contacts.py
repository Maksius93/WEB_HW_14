from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas import ContactsResponse, ContactsSchema, ContactsUpdateSchema
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service
from src.services.roles import RoleAccess

router = APIRouter(prefix='/contacts', tags=["contacts"])
access_to_all = RoleAccess([Role.admin, Role.moderator])


@router.get("/", response_model=List[ContactsResponse])
async def get_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0, le=200),
                    db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(limit, offset, db, user)
    return contacts


@router.get("/all", response_model=List[ContactsResponse], dependencies=[Depends(access_to_all)])
async def get_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0, le=200),
                    db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_all_contacts(limit, offset, db)
    return contacts

@router.get("/{contact_id}", response_model=ContactsResponse)
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact


@router.post("/", response_model=ContactsResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactsSchema, db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.create_contact(body, db, user)
    return contact


@router.put("/{contact_id}", response_model=ContactsResponse)
async def update_contact(body: ContactsUpdateSchema, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, db, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactsResponse)
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact