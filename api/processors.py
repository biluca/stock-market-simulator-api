from api.serializers import BuyTransactionSerializer, SellTransactionSerializer
from api.models import Stock, Owner, Portfolio, PriceMovement
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from decimal import Decimal
from api.simulator import MeanReversionSimulator


class Processor:
    def process(self, request):
        raise NotImplementedError(
            f"You must use define a process implementation {__class__.__name__}"
        )


class StockDataSimulationProcessor(Processor):
    PRICE_MOVEMENTS_RANGE = 10

    def process(self, request):
        stocks = Stock.objects.all()

        for stock in stocks:
            self.generate_price_movements(stock)

    def generate_price_movements(self, stock):
        simulator = MeanReversionSimulator()
        for _ in range(self.PRICE_MOVEMENTS_RANGE):
            next_price = simulator.generate_next_price()
            print(next_price)
            stock_price = PriceMovement.objects.get_stock_last_price(stock)

            if stock_price:
                movement_amount = stock_price.price - Decimal(next_price)
            else:
                movement_amount = 0.1

            data = {
                "stock": stock,
                "price": next_price,
                "movement_amount": movement_amount,
            }

            PriceMovement.objects.create(**data)


class StockBuyProcessor(Processor):
    def process(self, request):
        serializer = BuyTransactionSerializer(data=request.data)
        transaction = self.build_and_validate_transaction(request, serializer)

        portfolio = self.create_portfolio(transaction)
        self.update_owner_cash(transaction)

        return portfolio

    def build_and_validate_transaction(self, request, serializer):
        if serializer.is_valid(raise_exception=True):
            user = request.user
            owner = self.find_and_validate_owner(user)
            stock_abbreviation = serializer.validated_data["stock_abbreviation"]
            stock = self.find_and_validate_stock(stock_abbreviation)
            quantity = serializer.validated_data["quantity"]
            transaction_price = self.find_stock_price(stock)

            transaction = {
                "owner": owner,
                "stock": stock,
                "quantity": quantity,
                "transaction_price": transaction_price,
            }

            self.validate_owners_cash(transaction)

            return transaction

    def find_stock_price(self, stock):
        return PriceMovement.objects.get_stock_last_price(stock).price

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
        serializer = SellTransactionSerializer(data=request.data)
        transaction = self.build_and_validate_transaction(request, serializer)

        portfolio = self.create_portfolio(transaction)
        self.update_owner_cash(transaction)

    def build_and_validate_transaction(self, request, serializer):
        pass

    def create_portfolio(self, transaction):
        pass

    def update_owner_cash(self, transaction):
        pass
