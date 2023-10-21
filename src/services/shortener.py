"""Services for URL Shortener."""
import validators
from fastapi import Depends

from src.repositories.short_repo import URLRepository


class ShortenerService:
    """Service for URL Shortener."""

    def __init__(
        self,
        url_repo: URLRepository = Depends(URLRepository),
    ):
        """
        Service for URL Shortener.

        Args:
            url_repo (URLRepository): URL Repository.
        """
        self.short_repo = url_repo

    async def get_short(
        self,
        long_url: str,
    ):
        """
        Save long url to the storage and return short url.

        Args:
            long_url: long url

        Returns:
            str: short url
        """
        if not validators.url(long_url):
            if not validators.url(f'http://{long_url}'):  # noqa: WPS504
                return None
            else:
                long_url = f'http://{long_url}'

        return await self.short_repo.store(long_url=long_url)

    async def get_long(
        self,
        short_url: str,
    ):
        """
        Get long url by the short url.

        Args:
            short_url: short url.

        Returns:
            str: long url.
        """
        return await self.short_repo.retrieve(short_url=short_url)
