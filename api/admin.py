from django.contrib import admin

from api.models import Owner, Stock, Portfolio, PriceMovement


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "abbreviation",
        "company_name",
        "description",
        "industry",
        "stock_market",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "abbreviation",
        "company_name",
    ]


@admin.register(PriceMovement)
class PriceMovementAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "stock_abbreviation",
        "price",
        "movement_amount",
        "percentual_change_friendly",
        "created_at",
        "updated_at",
    ]


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "name",
        "cash_friendly",
        "user",
        "created_at",
        "updated_at",
    ]


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "owner",
        "stock",
        "quantity",
        "transaction_price",
        "created_at",
        "updated_at",
    ]
