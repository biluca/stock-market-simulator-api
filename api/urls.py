from django.urls import path, include
from rest_framework import routers

from api.views import (
    SimulateStockMartketView,
    CompanyView,
    StockView,
    UserView
)

router = routers.DefaultRouter()
router.register(r"companies", CompanyView)
router.register(r"stocks", StockView)
router.register(r"users", UserView)
# router.register(r"portfolio", PortfolioView)
# router.register(r"prices", PriceMovementView)

urlpatterns = [
    path("", include(router.urls)),
    # path("operation/buy/", BuyStockView.as_view({"post": "buy"}), name="buy-stock"),
    # path('stocks/sell/', SellStockView.as_view(), name='sell-stock'),
    path(
        "operation/simulate/",
        SimulateStockMartketView.as_view({"post": "simulate"}),
        name="simulate",
    ),
]
