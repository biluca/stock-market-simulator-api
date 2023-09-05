from django.db import migrations
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


def users_insertion(apps, schema_editor):
    users = [
        {
            "username": "franklin",
            "is_staff": True,
            "password": make_password("franklin"),
            "last_login": "2013-09-17 00:00:00",
            "is_superuser": True,
        },
        {
            "username": "michael",
            "is_staff": True,
            "password": make_password("michael"),
            "last_login": "2013-09-17 00:00:00",
            "is_superuser": True,
        },
        {
            "username": "trevor",
            "is_staff": True,
            "password": make_password("trevor"),
            "last_login": "2013-09-17 00:00:00",
            "is_superuser": True,
        },
    ]

    for user in users:
        User.objects.create(**user)


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0005_stocks_bulky_insertion copy"),
    ]

    operations = [
        migrations.RunPython(
            users_insertion,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
