import logging

from libgravatar import Gravatar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.schemas import UserSchema


async def get_user_by_email(email: str, db: AsyncSession) -> User:
    """
        Get a user by email.

        :param email: The email for the user.
        :type email: str
        :param db: The database session.
        :type db: AsyncSession
        :return: The user.
        :rtype: User
    """
    sq = select(User).filter_by(email=email)
    result = await db.execute(sq)
    user = result.scalar_one_or_none()
    logging.info(user)
    return user


async def create_user(body: UserSchema, db: AsyncSession) -> User:
    """
    Creates a new user.

    :param body: The data for the user to create.
    :type body: UserSchema
    :param db: The database session.
    :type db: AsyncSession
    :return: The newly created user.
    :rtype: User
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        logging.error(e)
    new_user = User(**body.model_dump(), avatar=avatar)  # User(username=username, email=email, password=password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession) -> None:
    """
        Update token for user who is login.

        :param user: The data for the user.
        :type user: User
        :param token: The token for user.
        :type token: str|None
        :param db: The database session.
        :type db: AsyncSession
        :return: The newly created user.
        :rtype: User
    """
    user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
    Confirmed email for registration user.

    :param email: The email for the user.
    :type email: str
    :param db: The database session.
    :type db: AsyncSession
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


async def update_avatar(email, url: str, db: AsyncSession) -> User:
    """
    Update avatar for user.

    :param email: The email for the user.
    :type email: str
    :param url: The url to image for the user.
    :type url: str
    :param db: The database session.
    :type db: AsyncSession
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    return user