"""URL Shortener endpoints."""
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from starlette.status import (
    HTTP_307_TEMPORARY_REDIRECT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

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

    Raises:
        HTTPException: If not URL was given.
    """
    response = ShortenerService(url_storage=global_storage)
    short_url = await response.get_short(long_url=long_url)

    if short_url is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Invalid URL provided',
        )

    return short_url


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

    Raises:
        HTTPException: If short url not found.
    """
    service = ShortenerService(url_storage=global_storage)
    long_url = await service.get_long(short_url=short_url)

    if long_url:
        return RedirectResponse(
            url=long_url,
            status_code=HTTP_307_TEMPORARY_REDIRECT,
        )

    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail='URL not found',
    )
