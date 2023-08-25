from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact, User
from src.schemas import ContactsSchema, ContactsUpdateSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession, user: User):
    """
        Retrieves a list of notes for a specific user with specified pagination parameters.

        :param offset: The number of contacts to skip.
        :type offset: int
        :param limit: The maximum number of contacts to return.
        :type limit: int
        :param user: The user to retrieve contacts for.
        :type user: User
        :param db: The database session.
        :type db: AsyncSession
        :return: A list of contacts.
        :rtype: List[Contacts]
    """
    sq = select(Contact).filter_by(user=user).offset(offset).limit(limit)
    contacts = await db.execute(sq)
    return contacts.scalars().all()


async def get_all_contacts(limit: int, offset: int, db: AsyncSession):
    """
        Retrieves a list of notes for a specific user with specified pagination parameters.

        :param offset: The number of contacts to skip.
        :type offset: int
        :param limit: The maximum number of contacts to return.
        :type limit: int
        :param db: The database session.
        :type db: AsyncSession
        :return: A list of contacts.
        :rtype: List[Contacts]
    """
    sq = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(sq)
    return contacts.scalars().all()


async def get_contact(contacts_id: int, db: AsyncSession, user: User):
    """
        Retrieves a single note with the specified ID for a specific user.

    :param contacts_id: The ID of the contact to retrieve.
    :type contacts_id: int
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: AsyncSession
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Contact | None
    """
    sq = select(Contact).filter_by(id=contacts_id, user=user)
    contact = await db.execute(sq)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactsSchema, db: AsyncSession, user: User):
    """
        Creates a new contact for a specific user.

        :param body: The data for the contact to create.
        :type body: ContactModel
        :param user: The user to create the contact for.
        :type user: User
        :param db: The database session.
        :type db: AsyncSession
        :return: The newly created contact.
        :rtype: Contact
    """
    contact = Contact(name=body.name, surname=body.surname, email=body.email, phone=body.phone, bd=body.bd, city=body.city, notes=body.notes, user=user)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactsUpdateSchema, db: AsyncSession, user: User):
    """
    Removes a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param body: The updated data for the contact.
    :type body: ContactUpdate
    :param user: The user to update the note for.
    :type user: User
    :param db: The database session.
    :type db: AsyncSession
    :return: The updated contact, or None if it does not exist.
    :rtype: Contact | None
    """
    sq = select(Contact).filter_by(id=contact_id, user=user)
    result = await db.execute(sq)
    contact = result.scalar_one_or_none()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.bd = body.bd
        contact.city = body.city
        contact.notes = body.notes
        await db.commit()
        await db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: AsyncSession, user: User):
    """
       Removes a single note with the specified ID for a specific user.

       :param contact_id: The ID of the contact to remove.
       :type contact_id: int
       :param user: The user to remove the contact for.
       :type user: User
       :param db: The database session.
       :type db: AsyncSession
       :return: The removed contact, or None if it does not exist.
       :rtype: Contact | None
    """
    sq = select(Contact).filter_by(id=contact_id, user=user)
    result = await db.execute(sq)
    contact = result.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact