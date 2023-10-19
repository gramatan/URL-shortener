"""Tests for shortener endpoints."""
import pytest
from fastapi.testclient import TestClient

from main_short import app


@pytest.mark.asyncio
class TestApi:
    """Class for testing API."""

    @pytest.fixture(scope='class')
    def test_client(self):
        """
        Fixture for creating a client for testing.

        Yields:
            Test client.
        """
        yield TestClient(app)

    @pytest.mark.parametrize(
        'long_url, expected_status',
        [
            pytest.param('https://example.com', 200, id='Valid URL'),
            pytest.param('example.com', 200, id='No schema, still valid'),
            pytest.param('not_a_url', 400, id='Invalid URL'),
            pytest.param(' ', 400, id='Just a space'),
        ],
    )
    async def test_get_short(self, test_client, long_url, expected_status):
        """
        Test for /api/short endpoint.

        Args:
            test_client (TestClient): Client for testing.
            long_url: Long url to be shortened.
            expected_status: Expected status.
        """
        response = test_client.post(url=f'/api/short?long_url={long_url}')
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        'short_url, expected_status',
        [
            pytest.param('99999', 404, id='URL not found'),
            pytest.param('notAnIndex', 404, id='Not a valid index'),
        ],
    )
    async def test_get_long(self, test_client, short_url, expected_status):
        """
        Test for /api/go endpoint.

        Args:
            test_client (TestClient): Client for testing.
            short_url: Short url to be decoded.
            expected_status: Expected status.
        """
        response = test_client.get(url=f'/api/go?short_url={short_url}')
        assert response.status_code == expected_status
