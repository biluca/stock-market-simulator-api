from rest_framework.viewsets import ModelViewSet

from api.models import Owner, Stock, Portfolio, PriceMovement
from api.serializers import (
    OwnerSerializer,
    StockSerializer,
    PortfolioSerializer,
    PriceMovementSerializer,
)
from api.permissions import IsStockOwner


class OwnerView(ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class StockView(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class PortfolioView(ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

    permission_classes = [IsStockOwner] #### NOT WORKING!!!


class PriceMovementView(ModelViewSet):
    queryset = PriceMovement.objects.all()
    serializer_class = PriceMovementSerializer
