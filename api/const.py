from collections.abc import Callable


class HTTP_METHODS:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"


class Industry:
    CHOICES = (
        ("GUNS", "Guns"),
        ("SPORTING_GOODS", "Sporting Goods"),
        ("INSURANCE", "Insurance"),
        ("FRANCHISE", "Franchise"),
        ("TELECOM", "Telecom"),
        ("PHARMA", "Pharma"),
        ("AUTOMOTIVE", "Automotive"),
        ("FOODS", "Foods"),
        ("FINANCES", "Finances"),
        ("SOCIAL_MEDIA", "Social Media"),
        ("LAW", "Law"),
        ("TELEVISON", "Televison"),
        ("TOBACCO", "Tobacco"),
        ("JOURNALISTIC", "Journalistic"),
        ("DRINKS", "Drinks"),
        ("AIRLINE", "Airline"),
        ("TECHONOLOGY", "Techonology"),
        ("REAL_ESTATE", "Real Estate"),
        ("TRANSPORT", "Transport"),
        ("SECURITY", "Security"),
        ("FUEL_DISTRIBUTION", "Fuel Distribution"),
        ("RADIO", "Radio"),
    )
