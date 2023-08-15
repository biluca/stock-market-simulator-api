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

    class Meta:
        abstract = True


class Owner(BaseModel):
    name = models.CharField(max_length=128)
    cash = models.DecimalField(decimal_places=2, max_digits=12)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)


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


class Portfolio(BaseModel):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()


class PriceMovement(BaseModel):
    stock = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)
    movement_amount = models.DecimalField(decimal_places=2, max_digits=12)
    price = models.DecimalField(decimal_places=2, max_digits=12)

    @property
    def percentual_change(self):
        change = self.movement_amount / (self.price - self.movement_amount)
        return round(change, 3)
    
