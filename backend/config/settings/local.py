from .base import *  # noqa: F403


DEBUG = True

DATABASES = {
    "default": env.db("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")  # noqa: F405
}
