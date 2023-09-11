from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import permissions

from django.contrib.auth.models import User as DjangoUser

from api.processors import (
    BuyStockProcessor,
    SellStockProcessor,
    StockDataSimulationProcessor,
)

from api.models import User, Stock, Portfolio, PriceMovement, Company
from api.serializers import (
    CompanyDetailSerializer,
    UserSerializer,
    StockSerializer,
    PortfolioSerializer,
    OperationStockSerializer,
)
from api.const import HTTP_METHODS


class ListDetailModelViewSet(ModelViewSet):
    detail_serializer_class = None
    list_serializer_class = None

    def get_serializer_class(self):
        if self.serializer_class is not None:
            return self.serializer_class

        has_detail_serializer_class = self.detail_serializer_class is not None
        has_list_serializer_class = self.list_serializer_class is not None

        validation_message = f"{self.__class__.__name__} should either include a `detail_serializer_class` attribute and a `list_serializer_class` attribute, or a `serializer_class` attribute, or override the `get_serializer_class()` method."
        assert (
            has_detail_serializer_class and has_list_serializer_class
        ), validation_message

        if self.kwargs.get("pk"):
            return self.detail_serializer_class
        return self.list_serializer_class


class SimulateStockMartketView(GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def simulate(self, request, *args, **kwargs):
        processor = StockDataSimulationProcessor()
        processor.process(request)

        return Response(status=status.HTTP_204_NO_CONTENT)


class CompanyView(ListDetailModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanyDetailSerializer

    permission_classes = [permissions.IsAuthenticated]


class StockView(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    permission_classes = [permissions.IsAuthenticated]


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [permissions.IsAuthenticated]


class PortfolioView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

    def get_queryset(self):
        user = User.objects.get(id=self.request.user.id)
        return self.queryset.filter(user=user)


class BuyStockView(GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def buy(self, request, *args, **kwargs):
        processor = BuyStockProcessor()
        transaction = processor.process(request)

        serializer = OperationStockSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SellStockView(GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def sell(self, request, *args, **kwargs):
        processor = SellStockProcessor()
        transaction = processor.process(request)

        serializer = OperationStockSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class PriceMovementView(ModelViewSet):
#     queryset = PriceMovement.objects.all()
#     serializer_class = PriceMovementSerializer

#     permission_classes = [permissions.IsAuthenticated, IsUserOwner]


# class SellStockView(GenericViewSet):
#     serializer_class = SellTransactionSerializer
#     permission_classes = [permissions.IsAuthenticated, IsUserOwner]

#     def sell(self, request, *args, **kwargs):
#         processor = StockSellProcessor()
#         processor.process(request)

#         return Response(status=status.HTTP_204_NO_CONTENT)
