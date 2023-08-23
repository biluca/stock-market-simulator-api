from django.db import migrations, transaction
from api.models import Stock, PriceMovement
from decimal import Decimal


def prices_dict():
    return [
        {"stock": "AMU", "price": "2.99", "movement_amount": "0.30"},
        {"stock": "AMU", "price": "3.29", "movement_amount": "0.30"},
        {"stock": "AMU", "price": "3.59", "movement_amount": "0.50"},
        {"stock": "AMU", "price": "4.09", "movement_amount": "0.30"},
        {"stock": "AMU", "price": "4.39", "movement_amount": "0.30"},
        {"stock": "AMU", "price": "4.69", "movement_amount": "0.60"},
        {"stock": "AMU", "price": "5.29", "movement_amount": "0.40"},
        {"stock": "AMU", "price": "5.69", "movement_amount": "1.00"},
        {"stock": "AMU", "price": "6.69", "movement_amount": "1.00"},
        {"stock": "AMU", "price": "7.69", "movement_amount": "0.90"},
        {"stock": "DEB", "price": "2.99", "movement_amount": "-1.600"},
        {"stock": "DEB", "price": "1.390", "movement_amount": "-2.200"},
        {"stock": "DEB", "price": "-0.810", "movement_amount": "-1.900"},
        {"stock": "DEB", "price": "-2.710", "movement_amount": "-1.400"},
        {"stock": "DEB", "price": "-4.110", "movement_amount": "-1.600"},
        {"stock": "DEB", "price": "-5.710", "movement_amount": "-1.500"},
        {"stock": "DEB", "price": "-7.210", "movement_amount": "-3.200"},
        {"stock": "DEB", "price": "-10.410", "movement_amount": "-1.500"},
        {"stock": "DEB", "price": "-11.910", "movement_amount": "-1.800"},
        {"stock": "DEB", "price": "-13.710", "movement_amount": "-1.100"},
        {"stock": "GCD", "price": "2.99", "movement_amount": "-0.500"},
        {"stock": "GCD", "price": "2.490", "movement_amount": "-0.400"},
        {"stock": "GCD", "price": "2.090", "movement_amount": "0.500"},
        {"stock": "GCD", "price": "2.590", "movement_amount": "-0.400"},
        {"stock": "GCD", "price": "2.190", "movement_amount": "0.800"},
        {"stock": "GCD", "price": "2.990", "movement_amount": "-0.500"},
        {"stock": "GCD", "price": "2.490", "movement_amount": "2.000"},
        {"stock": "GCD", "price": "4.490", "movement_amount": "-0.500"},
        {"stock": "GCD", "price": "3.990", "movement_amount": "-0.400"},
        {"stock": "GCD", "price": "3.590", "movement_amount": "0.900"},
        {"stock": "PIS", "price": "2.99", "movement_amount": "-0.300"},
        {"stock": "PIS", "price": "2.690", "movement_amount": "-0.500"},
        {"stock": "PIS", "price": "2.190", "movement_amount": "-0.400"},
        {"stock": "PIS", "price": "1.790", "movement_amount": "-0.500"},
        {"stock": "PIS", "price": "1.290", "movement_amount": "-0.300"},
        {"stock": "PIS", "price": "0.990", "movement_amount": "-0.400"},
        {"stock": "PIS", "price": "0.590", "movement_amount": "-0.400"},
        {"stock": "PIS", "price": "0.190", "movement_amount": "-0.300"},
        {"stock": "PIS", "price": "-0.110", "movement_amount": "-0.400"},
        {"stock": "PIS", "price": "-0.510", "movement_amount": "-0.500"},
        {"stock": "SKS", "price": "2.99", "movement_amount": "5.200"},
        {"stock": "SKS", "price": "8.190", "movement_amount": "5.200"},
        {"stock": "SKS", "price": "13.390", "movement_amount": "6.900"},
        {"stock": "SKS", "price": "20.290", "movement_amount": "5.900"},
        {"stock": "SKS", "price": "26.190", "movement_amount": "4.900"},
        {"stock": "SKS", "price": "31.090", "movement_amount": "4.200"},
        {"stock": "SKS", "price": "35.290", "movement_amount": "9.400"},
        {"stock": "SKS", "price": "44.690", "movement_amount": "9.900"},
        {"stock": "SKS", "price": "54.590", "movement_amount": "7.200"},
        {"stock": "SKS", "price": "61.790", "movement_amount": "6.600"},
    ]


def prices_movements_insertion(apps, schema_editor):
    prices = prices_dict()

    for price in prices:
        stock = Stock.objects.get(abbreviation=price.get("stock"))

        data = {
            "stock": stock,
            "movement_amount": Decimal(price.get("movement_amount")),
            "price": Decimal(price.get("price")),
        }

        with transaction.atomic():
            priceMovement = PriceMovement.objects.create(**data)


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0008_price_movement_insertion"),
    ]

    operations = [
        migrations.RunPython(
            prices_movements_insertion,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
