"""Conftest for all tests."""
import asyncio

import asyncpg
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config.config import (
    POSTGRES_DB_NAME,
    POSTGRES_DB_PASS,
    POSTGRES_DB_USER,
    POSTGRES_HOST,
    POSTGRES_PORT,
)
from config.postgres_config import AppConfig, PostgresConfig
from src.database.base import Base

app_config = AppConfig(
    postgres=PostgresConfig(    # noqa: S106
        login=POSTGRES_DB_USER,
        password=POSTGRES_DB_PASS,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        db_name=f'{POSTGRES_DB_NAME}_test',
    ),
)


@pytest.fixture(scope='session')
def event_loop():
    """
    Фикстура для создания цикла событий.

    Yields:
        asyncio.AbstractEventLoop: Цикл событий.
    """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def config():
    """
    Фикстура для создания конфигурации приложения.

    Yields:
        AppConfig: Конфигурация приложения.
    """
    app_config.postgres.db_name = f'{app_config.postgres.db_name}'
    yield app_config


@pytest_asyncio.fixture(scope='session')
async def flush_db(config):
    """
    Фикстура для очистки БД.

    Args:
        config: конфигурация приложения
    """
    postgres_table_uri = f'postgresql://{app_config.postgres.url}/postgres'

    connection = await asyncpg.connect(postgres_table_uri)
    await connection.execute(f'DROP DATABASE IF EXISTS {app_config.postgres.db_name}')  # noqa: E501
    await connection.execute(f'CREATE DATABASE {app_config.postgres.db_name}')
    await connection.close()


@pytest_asyncio.fixture(scope='session')
async def db_engine(config):
    """
    Фикстура для создания подключения к БД.

    Args:
        config: конфигурация приложения

    Yields:
        Engine: Подключение к БД.
    """
    yield create_async_engine(config.postgres.uri, echo=True)


@pytest_asyncio.fixture(scope='session')
async def new_db_schema(flush_db, db_engine):
    """
    Фикстура для создания схемы БД.

    Args:
        flush_db: фикстура для очистки БД
        db_engine: фикстура для подключения к БД

    Yields:
        None
    """
    async with db_engine.begin() as first_connection:
        await first_connection.run_sync(Base.metadata.drop_all)

    async with db_engine.begin() as second_connection:
        await second_connection.run_sync(Base.metadata.create_all)
    yield
    await db_engine.dispose()


@pytest_asyncio.fixture(scope='session')
async def db_session(new_db_schema, db_engine):
    """
    Фикстура для создания сессии для работы с БД.

    Args:
        new_db_schema: фикстура для создания схемы БД
        db_engine: фикстура для подключения к БД

    Yields:
        AsyncSession: Сессия для работы с БД.
    """
    pg_session = async_sessionmaker(db_engine, expire_on_commit=False)
    async with pg_session() as session:
        yield session
        await session.rollback()
        await session.close()
