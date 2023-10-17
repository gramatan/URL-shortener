"""Readiness and liveness check endpoints."""
from fastapi import APIRouter
from starlette import status

router = APIRouter()


@router.get(
    '/up',
    status_code=status.HTTP_200_OK,
)
async def health_check():
    """
    Health check endpoint.

    Returns:
        str: OK.
    """
    return 'OK'


@router.get(
    '/ready',
    status_code=status.HTTP_200_OK,
)
async def readiness_check():
    """
    Readiness check endpoint.

    Returns:
        str: OK.
    """
    return 'OK'
