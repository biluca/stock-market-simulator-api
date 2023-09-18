from django.urls import path, include
from rest_framework import routers

from api.views import (
    WelcomeView,
    SimulateStockMartketView,
    CompanyView,
    StockView,
    PortfolioView,
    BuyStockView,
    SellStockView,
)

router = routers.DefaultRouter()
router.register(r"companies", CompanyView)
router.register(r"stocks", StockView)

urlpatterns = [
    path("", WelcomeView.as_view({"get": "welcome"}), name="welcome"),
    path("", include(router.urls)),
    path("operation/buy/", BuyStockView.as_view({"post": "buy"}), name="buy-stock"),
    path("operation/sell/", SellStockView.as_view({"post": "sell"}), name="sell-stock"),
    path(
        "operation/portfolio/",
        PortfolioView.as_view({"post": "get"}),
        name="sell-stock",
    ),
    path(
        "operation/simulate/",
        SimulateStockMartketView.as_view({"post": "simulate"}),
        name="simulate",
    ),
]
