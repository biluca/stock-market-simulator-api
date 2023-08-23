from django.db import migrations, transaction
from api.models import Stock, PriceMovement


def prices_movements_insertion(apps, schema_editor):
    movement_amount = 0.0
    price = 2.99

    stocks = Stock.objects.all()

    for stock in stocks:
        data = {
            "stock": stock,
            "movement_amount": movement_amount,
            "price": price,
        }

        with transaction.atomic():
            priceMovement = PriceMovement.objects.create(**data)


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0007_portfolio_transaction_price"),
    ]

    operations = [
        migrations.RunPython(
            prices_movements_insertion,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
