"""Repo for shortener."""
import secrets

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from config.config import SHORT_URL_LENGTH
from config.postgres_adaptor import get_db_session
from src.database.base import UserAlchemyModel


class URLRepository:
    """Repo for shortener."""

    def __init__(
        self,
        session: AsyncSession = Depends(get_db_session),
    ):
        """
        Repo for shortener.

        Args:
            session: session for db.
        """
        self.session = session

    async def store(self, long_url: str) -> str:
        """
        Store long url to storage and return short url.

        Args:
            long_url: long url.

        Returns:
            str: short url.
        """
        existing_url = await self.session.execute(
            select(UserAlchemyModel).filter_by(saved_url=long_url),
        )
        record = existing_url.scalar_one_or_none()

        if record:
            return record.token  # type: ignore

        token = await self._generate_token()
        new_url = UserAlchemyModel(token=token, saved_url=long_url)
        self.session.add(new_url)

        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            return await self.store(long_url)

        return token

    async def retrieve(self, short_url: str) -> str | None:
        """
        Retrieve long url by short url.

        Args:
            short_url: short url.

        Returns:
            str | None: long url or nothing.
        """
        is_existed = await self.session.execute(
            select(UserAlchemyModel).filter_by(token=short_url),
        )
        record = is_existed.scalar_one_or_none()

        if record:
            return record.saved_url

        return None

    async def _generate_token(self) -> str:
        """
        Generate a unique token.

        Returns:
            str: token.
        """
        while True:
            token = secrets.token_urlsafe(SHORT_URL_LENGTH)
            existing_token = await self.session.execute(
                select(UserAlchemyModel).filter_by(token=token),
            )
            if not existing_token.scalar_one_or_none():
                return token
