from .base import *  # noqa: F403


DEBUG = True

DATABASES = {
    "default": env.db(get_database_url(default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"))  # noqa: F405
}
