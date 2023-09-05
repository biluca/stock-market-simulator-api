from django.db import migrations
from api.models import Company


def companies_bulky_insertion(apps, schema_editor):
    companies = [
        {
            "name": "Ammu Nation",
            "ceo_name": "Beatrice Blingbottom",
            "description": "Arming Your Future",
            "industry": "GUNS",
        },
        {
            "name": "Los Santos Customs",
            "ceo_name": "Reginald Ransomware Junior",
            "description": "Turning Rides into Reflections of You",
            "industry": "AUTOMOTIVE",
        },
        {
            "name": "Life Invader",
            "ceo_name": "Jay Norris",
            "description": "Connecting Lives, Shaping Stories",
            "industry": "SOCIAL_MEDIA",
        },
        {
            "name": "Pisswasser",
            "ceo_name": "Wellington Wallethoard",
            "description": "Refreshing the Spirit of Life",
            "industry": "DRINKS",
        },
        {
            "name": "Maze Bank",
            "ceo_name": "Maximilian Moneybags",
            "description": "Building Bridges to Your Financial Future",
            "industry": "FINANCES",
        },
        {
            "name": "Weazel News",
            "ceo_name": "Gertrude Goldrush",
            "description": "See Beyond, Tune into Tomorrow",
            "industry": "TELEVISON",
        },
        {
            "name": "Maibatsu",
            "ceo_name": "Hiroshi Fujimori",
            "description": "Driving Innovation, Defining the Future",
            "industry": "AUTOMOTIVE",
        },
        {
            "name": "Cluckin Bell",
            "ceo_name": "Penelope Powergrub",
            "description": "A Flavorful Tradition, Every Bell Satisfies",
            "industry": "FOODS",
        },
        {
            "name": "Vapid",
            "ceo_name": "Bartholomew Bankstack",
            "description": "Unleash the Road within You",
            "industry": "AUTOMOTIVE",
        },
        {
            "name": "Debonaire",
            "ceo_name": "Prudence Profitmunch",
            "description": "Elegance in Every Puff, Luxury in Every Draw",
            "industry": "TOBACCO",
        },
    ]

    for company in companies:
        Company.objects.create(**company)


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_users_insertion"),
    ]

    operations = [
        migrations.RunPython(
            companies_bulky_insertion,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
