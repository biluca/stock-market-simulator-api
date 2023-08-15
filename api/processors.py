from api.serializers import TransactionSerializer
from api.models import Stock, Owner, Portfolio
from django.contrib.auth.models import User


class Processor:
    def process(self, request):
        raise NotImplementedError(
            f"You must use define a process implementation {__class__.__name__}"
        )


class StockPurchaseProcessor(Processor):
    def process(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            stock_abbreviation = serializer.validated_data["stock_abbreviation"]
            quantity = serializer.validated_data["quantity"]

            owner = self.find_owner(user)
            stock = self.find_stock(stock_abbreviation)

            portfolio = self.create_portfolio(owner, stock, quantity, 9.99)

            return portfolio

    def find_stock(self, stock_abbreviation: str) -> Stock:
        return Stock.objects.get(abbreviation=stock_abbreviation)

    def find_owner(self, user: User) -> Owner:
        return Owner.objects.get(user=user)

    def create_portfolio(self, owner, stock, quantity, price) -> Portfolio:
        data = {
            "owner": owner,
            "stock": stock,
            "quantity": quantity,
            "transaction_price": price,
        }
        portfolio = Portfolio.objects.create(**data)
        return portfolio.save()
