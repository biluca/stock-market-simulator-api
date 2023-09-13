import pytest

from api.models import User, Company, Stock, PriceMovement
from rest_framework.test import APIClient
from django.contrib.auth.hashers import make_password


@pytest.fixture()
def user():
    user_data = {
        "username": "frodo",
        "is_staff": True,
        "password": make_password("theRing"),
        "last_login": "2013-09-17 00:00:00",
        "is_superuser": True,
        "name": "Frodo Baggins",
        "cash": 999,
    }

    new_user, new = User.objects.get_or_create(**user_data)
    return new_user


@pytest.fixture()
def access_token(user):
    api_client = APIClient()
    payload = {"username": "frodo", "password": "theRing"}
    response = api_client.post("/login/", payload)
    data = response.data

    return data["access"]


@pytest.fixture
def api_client(access_token):
    api_client = APIClient()
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client


@pytest.fixture
def company():
    company_data = {
        "name": "B8 Technologies",
        "industry": "TECHONOLOGY",
        "ceo_name": "Vinicios Biluca",
        "description": "Always in pursuit of Happiness",
    }

    new_company, new = Company.objects.get_or_create(**company_data)
    return new_company


@pytest.fixture
def stock(company):
    stock_data = {
        "company": company,
        "abbreviation": "VVV",
    }

    new_stock, new = Stock.objects.get_or_create(**stock_data)
    return new_stock


@pytest.fixture
def stock_buy_sell(company):
    stock_data = {
        "company": company,
        "abbreviation": "BSS",
    }

    new_stock, new = Stock.objects.get_or_create(**stock_data)
    return new_stock


@pytest.fixture
def stock_price_movement(stock_buy_sell):
    price_movement_data = {
        "stock": stock_buy_sell,
        "price": 10.00,
    }

    new_price_movement, new = PriceMovement.objects.get_or_create(**price_movement_data)
    return new_price_movement
