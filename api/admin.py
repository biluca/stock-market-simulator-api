from django.contrib import admin

from api.models import Owner, Stock, Portfolio, PriceMovement


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = [
        "abbreviation",
        "company_name",
        "description",
        "industry",
        "stock_market",
    ]

    list_filter = [
        "abbreviation",
        "company_name",
    ]


@admin.register(PriceMovement)
class PriceMovementAdmin(admin.ModelAdmin):
    list_display = [
        "stock_abbreviation",
        "price",
        "movement_amount",
        "percentual_change_friendly",
        "created_at",
        "updated_at",
    ]


admin.site.register(Owner)
admin.site.register(Portfolio)
