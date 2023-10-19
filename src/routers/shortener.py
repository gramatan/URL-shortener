"""URL Shortener endpoints."""
from fastapi import APIRouter

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
    return long_url


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
    return short_url
