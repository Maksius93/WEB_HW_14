import unittest
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User, Contact
from src.schemas import ContactsSchema, ContactsUpdateSchema
from src.repository.contacts import get_contacts, create_contact, update_contact, get_contact, get_all_contacts, remove_contact


class TestAsync(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)
        self.user = User(id=1, email="test@tes.com", password="qwerty", confirmed=True)

    async def test_get_contacts(self):
        limit = 10
        offset = 0
        expected_contacts = [Contact(), Contact(), Contact(), Contact()]
        mock_contacts = MagicMock()
        mock_contacts.scalars.return_value.all.return_value = expected_contacts
        self.session.execute.return_value = mock_contacts
        result = await get_contacts(limit, offset, self.session, self.user)
        self.assertEqual(result, expected_contacts)

    async def test_get_all_contacts(self):
        limit = 10
        offset = 0
        expected_contacts = [Contact(), Contact(), Contact(), Contact()]
        mock_contacts = MagicMock()
        mock_contacts.scalars.return_value.all.return_value = expected_contacts
        self.session.execute.return_value = mock_contacts
        result = await get_all_contacts(limit, offset, self.session)
        self.assertEqual(result, expected_contacts)

    async def test_get_contact(self):
        contact = Contact()
        mock_contact = MagicMock()
        mock_contact.scalar_one_or_none.return_value = contact
        self.session.execute.return_value = mock_contact
        result = await get_contact(contact.id, self.session, self.user)
        self.assertEqual(result, contact)

    async def test_create_todo(self):
        body = ContactsSchema(name="Test name", surname="Test surname", email="test@email.ue", phone="0568564575", bd="12-05-1996", city="Konotop", notes="Student")
        result = await create_contact(body, self.session, self.user)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.bd, body.bd)
        self.assertEqual(result.city, body.city)
        self.assertEqual(result.notes, body.notes)

    async def test_update_todo(self):
        body = ContactsUpdateSchema(name="Test name", surname="Test surname", email="test@email.ue", phone="0568564575", bd="12-05-1996", city="Konotop", notes="Student")
        contact = Contact(name="New name", surname="surname", email="test@ex.com", phone="0448564575", bd="12-08-1996", city="Poltava", notes="notes", user_id=self.user.id)

        mock_contact = MagicMock()
        mock_contact.scalar_one_or_none.return_value = contact
        self.session.execute.return_value = mock_contact

        result = await update_contact(contact.id, body, self.session, self.user)

        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.bd, body.bd)
        self.assertEqual(result.city, body.city)
        self.assertEqual(result.notes, body.notes)

    async def test_remove_contact(self):
        contact = Contact()
        mock_contact = MagicMock()
        mock_contact.scalar_one_or_none.return_value = contact
        self.session.execute.return_value = mock_contact
        result = await remove_contact(contact.id, self.session, self.user)
        self.assertEqual(result, contact)