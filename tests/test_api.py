import requests
import pytest

with open('tests/api_key.txt', 'r') as f:
    API_KEY = f.read().strip()

BASE_URL = 'http://localhost:5000'


@pytest.fixture
def headers():
    return {
        'x-api-key': API_KEY
    }


def test_get_logs(headers):
    response = requests.get(f'{BASE_URL}/api/logs', headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_items(headers):
    response = requests.get(f'{BASE_URL}/api/items', headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_invalid_api_key():
    fake_headers = {'x-api-key': 'invalidkey'}
    response = requests.get(f'{BASE_URL}/api/logs', headers=fake_headers)
    assert response.status_code == 403 or response.status_code == 401


def test_missing_api_key():
    response = requests.get(f'{BASE_URL}/api/logs')
    assert response.status_code == 401
