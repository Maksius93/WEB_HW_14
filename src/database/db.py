import contextlib
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.conf.config import config


class Base(DeclarativeBase):
    pass


class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker | None = async_sessionmaker(autocommit=False,
                                                                            autoflush=False,
                                                                            expire_on_commit=False,
                                                                            bind=self._engine)

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """
        The session function is a coroutine that returns an asynchronous context manager.
        The context manager yields an AsyncSession object, which can be used to query the database.
        When the session function exits, it will automatically commit any changes made to the database and close the connection.

        :param self: Represent the instance of the object itself
        :return: An asynciterator
        :doc-author: Trelent
        """
        if self._session_maker is None:
            raise Exception("DatabaseSessionManager is not initialized")
        session = self._session_maker()
        try:
            yield session
        except Exception as err:
            print(err)
            await session.rollback()
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(config.sqlalchemy_database_url)


# Dependency
async def get_db():
    """
    The get_db function is a coroutine that returns an open database session.
    It will run the async with block, which ensures that the session will be closed when we are done with it.
    The yield from expression is similar to return in that it gives a value back to the caller of this function, but instead of immediately returning, it first suspends execution of this generator and yields control back to its caller.

    :return: A context manager that can be used to get a database connection
    :doc-author: Trelent
    """
    async with sessionmanager.session() as session:
        yield session