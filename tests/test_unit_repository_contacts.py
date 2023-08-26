import unittest
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User, Contact
from src.schemas import ContactsSchema, ContactsUpdateSchema
from src.repository.contacts import get_contacts, create_contact, update_contact, get_contact, get_all_contacts, remove_contact


class TestAsync(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        """
        The setUp function is called before each test function.
        It creates a new session and user object for each test.

        :param self: Represent the instance of the class
        :return: A mock session and a user object
        :doc-author: Trelent
        """
        self.session = AsyncMock(spec=AsyncSession)
        self.user = User(id=1, email="test@tes.com", password="qwerty", confirmed=True)

    async def test_get_contacts(self):
        """
        The test_get_contacts function tests the get_contacts function.
        It does this by mocking out the session object and returning a list of mock contacts.
        The test then asserts that the result of calling get_contacts is equal to expected_contacts.

        :param self: Access the class attributes and methods
        :return: The expected_contacts list
        :doc-author: Trelent
        """
        limit = 10
        offset = 0
        expected_contacts = [Contact(), Contact(), Contact(), Contact()]
        mock_contacts = MagicMock()
        mock_contacts.scalars.return_value.all.return_value = expected_contacts
        self.session.execute.return_value = mock_contacts
        result = await get_contacts(limit, offset, self.session, self.user)
        self.assertEqual(result, expected_contacts)

    async def test_get_all_contacts(self):
        """
        The test_get_all_contacts function tests the get_all_contacts function.
        It does this by mocking out the session object and setting up a mock return value for it.
        The test then calls get_all_contacts with some arguments, and asserts that the result is what we expect.

        :param self: Represent the instance of the class
        :return: A list of contacts
        :doc-author: Trelent
        """
        limit = 10
        offset = 0
        expected_contacts = [Contact(), Contact(), Contact(), Contact()]
        mock_contacts = MagicMock()
        mock_contacts.scalars.return_value.all.return_value = expected_contacts
        self.session.execute.return_value = mock_contacts
        result = await get_all_contacts(limit, offset, self.session)
        self.assertEqual(result, expected_contacts)

    async def test_get_contact(self):
        """
        The test_get_contact function tests the get_contact function.
        It does this by creating a mock contact, and then using that to create a mock session.
        The test then calls the get_contact function with the mocked session and user, which should return our mocked contact.

        :param self: Represent the instance of the class
        :return: The contact object
        :doc-author: Trelent
        """
        contact = Contact()
        mock_contact = MagicMock()
        mock_contact.scalar_one_or_none.return_value = contact
        self.session.execute.return_value = mock_contact
        result = await get_contact(contact.id, self.session, self.user)
        self.assertEqual(result, contact)

    async def test_create_contact(self):

        """
        The test_create_contact function tests the create_contact function.
            It creates a contact with the given parameters and checks if it was created correctly.

        :param self: Represent the instance of the class
        :return: A contact with the specified parameters
        :doc-author: Trelent
        """
        body = ContactsSchema(name="Test name", surname="Test surname", email="test@email.ue", phone="0568564575", bd="12-05-1996", city="Konotop", notes="Student")
        result = await create_contact(body, self.session, self.user)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.bd, body.bd)
        self.assertEqual(result.city, body.city)
        self.assertEqual(result.notes, body.notes)

    async def test_update_contact(self):

        """
        The test_update_contact function tests the update_contact function.
            The test_update_contact function creates a body, contact and mock object.
            The test_update_contact function then calls the update contact method with these objects as parameters.

        :param self: Represent the instance of the class
        :return: The contact object with updated fields
        :doc-author: Trelent
        """
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
        """
        The test_remove_contact function tests the remove_contact function.
        It does this by creating a mock contact, and then using that to test the remove_contact function.
        The result of running the remove_contact function should be equal to our mock contact.

        :param self: Represent the instance of the class
        :return: The contact that is removed
        :doc-author: Trelent
        """
        contact = Contact()
        mock_contact = MagicMock()
        mock_contact.scalar_one_or_none.return_value = contact
        self.session.execute.return_value = mock_contact
        result = await remove_contact(contact.id, self.session, self.user)
        self.assertEqual(result, contact)