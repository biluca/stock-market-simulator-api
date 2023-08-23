from rest_framework import serializers
from api.models import Owner, Stock, Portfolio, PriceMovement


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ["id", "name", "cash"]


class StockSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField("get_price_movements")

    def get_price_movements(self, obj):
        last_price = PriceMovement.objects.get_stock_last_price(obj)

        return PriceMovementSerializer(last_price).data

    class Meta:
        model = Stock
        fields = ["id", "company_name", "abbreviation", "price"]


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = "__all__"


class PriceMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceMovement
        fields = ["id", "price", "movement_amount", "percentual_change_friendly", "created_at"]


class BuyTransactionSerializer(serializers.Serializer):
    stock_abbreviation = serializers.CharField()
    quantity = serializers.IntegerField()


class SellTransactionSerializer(serializers.Serializer):
    stock_abbreviation = serializers.CharField()
    quantity = serializers.IntegerField()
    sell_all = serializers.BooleanField()
