"""Tests for shortener endpoints."""
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from main_short import app


@pytest.mark.asyncio
class TestApi:
    """Class for testing API."""

    @pytest_asyncio.fixture(scope='module')
    async def test_client(self):
        """
        Fixture for creating a client for testing.

        Yields:
            TestClient: Test client.
        """
        yield TestClient(app)

    async def test_get_short(
        self,
        test_client,
    ):
        """
        Test for /healthz/up endpoint.

        Args:
            test_client (TestClient): Client for testing.
        """
        add_data = {
            'long_url': 'https://example.com',
        }
        response = test_client.post(url='/api/short', params=add_data)
        assert response.status_code == 200

    async def test_get_long(
        self,
        test_client,
    ):
        """
        Test for /healthz/ready endpoint.

        Args:
            test_client (TestClient): Client for testing.
        """
        add_data = {
            'short_url': 'someShortCode',
        }
        response = test_client.get(url='/api/go', params=add_data)
        assert response.status_code == 200
