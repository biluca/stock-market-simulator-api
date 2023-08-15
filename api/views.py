from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status

from api.processors import StockPurchaseProcessor

from api.models import Owner, Stock, Portfolio, PriceMovement
from api.serializers import (
    OwnerSerializer,
    StockSerializer,
    PortfolioSerializer,
    PriceMovementSerializer,
    TransactionSerializer,
)
from api.permissions import IsStockOwner


class OwnerView(ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class StockView(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class PortfolioView(ModelViewSet):
    permission_classes = [IsStockOwner]

    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

    def get_queryset(self):
        user = self.request.user
        owner = Owner.objects.get(user=user)
        return self.queryset.filter(owner=owner)


class PriceMovementView(ModelViewSet):
    queryset = PriceMovement.objects.all()
    serializer_class = PriceMovementSerializer


class BuyStockView(GenericViewSet):
    serializer_class = TransactionSerializer

    def buy(self, request, *args, **kwargs):
        processor = StockPurchaseProcessor()
        portfolio = processor.process(request)

        portfolioSerializer = PortfolioSerializer(portfolio)

        return Response(portfolioSerializer.data, status=status.HTTP_201_CREATED)
