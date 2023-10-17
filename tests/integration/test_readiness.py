"""Tests for readiness endpoints."""
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from config.config import HEALTHZ_PREFIX
from main_short import app


@pytest.mark.asyncio
class TestApi:
    """Class for testing API."""

    @pytest_asyncio.fixture(scope='module')
    async def test_client(self):
        """
        Фикстура для создания клиента для тестирования.

        Yields:
            TestClient: Клиент для тестирования.
        """
        yield TestClient(app)

    async def test_get_up(
        self,
        test_client,
    ):
        """
        Test for /healthz/up endpoint.

        Args:
            test_client (TestClient): Client for testing.
        """
        response = test_client.get(f'{HEALTHZ_PREFIX}/up')
        assert response.status_code == 200

    async def test_get_ready(
        self,
        test_client,
    ):
        """
        Test for /healthz/ready endpoint.

        Args:
            test_client (TestClient): Client for testing.
        """
        response = test_client.get(f'{HEALTHZ_PREFIX}/ready')
        assert response.status_code == 200
