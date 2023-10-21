"""Simple readiness and liveness check endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.postgres_adaptor import get_db_session

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
async def readiness_check(
    check_db: AsyncSession = Depends(get_db_session),
):
    """
    Readiness check endpoint.

    Args:
        check_db (AsyncSession): Check db connection.

    Returns:
        str: OK.

    Raises:
        HTTPException: If db connection is not ok.
    """
    try:
        async with check_db as session:
            await session.execute(text('SELECT 1'))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='NOT OK',
        )
    return 'OK'
