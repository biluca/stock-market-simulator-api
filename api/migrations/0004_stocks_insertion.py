from django.db import migrations
from api.models import Stock, Company


def stocks_bulky_insertion(apps, schema_editor):
    stocks = [
        {
            "company_name": "Ammu Nation",
            "abbreviation": "AMU",
        },
        {
            "company_name": "Los Santos Customs",
            "abbreviation": "LSC",
        },
        {
            "company_name": "Life Invader",
            "abbreviation": "LFI",
        },
        {
            "company_name": "Pisswasser",
            "abbreviation": "PIS",
        },
        {
            "company_name": "Maze Bank",
            "abbreviation": "MAZ",
        },
        {
            "company_name": "Weazel News",
            "abbreviation": "WZL",
        },
        {
            "company_name": "Maibatsu",
            "abbreviation": "MAI",
        },
        {
            "company_name": "Cluckin Bell",
            "abbreviation": "CLK",
        },
        {
            "company_name": "Vapid",
            "abbreviation": "VAP",
        },
        {
            "company_name": "Debonaire",
            "abbreviation": "DEB",
        },
    ]

    for stock in stocks:
        company = Company.objects.get(name=stock["company_name"])
        stock["company"] = company
        stock.pop("company_name")
        Stock.objects.create(**stock)


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0003_companies_insertion"),
    ]

    operations = [
        migrations.RunPython(
            stocks_bulky_insertion,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
