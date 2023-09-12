from rest_framework import serializers
from api.models import Company, Stock, Portfolio, PriceMovement, Transaction
from django.contrib.auth.hashers import make_password


class CompanyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "ceo_name", "description", "industry"]


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "ceo_name"]


class StockSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField("get_price_movements")

    def get_price_movements(self, obj):
        last_price = PriceMovement.objects.get_stock_last_price(obj)
        return PriceMovementSerializer(last_price).data

    class Meta:
        model = Stock
        fields = ["id", "company", "abbreviation", "price"]


class StockSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["id", "company", "abbreviation"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class PortfolioSerializer(serializers.Serializer):
    stock_id = serializers.CharField()
    stock_abbreviation = serializers.CharField()
    total_quantity = serializers.IntegerField()


class PriceMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceMovement
        fields = [
            "id",
            "price",
            "created_at",
        ]


class OperationStockSerializer(serializers.Serializer):
    stock_abbreviation = serializers.CharField(write_only=True)
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(
        read_only=True, max_digits=14, decimal_places=2, coerce_to_string=False
    )
    transaction_amount = serializers.SerializerMethodField()
    stock = serializers.SerializerMethodField()

    def get_stock(self, obj):
        return StockSimpleSerializer(obj.stock).data

    def get_transaction_amount(self, obj):
        return obj.transaction_amount
