import pytest
import json
from api.models import Company

COMPANY_API_URL = "companies"


@pytest.mark.django_db
class TestCompanyAPI:
    def test_create_company(self, api_client):
        payload = {
            "name": "B8 Technologies",
            "industry": "TECHONOLOGY",
            "ceo_name": "Vinicios Biluca",
            "description": "Always in pursuit of Happiness",
        }

        response = api_client.post(f"/{COMPANY_API_URL}/", payload)

        assert response.status_code <= 400

        new_company = Company.objects.get(name="B8 Technologies")
        assert new_company is not None

    def test_fail_create_company(self, api_client):
        payload = {}
        response = api_client.post(f"/{COMPANY_API_URL}/", payload)
        assert response.status_code == 400

    def test_retrieve_company(self, api_client, company):
        id = company.id
        response = api_client.get(f"/{COMPANY_API_URL}/{id}/")
        data = response.data

        assert response.status_code <= 400
        
        data_file = open("api/tests/scenarios/companies/001.json")
        expected_data = json.load(data_file)

        data.pop("id")
        assert data == expected_data

    def test_retrieve_companies(self, api_client):
        response = api_client.get(f"/{COMPANY_API_URL}/")
        data = response.data

        assert response.status_code <= 400
        assert len(data) >= 10

    def test_update_company(self, api_client, company):
        payload = {
            "name": "The Shire Corporation",
            "ceo_name": "Bilbo Baggins",
            "description": "Changing the World!",
            "industry": "TECHONOLOGY",
        }

        pre_update_company = Company.objects.get(id=company.id)
        assert pre_update_company.name == "B8 Technologies"
        assert pre_update_company.ceo_name == "Vinicios Biluca"
        assert pre_update_company.description == "Always in pursuit of Happiness"

        response = api_client.put(f"/{COMPANY_API_URL}/{company.id}/", payload)
        assert response.status_code <= 400

        post_updated_company = Company.objects.get(id=company.id)
        assert post_updated_company.name == "The Shire Corporation"
        assert post_updated_company.ceo_name == "Bilbo Baggins"
        assert post_updated_company.description == "Changing the World!"

    def test_failed_retrieve_company(self, api_client):
        response = api_client.get(f"/{COMPANY_API_URL}/123456789/")
        assert response.status_code == 404

    def test_delete_company(self, api_client, company):
        response = api_client.delete(f"/{COMPANY_API_URL}/{company.id}/")
        assert response.status_code <= 204

    def test_failed_delete_company(self, api_client):
        response = api_client.delete(f"/{COMPANY_API_URL}/123456789/")
        assert response.status_code == 404
