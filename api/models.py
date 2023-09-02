from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

from api.const import Industry, StockMarket


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


class Owner(BaseModel):
    name = models.CharField(max_length=128)
    cash = models.DecimalField(decimal_places=2, max_digits=12)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.name} [{self.user.username}]"

    @property
    def cash_friendly(self):
        return f"${self.cash:.2f}"


class Stock(BaseModel):
    company_name = models.CharField(max_length=128, null=False)
    description = models.CharField(max_length=256, null=True)
    abbreviation = models.CharField(max_length=3, unique=True, null=False)
    industry = models.CharField(max_length=128, choices=Industry.CHOICES, null=False)
    stock_market = models.CharField(
        max_length=128, choices=StockMarket.CHOICES, null=False
    )
    logo_url = models.URLField(null=True)

    owners = models.ManyToManyField(Owner, through="Portfolio")

    def __str__(self) -> str:
        return f"[{self.abbreviation}] {self.company_name}"


class Portfolio(BaseModel):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    transaction_price = models.DecimalField(
        decimal_places=2, max_digits=12, default=0.0
    )

    def __str__(self) -> str:
        return f"[{self.stock.abbreviation}, {self.quantity}] {self.owner.name}"


class PriceMovementManager(models.manager.Manager):
    def get_stock_last_price(self, stock):
        last_price = (
            PriceMovement.objects.filter(stock=stock).order_by("-created_at").first()
        )
        return last_price


class PriceMovement(BaseModel):
    stock = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)
    movement_amount = models.DecimalField(decimal_places=2, max_digits=12)
    price = models.DecimalField(decimal_places=2, max_digits=12)

    objects = PriceMovementManager()

    @property
    def percentual_change(self):
        change = self.movement_amount / (self.price - self.movement_amount) * 100
        return round(change, 2)

    @property
    def percentual_change_friendly(self):
        return f"{self.percentual_change} %"

    @property
    def stock_abbreviation(self):
        return self.stock.abbreviation

    def __str__(self) -> str:
        return f"[{self.stock.abbreviation}] {self.price} ({self.percentual_change}%)"
