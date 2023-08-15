from rest_framework import serializers
from api.models import Owner, Stock, Portfolio, PriceMovement


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = "__all__"


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = "__all__"


class PriceMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceMovement
        fields = "__all__"


class TransactionSerializer(serializers.Serializer):
    stock_abbreviation = serializers.CharField()
    quantity = serializers.IntegerField()
