from django.db import models
from django.contrib.auth.models import User as DjangoUser
from uuid import uuid4
from api.const import Industry


class CreatedAndUpdatedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BaseModel(CreatedAndUpdatedModel):
    id = models.UUIDField(default=uuid4, primary_key=True)

    @property
    def uuid(self):
        return str(self.id)[0:8]

    class Meta:
        abstract = True


class User(DjangoUser):
    name = models.CharField(max_length=128)
    cash = models.DecimalField(decimal_places=2, max_digits=14)

    def __str__(self) -> str:
        return f"{self.name} [{self.username}]"

    @property
    def cash_friendly(self):
        return f"${self.cash:.2f}"


class PortfolioManager(models.manager.Manager):
    def get_stock_transactions(self, portfolio, stock=None):
        if stock == None:
            transactions = Transaction.objects.filter(portfolio=portfolio).order_by(
                "-created_at"
            )
        else:
            transactions = Transaction.objects.filter(
                stock=stock, portfolio=portfolio
            ).order_by("-created_at")

       
        return transactions


class Portfolio(BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    objects = PortfolioManager()

    def __str__(self) -> str:
        return f"{self.user.name}"


class Company(BaseModel):
    class Meta:
        verbose_name_plural = "Companies"

    name = models.CharField(max_length=128, null=False)
    ceo_name = models.CharField(max_length=128, null=True)
    description = models.CharField(max_length=256, null=True)
    industry = models.CharField(max_length=128, choices=Industry.CHOICES, null=False)

    def __str__(self) -> str:
        return f"{self.name} by {self.ceo_name}"


class Stock(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    abbreviation = models.CharField(max_length=3, unique=True, null=False)

    def __str__(self) -> str:
        return f"[{self.abbreviation}] {self.company.name}"


class Transaction(BaseModel):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.DO_NOTHING)
    stock = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)
    price = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    quantity = models.PositiveBigIntegerField(default=0)


class PriceMovementManager(models.manager.Manager):
    def get_stock_last_price(self, stock):
        last_price = (
            PriceMovement.objects.filter(stock=stock).order_by("-created_at").first()
        )
        return last_price


class PriceMovement(BaseModel):
    class Meta:
        verbose_name_plural = "Price Movements"

    objects = PriceMovementManager()

    stock = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)
    price = models.DecimalField(decimal_places=2, max_digits=12)

    @property
    def price_friendly(self):
        return f"$ {self.price:.2f}"
