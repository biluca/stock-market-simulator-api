from django.contrib import admin

from api.models import Owner, Stock, Portfolio, PriceMovement

admin.site.register(Owner)
admin.site.register(Stock)
admin.site.register(Portfolio)
admin.site.register(PriceMovement)
