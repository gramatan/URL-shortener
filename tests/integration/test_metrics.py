"""Тесты на проверку метрик."""
from fastapi.testclient import TestClient

from main_short import app

client = TestClient(app)

expected_metrics = [
    'gran_url_request_number',
    'gran_url_http_requests_total',
]


def test_metrics_endpoint():
    """Тест на проверку метрик."""
    response = client.get('/metrics')

    assert response.status_code == 200

    for metric in expected_metrics:
        assert metric in response.text, f'Metric {metric} not found in response'    # noqa: E501
