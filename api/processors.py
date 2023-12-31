from api.serializers import OperationStockSerializer
from api.models import Stock, User, Portfolio, PriceMovement, Transaction
from api.simulator import MeanReversionSimulator
from decimal import Decimal


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

            data = {
                "stock": stock,
                "price": next_price,
            }

            PriceMovement.objects.create(**data)


class StockProcessor(Processor):
    def get_stock(self, stock_abbreviation):
        try:
            return Stock.objects.get(abbreviation=stock_abbreviation)
        except:
            raise ValueError("Stock Not Found!")

    def get_or_create_portfolio(self, user):
        portfolio_user = User.objects.get(id=user.id)
        portfolio, new = Portfolio.objects.get_or_create(user=portfolio_user)
        return portfolio

    def update_user(self, transaction):
        user = transaction["portfolio"].user
        user_cash = user.cash
        quantity = transaction["quantity"]
        price = Decimal(transaction["price"])

        user.cash = user_cash - (quantity * price)
        user.save()


class BuyStockProcessor(StockProcessor):
    def process(self, request):
        serializer = OperationStockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quantity = serializer.validated_data["quantity"]
        stock = self.get_stock(serializer.validated_data["stock_abbreviation"])
        portfolio = self.get_or_create_portfolio(request.user)
        price_movement = PriceMovement.objects.get_stock_last_price(stock)
        if price_movement:
            price = price_movement.price
        else:
            price = 0.0

        transaction = {
            "quantity": quantity,
            "stock": stock,
            "portfolio": portfolio,
            "price": price,
        }

        self.validate_transaction(transaction)
        new_transaction = Transaction.objects.create(**transaction)
        self.update_user(transaction)

        return new_transaction

    def validate_transaction(self, transaction):
        user = transaction["portfolio"].user
        user_cash = user.cash
        transaction_quantity = transaction["quantity"]
        price = transaction["price"]

        if abs(transaction_quantity) <= 0:
            raise ValueError("Make sure that the Quanity is Greater or Equal to 1!")

        if user_cash < (transaction_quantity * price):
            raise ValueError("User does not have sufficient funds!")


class SellStockProcessor(StockProcessor):
    def process(self, request):
        serializer = OperationStockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quantity = serializer.validated_data["quantity"]
        stock = self.get_stock(serializer.validated_data["stock_abbreviation"])
        portfolio = self.get_or_create_portfolio(request.user)
        price = PriceMovement.objects.get_stock_last_price(stock).price

        transaction = {
            "quantity": quantity * (-1),
            "stock": stock,
            "portfolio": portfolio,
            "price": price,
        }

        self.validate_transaction(transaction)
        new_transaction = Transaction.objects.create(**transaction)
        self.update_user(transaction)

        return new_transaction

    def validate_transaction(self, transaction):
        portfolio = transaction["portfolio"]
        stock = transaction["stock"]
        transaction_quantity = transaction["quantity"]

        if abs(transaction_quantity) <= 0:
            raise ValueError("Make sure that the Quanity is Greater or Equal to 1!")

        transactions = Transaction.objects.get_portfolio_stock_transactions(
            portfolio, stock
        )

        quantity_stocks_owned = 0
        for transaction in transactions:
            if transaction.quantity > 0:
                quantity_stocks_owned = quantity_stocks_owned + transaction.quantity

        if abs(transaction_quantity) > quantity_stocks_owned:
            raise ValueError(
                f"User does not Own that Quantity on the [{stock.abbreviation}] Stock! Quantity Owned: {quantity_stocks_owned}"
            )
