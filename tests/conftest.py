"""Conftest for all tests."""
import asyncio

import pytest


@pytest.fixture(scope='module')
def event_loop():
    """
    Фикстура для создания цикла событий.

    Yields:
        asyncio.AbstractEventLoop: Цикл событий.
    """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
