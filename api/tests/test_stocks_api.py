import pytest
import json
from api.models import Stock

STOCK_API_URL = "stocks"


@pytest.mark.django_db
class TestCompanyAPI:
    def test_create_stock(self, api_client, company):
        payload = {
            "company": company.id,
            "abbreviation": "XXX",
        }

        response = api_client.post(f"/{STOCK_API_URL}/", payload)

        assert response.status_code <= 400

        new_stock = Stock.objects.get(abbreviation="XXX")
        assert new_stock is not None

    def test_fail_create_stock(self, api_client):
        payload = {}
        response = api_client.post(f"/{STOCK_API_URL}/", payload)
        assert response.status_code == 400

    def test_retrieve_stocks(self, api_client):
        response = api_client.get(f"/{STOCK_API_URL}/")
        data = response.data

        assert response.status_code <= 400
        assert len(data) >= 10
    
    def test_retrieve_stock(self, api_client, stock):
        id = stock.id
        response = api_client.get(f"/{STOCK_API_URL}/{id}/")
        data = response.data

        assert response.status_code <= 400
        
        data_file = open("api/tests/scenarios/stocks/001.json")
        expected_data = json.load(data_file)

        data.pop("id")
        data.pop("company")
        assert data == expected_data

    def test_update_stock(self, api_client, company, stock):
        payload = {
            "abbreviation": "B8T",
            "company": company.id,
        }

        pre_update_stock = Stock.objects.get(id=stock.id)
        assert pre_update_stock.abbreviation == "VVV"

        response = api_client.put(f"/{STOCK_API_URL}/{stock.id}/", payload)
        assert response.status_code <= 400

        post_updated_stock = Stock.objects.get(id=stock.id)
        assert post_updated_stock.abbreviation == "B8T"

    def test_failed_retrieve_stock(self, api_client):
        response = api_client.get(f"/{STOCK_API_URL}/123456789/")
        assert response.status_code == 404

    def test_delete_stock(self, api_client, stock):
        response = api_client.delete(f"/{STOCK_API_URL}/{stock.id}/")
        assert response.status_code <= 204

    def test_failed_delete_stock(self, api_client):
        response = api_client.delete(f"/{STOCK_API_URL}/123456789/")
        assert response.status_code == 404
