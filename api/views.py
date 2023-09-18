from rest_framework import renderers
from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions


from api.processors import (
    BuyStockProcessor,
    SellStockProcessor,
    StockDataSimulationProcessor,
)

from api.models import User, Stock, Portfolio, Company
from api.serializers import (
    CompanyDetailSerializer,
    DetailStockSerializer,
    ListStockSerializer,
    PortfolioSerializer,
    OperationStockSerializer,
)

class WelcomeView(GenericViewSet):
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'working.html'

    def welcome(self, request, *args, **kwargs):
        return render(request, self.template_name)

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


class StockView(ListDetailModelViewSet):
    queryset = Stock.objects.all()
    detail_serializer_class = DetailStockSerializer
    list_serializer_class = ListStockSerializer

    permission_classes = [permissions.IsAuthenticated]


class PortfolioView(GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PortfolioSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        user = User.objects.get(id=user.id)
        summary = Portfolio.objects.get_portfolio_summary(user)

        serializer = PortfolioSerializer(summary)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BuyStockView(GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def buy(self, request, *args, **kwargs):
        try:
            processor = BuyStockProcessor()
            transaction = processor.process(request)

            serializer = OperationStockSerializer(transaction)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            error_data = {
                "error": str(error),
            }
            return Response(error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SellStockView(GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def sell(self, request, *args, **kwargs):
        try:
            processor = SellStockProcessor()
            transaction = processor.process(request)

            serializer = OperationStockSerializer(transaction)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as error:
            error_data = {
                "error": str(error),
            }
            return Response(error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
