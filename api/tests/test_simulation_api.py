import pytest

from api.models import PriceMovement

SIMULATION_API_URL = "operation/simulate"


@pytest.mark.django_db
class TestSimulationAPI:
    def test_price_movement_generation(self, api_client):
        pre_length = len(PriceMovement.objects.all())
        payload = {}
        api_client.post(f"/{SIMULATION_API_URL}/", payload)
        post_length = len(PriceMovement.objects.all())

        assert post_length == (pre_length + 100)
