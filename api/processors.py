from api.serializers import TransactionSerializer
from api.models import Stock, Owner, Portfolio
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from decimal import Decimal


class Processor:
    def process(self, request):
        raise NotImplementedError(
            f"You must use define a process implementation {__class__.__name__}"
        )


class StockBuyProcessor(Processor):
    def process(self, request):
        serializer = TransactionSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = request.user
            owner = self.find_and_validate_owner(user)
            stock_abbreviation = serializer.validated_data["stock_abbreviation"]
            stock = self.find_and_validate_stock(stock_abbreviation)
            quantity = serializer.validated_data["quantity"]

            data = {
                "owner": owner,
                "stock": stock,
                "quantity": quantity,
                "transaction_price": 9.99,
            }

            self.validate_owners_cash(data)
            portfolio = self.create_portfolio(data)
            self.update_owner_cash(data)

            return portfolio

    def validate_owners_cash(self, data):
        buy_total_amount = data.get("quantity") * data.get("transaction_price")
        ownwers_cash = data.get("owner").cash

        if buy_total_amount > ownwers_cash:
            raise ValidationError("Owner doest not have enough funds")

    def update_owner_cash(self, data):
        owner = data.get("owner")
        quantity = data.get("quantity")
        transaction_price = data.get("transaction_price")

        transaction_total_amount = quantity * transaction_price
        owner.cash = owner.cash - Decimal(transaction_total_amount)

        owner.save()

    def find_and_validate_stock(self, stock_abbreviation: str) -> Stock:
        try:
            return Stock.objects.get(abbreviation=stock_abbreviation)
        except:
            raise ValidationError("Stock not found")

    def find_and_validate_owner(self, user: User) -> Owner:
        try:
            return Owner.objects.get(user=user)
        except:
            raise ValidationError("Owner not found")

    def create_portfolio(self, data) -> Portfolio:
        portfolio = Portfolio.objects.create(**data)
        portfolio.save()

        return portfolio


class StockSellProcessor(Processor):
    def process(self, request):
        pass
