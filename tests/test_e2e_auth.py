from unittest.mock import MagicMock

import pytest
from sqlalchemy import select

from src.database.models import User
from tests.conftest import TestingSessionLocal

user_mock = {
    "username": "ironman",
    "email": "ironman@ex.com",
    "password": "123456",
}


def test_create_user(client, monkeypatch):
    """
    The test_create_user function tests the creation of a new user.
    It uses the client fixture to make a POST request to /auth/signup with some mock data.
    The response is then checked for status code 201 and that it contains an email, username, and avatar.

    :param client: Make requests to the api
    :param monkeypatch: Mock the send_email function
    :return: The user created
    :doc-author: Trelent
    """
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.services.email.send_email", mock_send_email)
    response = client.post("/auth/signup", json=user_mock)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data.get("email") == user_mock.get("email")
    assert data.get("username") == user_mock.get("username")
    assert "avatar" in data


def test_repeat_create_user(client, monkeypatch):
    """
    The test_repeat_create_user function tests that a user cannot be created twice.
    It does this by first mocking the send_email function, which is called when a new user is created.
    Then it creates a new user with the client object and asserts that the response status code is 409 (Conflict).
    Finally, it asserts that the detail field of data returned in JSON format matches what we expect.

    :param client: Make requests to the flask application
    :param monkeypatch: Mock the send_email function
    :return: A 409 error, which is the same as the test_create_user function
    :doc-author: Trelent
    """
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.services.email.send_email", mock_send_email)
    response = client.post("/auth/signup", json=user_mock)
    assert response.status_code == 409, response.text
    data = response.json()
    assert data.get("detail") == "Account already exists"


def test_login_user_not_confirmed(client, monkeypatch):
    """
    The test_login_user_not_confirmed function tests that a user cannot login if they have not confirmed their email.
    The test_login_user_not_confirmed function uses the client fixture to make a POST request to the /auth/login endpoint with
    the username and password of an unconfirmed user. The test asserts that the response status code is 401, which means
    unauthorized access, and then asserts that the detail key in data is equal to &quot;Email not confirmed&quot;. This confirms
    that users who have not confirmed their email address are unable to login.

    :param client: Make requests to the flask application
    :param monkeypatch: Mock the send_email function
    :return: A 401 status code and an error message
    :doc-author: Trelent
    """
    response = client.post(
        "/auth/login",
        data={
            "username": user_mock.get("email"),
            "password": user_mock.get("password"),
        },
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data.get("detail") == "Email not confirmed"


@pytest.mark.asyncio
async def test_login_user(client, monkeypatch):
    """
    The test_login_user function tests the login endpoint.
    It first creates a user in the database, then it logs in with that user's credentials and checks if an access token is returned.

    :param client: Make requests to the api
    :param monkeypatch: Patch the function that is called in the test
    :return: A 200 status code with a bearer token
    :doc-author: Trelent
    """
    async with TestingSessionLocal() as session:
        current_user = await session.execute(select(User).filter(User.email == user_mock.get('email')))
        current_user = current_user.scalar_one_or_none()
        current_user.confirmed = True
        await session.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": user_mock.get("email"),
            "password": user_mock.get("password"),
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password_user(client, monkeypatch):
    """
    The test_login_wrong_password_user function tests the login endpoint with a wrong password.
    It should return a 401 status code and an error message.

    :param client: Make requests to the flask application
    :param monkeypatch: Mock the user_mock
    :return: A 401 status code and an error message
    :doc-author: Trelent
    """
    response = client.post(
        "/auth/login",
        data={
            "username": user_mock.get("email"),
            "password": "password",
        },
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data.get("detail") == "Invalid password"


def test_login_wrong_email_user(client, monkeypatch):

    """
    The test_login_wrong_email_user function tests the login endpoint with a wrong email.
        It should return a 401 status code and an error message.

    :param client: Make requests to the flask application
    :param monkeypatch: Mock the login function
    :return: The status code 401 and the message &quot;invalid email&quot;
    :doc-author: Trelent
    """
    response = client.post(
        "/auth/login",
        data={
            "username": "email@email.com",
            "password": user_mock.get("password"),
        },
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data.get("detail") == "Invalid email"


def test_login_validation_user(client, monkeypatch):

    """
    The test_login_validation_user function tests that the login endpoint returns a 422 status code when
    the user does not provide a username. The test also asserts that the response contains an error message.

    :param client: Make a request to the flask application
    :param monkeypatch: Mock the function get_user_by_email
    :return: A 422 status code and a &quot;detail&quot; key in the data
    :doc-author: Trelent
    """
    response = client.post(
        "/auth/login",
        data={
            "password": user_mock.get("password"),
        },
    )
    assert response.status_code == 422, response.text
    data = response.json()
    assert "detail" in data