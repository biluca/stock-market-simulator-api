from django.db import migrations
from django.contrib.auth.hashers import make_password
from api.models import User


def users_insertion(apps, schema_editor):
    users = [
        {
            "username": "franklin",
            "is_staff": True,
            "password": make_password("franklin"),
            "last_login": "2013-09-17 00:00:00",
            "is_superuser": True,
            "name": "Franklin Clinton",
            "cash": 300000,
        },
        {
            "username": "michael",
            "is_staff": True,
            "password": make_password("michael"),
            "last_login": "2013-09-17 00:00:00",
            "is_superuser": True,
            "name": "Michael De Santa",
            "cash": 14000000,
        },
        {
            "username": "trevor",
            "is_staff": True,
            "password": make_password("trevor"),
            "last_login": "2013-09-17 00:00:00",
            "is_superuser": True,
            "name": "Trevor Philips",
            "cash": 8000000,
        },
        {
            "username": "biluca",
            "is_staff": True,
            "password": make_password("biluca"),
            "last_login": "2013-09-17 00:00:00",
            "is_superuser": True,
            "name": "Vinicios Biluca",
            "cash": 800,
        },
    ]

    for user in users:
        User.objects.create(**user)


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            users_insertion,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
