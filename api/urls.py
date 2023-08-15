from django.urls import path, include
from rest_framework import routers

from api.views import OwnerView, StockView, PortfolioView, PriceMovementView

router = routers.DefaultRouter()
router.register(r"owners", OwnerView)
router.register(r"stocks", StockView)
router.register(r"portfolio", PortfolioView)
router.register(r"prices", PriceMovementView)

urlpatterns = [
    path("", include(router.urls)),
]
