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
    """
    The get_contacts function returns a list of contacts.

    :param limit: int: Limit the number of contacts returned
    :param ge: Set a minimum value for the limit and offset parameters
    :param le: Limit the number of contacts returned
    :param offset: int: Specify the number of records to skip
    :param ge: Specify the minimum value of the limit parameter
    :param le: Set a maximum value for the limit parameter
    :param db: AsyncSession: Get the database connection from the dependency injection system
    :param user: User: Get the current user from the database
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(limit, offset, db, user)
    return contacts


@router.get("/all", response_model=List[ContactsResponse], dependencies=[Depends(access_to_all)])
async def get_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0, le=200),
                    db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts function returns a list of contacts.

    :param limit: int: Limit the number of contacts returned
    :param ge: Set a minimum value for the limit and offset parameters
    :param le: Limit the number of contacts returned
    :param offset: int: Specify the offset of the first contact to return
    :param ge: Specify the minimum value that can be passed in for a parameter
    :param le: Specify that the limit must be less than or equal to 500
    :param db: AsyncSession: Get the database session, which is passed to the repository
    :param user: User: Get the current user
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_all_contacts(limit, offset, db)
    return contacts

@router.get("/{contact_id}", response_model=ContactsResponse)
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact function returns a contact by its id.

    :param contact_id: int: Get the contact id from the path
    :param db: AsyncSession: Pass the database session to the repository
    :param user: User: Get the current user from the auth_service
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact


@router.post("/", response_model=ContactsResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactsSchema, db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactsSchema: Validate the request body
    :param db: AsyncSession: Pass the database session to the repository function
    :param user: User: Get the user that is currently logged in
    :return: A contact object, which is a pydantic model
    :doc-author: Trelent
    """
    contact = await repository_contacts.create_contact(body, db, user)
    return contact


@router.put("/{contact_id}", response_model=ContactsResponse)
async def update_contact(body: ContactsUpdateSchema, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes an id of the contact to be updated, and a body containing all fields that need to be updated.
        If no such contact exists, it returns 404 NOT FOUND.

    :param body: ContactsUpdateSchema: Validate the request body
    :param contact_id: int: Get the contact id from the url
    :param db: AsyncSession: Get the database session
    :param user: User: Get the current user from the auth_service
    :return: The updated contact
    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(contact_id, body, db, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactsResponse)
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    """
    The delete_contact function deletes a contact from the database.
        It takes in an integer representing the id of the contact to be deleted, and returns a dictionary containing information about that contact.

    :param contact_id: int: Get the contact id from the url
    :param db: AsyncSession: Get the database session
    :param user: User: Get the current user
    :return: The deleted contact
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return contact