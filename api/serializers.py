from rest_framework import serializers
from api.models import Company, User, Stock, Portfolio, PriceMovement
from django.contrib.auth.hashers import make_password


class CompanyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "ceo_name", "description", "description", "industry"]


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "ceo_name"]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "name",
            "cash",
            "is_staff",
            "last_login",
            "is_superuser",
        ]
    
    def create(self, validated_data):
        modified_data = self.make_password(validated_data)
        instance = User.objects.create(**modified_data)
        return instance
    
    def make_password(self, validated_data):
        hashed_password = str(make_password(validated_data["password"]))
        validated_data["password"] = hashed_password
        return validated_data



class StockSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField("get_price_movements")

    def get_price_movements(self, obj):
        last_price = PriceMovement.objects.get_stock_last_price(obj)
        return PriceMovementSerializer(last_price).data

    class Meta:
        model = Stock
        fields = ["id", "company", "abbreviation", "price"]


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = "__all__"


class PriceMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceMovement
        fields = [
            "id",
            "price",
            "created_at",
        ]


class BuyTransactionSerializer(serializers.Serializer):
    stock_abbreviation = serializers.CharField()
    quantity = serializers.IntegerField()


class SellTransactionSerializer(serializers.Serializer):
    stock_abbreviation = serializers.CharField()
    quantity = serializers.IntegerField()
    sell_all = serializers.BooleanField()
