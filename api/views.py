from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from api.processors import StockBuyProcessor, StockSellProcessor

from api.models import Owner, Stock, Portfolio, PriceMovement
from api.serializers import (
    OwnerSerializer,
    StockSerializer,
    PortfolioSerializer,
    PriceMovementSerializer,
    BuyTransactionSerializer,
    SellTransactionSerializer,
)
from api.permissions import IsStockOwner, IsUserOwner


class OwnerView(ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class StockView(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    permission_classes = [permissions.IsAuthenticated, IsUserOwner]


class PortfolioView(ModelViewSet):
    permission_classes = [IsStockOwner, permissions.IsAuthenticated]

    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

    def get_queryset(self):
        user = self.request.user
        owner = Owner.objects.get(user=user)
        return self.queryset.filter(owner=owner)


class PriceMovementView(ModelViewSet):
    queryset = PriceMovement.objects.all()
    serializer_class = PriceMovementSerializer

    permission_classes = [permissions.IsAuthenticated, IsUserOwner]


class BuyStockView(GenericViewSet):
    serializer_class = BuyTransactionSerializer

    permission_classes = [permissions.IsAuthenticated, IsUserOwner]

    def buy(self, request, *args, **kwargs):
        processor = StockBuyProcessor()
        portfolio = processor.process(request)

        portfolioSerializer = PortfolioSerializer(portfolio)

        return Response(portfolioSerializer.data, status=status.HTTP_200_OK)


class SellStockView(GenericViewSet):
    serializer_class = SellTransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserOwner]

    def sell(self, request, *args, **kwargs):
        processor = StockSellProcessor()
        processor.process(request)

        return Response(status=status.HTTP_204_NO_CONTENT)
