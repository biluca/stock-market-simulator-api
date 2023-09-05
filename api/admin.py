from django.contrib import admin
from api.models import User, Company, Stock, Transaction, Portfolio, PriceMovement


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["name", "cash_friendly"]


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "name",
        "ceo_name",
        "description",
        "industry",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "name",
    ]


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "abbreviation",
        "company",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "abbreviation",
    ]


@admin.register(PriceMovement)
class PriceMovementAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "stock",
        "price_friendly",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "stock",
    ]


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "user",
        "created_at",
        "updated_at",
    ]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "portfolio",
        "stock",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "stock",
    ]
