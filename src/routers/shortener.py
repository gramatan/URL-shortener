"""URL Shortener endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from starlette.status import (
    HTTP_307_TEMPORARY_REDIRECT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from src.services.shortener import ShortenerService

router = APIRouter()


@router.post('/short')
async def get_short_url(
    long_url: str,
    response: ShortenerService = Depends(),
):
    """
    Endpoint for creating short URL.

    Args:
        long_url: URL to be packed.
        response: Shortener service.

    Returns:
        str: short URL.

    Raises:
        HTTPException: If not URL was given.
    """
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
    response: ShortenerService = Depends(),
):
    """
    Endpoint for getting long URL.

    Args:
        short_url: URL to be decoded.
        response: ShortenerService.

    Returns:
        str: Long url.

    Raises:
        HTTPException: If short url not found.
    """
    long_url = await response.get_long(short_url=short_url)

    if long_url:
        return RedirectResponse(
            url=long_url,
            status_code=HTTP_307_TEMPORARY_REDIRECT,
        )

    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail='URL not found',
    )
