from api.serializers import BuyTransactionSerializer, SellTransactionSerializer
from api.models import Stock, User, Portfolio, PriceMovement
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
            }

            PriceMovement.objects.create(**data)


class StockBuyProcessor(Processor):
    def process(self, request):
        pass

    def build_and_validate_transaction(self, request, serializer):
        pass

    def create_portfolio(self, transaction):
        pass

    def update_owner_cash(self, transaction):
        pass


class StockSellProcessor(Processor):
    def process(self, request):
        pass

    def build_and_validate_transaction(self, request, serializer):
        pass

    def create_portfolio(self, transaction):
        pass

    def update_owner_cash(self, transaction):
        pass
