"""URL Shortener endpoints."""
from fastapi import APIRouter

from src.database.db import global_storage
from src.services.shortener import ShortenerService

router = APIRouter()


@router.post('/short')
async def get_short_url(
    long_url: str,
):
    """
    Endpoint for creating short URL.

    Args:
        long_url: URL to be packed.

    Returns:
        str: short URL.
    """
    response = ShortenerService(url_storage=global_storage)
    return await response.get_short(long_url=long_url)


@router.get('/go')
async def get_long_url(
    short_url: str,
):
    """
    Endpoint for getting long URL.

    Args:
        short_url: URL to be decoded.

    Returns:
        str: Long url.
    """
    response = ShortenerService(url_storage=global_storage)
    return await response.get_long(short_url=str(short_url))
