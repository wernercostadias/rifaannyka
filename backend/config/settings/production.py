from .base import *  # noqa: F403
from django.core.exceptions import ImproperlyConfigured


DEBUG = False

database_url = get_database_url()  # noqa: F405
if not database_url:
    raise ImproperlyConfigured(
        "Defina DATABASE_URL ou as variaveis POSTGRES_HOST, POSTGRES_PORT, "
        "POSTGRES_DB, POSTGRES_USER e POSTGRES_PASSWORD."
    )

DATABASES = {
    "default": env.db(database_url)  # noqa: F405
}
