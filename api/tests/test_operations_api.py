import pytest

from api.models import User, Transaction
from decimal import Decimal

BUY_API_URL = "operation/buy"
SELL_API_URL = "operation/sell"
PORTFOLIO_API_URL = "operation/portfolio"


@pytest.mark.django_db()
class TestBuyStockOperation:
    @pytest.fixture()
    def fake_purchase(self, api_client, stock_buy_sell, user, stock_price_movement):
        payload = {"stock_abbreviation": "BSS", "quantity": 3}
        api_client.post(f"/{BUY_API_URL}/", payload)

    def test_buy_stock_generation(
        self, api_client, stock_buy_sell, user, stock_price_movement
    ):
        payload = {"stock_abbreviation": "BSS", "quantity": 3}
        response = api_client.post(f"/{BUY_API_URL}/", payload)

        assert response.status_code <= 400

        retrieved_user = User.objects.get(id=user.id)
        assert retrieved_user.cash == Decimal(969.00)

        retrieved_transaction = Transaction.objects.all().first()
        assert retrieved_transaction.transaction_amount == 30.00

    def test_wrong_buy_not_enough_funds_stock_generation(
        self, api_client, stock_buy_sell, user, stock_price_movement, fake_purchase
    ):
        payload = {"stock_abbreviation": "BSS", "quantity": 999}
        response = api_client.post(f"/{BUY_API_URL}/", payload)
        data = response.data

        assert response.status_code == 500
        assert "User does not have sufficient funds!" in data["error"]

    def test_wrong_stock_buy_stock_generation(
        self, api_client, stock_buy_sell, user, stock_price_movement, fake_purchase
    ):
        payload = {"stock_abbreviation": "XYZ", "quantity": 1}
        response = api_client.post(f"/{BUY_API_URL}/", payload)
        data = response.data

        assert response.status_code == 500
        assert "Stock Not Found!" in data["error"]

    def test_sell_stock_generation(
        self, api_client, stock_buy_sell, user, stock_price_movement, fake_purchase
    ):
        payload = {"stock_abbreviation": "BSS", "quantity": 3}
        response = api_client.post(f"/{SELL_API_URL}/", payload)

        assert response.status_code <= 400

        retrieved_user = User.objects.get(id=user.id)
        assert retrieved_user.cash == Decimal(999.00)

        retrieved_transaction = Transaction.objects.all().first()
        assert retrieved_transaction.transaction_amount == 30.00

    def test_wrong_sell_stock_generation(
        self, api_client, stock_buy_sell, user, stock_price_movement, fake_purchase
    ):
        payload = {"stock_abbreviation": "BSS", "quantity": 99}
        response = api_client.post(f"/{SELL_API_URL}/", payload)
        data = response.data

        assert response.status_code == 500
        assert "User does not Own that Quantity on the [BSS] Stock" in data["error"]

    def test_wrong_stock__sell_stock_generation(
        self, api_client, stock_buy_sell, user, stock_price_movement, fake_purchase
    ):
        payload = {"stock_abbreviation": "XYZ", "quantity": 1}
        response = api_client.post(f"/{SELL_API_URL}/", payload)
        data = response.data

        assert response.status_code == 500
        assert "Stock Not Found!" in data["error"]

    def test_portfolio(
        self, api_client, stock_buy_sell, user, stock_price_movement, fake_purchase
    ):
        response = api_client.post(f"/{PORTFOLIO_API_URL}/")
        data = response.data

        assert response.status_code <= 400
        assert len(data) > 0
