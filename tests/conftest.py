import asyncio

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from main import app
from src.database.db import Base, get_db
from src.database.models import User
from src.services.auth import auth_service

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.sqlite"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)

user = {
    "username": "ironman",
    "email": "ironman@example.com",
    "password": "123456789",
}


@pytest.fixture(scope="module", autouse=True)
def init_models_fixture():
    """
    The init_models_fixture function is a fixture that will be called before each test.
    It will create the database tables and insert a user into the database.

    :return: A function
    :doc-author: Trelent
    """
    async def init_models():
        """
        The init_models function is a fixture that will be run before each test.
        It creates the database tables and inserts an admin user into the database.

        :return: A coroutine, which is an object that can be awaited
        :doc-author: Trelent
        """
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        async with TestingSessionLocal() as session:
            user_hash = auth_service.get_password_hash(user.get("password"))
            current_user = User(
                username=user.get("username"),
                email=user.get("email"),
                password=user_hash,
                confirmed=True,
                role="admin",
            )
            session.add(current_user)
            await session.commit()

    asyncio.run(init_models())


@pytest.fixture(scope="module")
def client():
    """
    The client function is a fixture that will be called once per test file.
    It returns a TestClient instance, which is used to make HTTP requests in the tests.
    The app fixture provides access to the FastAPI application instance, and we use it here to override its get_db dependency with our own version of get_db that uses an in-memory SQLite database instead of PostgreSQL.

    :return: A test client for the app
    :doc-author: Trelent
    """
    async def override_get_db():
        """
        The override_get_db function is a fixture that will be called by pytest before each test.
        It creates a new database session for the test to use and handles rolling back transactions and closing connections.

        :return: A context manager, which is a special kind of object that supports the with statement
        :doc-author: Trelent
        """
        session = TestingSessionLocal()
        try:
            yield session
        except Exception as err:
            print(err)
            await session.rollback()
        finally:
            await session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture(scope="module")
def get_token(client):
    """
    The get_token function is used to get a token for the user.
    It uses the client object to make a POST request to /auth/login with the username and password of our test user.
    The response should be 200, meaning that it was successful, and we can then return data[&quot;access_token&quot;] which is
    the access token returned by our API.

    :param client: Make requests to the application
    :return: The token for the user
    :doc-author: Trelent
    """
    response = client.post(
        "/auth/login",
        data={
            "username": user.get("email"),
            "password": user.get("password"),
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    return data["access_token"]


@pytest_asyncio.fixture()
async def get_token_simple(client):
    """
    The get_token_simple function is a helper function that creates an access token for the user.
        It uses the auth_service to create an access token with data containing the user's email address.

    :param client: Get the client_id of the client that is requesting a token
    :return: A jwt token
    :doc-author: Trelent
    """
    access_token = await auth_service.create_access_token(
        data={"sub": user.get("email")}
    )
    return access_token