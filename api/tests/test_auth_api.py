import pytest

AUTH_API_URL = "login"


@pytest.mark.django_db
class TestAuthAPI:
    def test_login(self, api_client, user):
        payload = {"username": "frodo", "password": "theRing"}

        response = api_client.post(f"/{AUTH_API_URL}/", payload)
        data = response.data

        assert response.status_code == 200
        assert "access" in data

    def test_failed_login(self, api_client):
        payload = {"username": "dummy", "password": "12345"}
        response = api_client.post(f"/{AUTH_API_URL}/", payload)
        assert response.status_code == 401
