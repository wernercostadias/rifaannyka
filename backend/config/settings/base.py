from pathlib import Path

import environ


BASE_DIR = Path(__file__).resolve().parents[2]
ROOT_DIR = BASE_DIR.parent

env = environ.Env(
    ENVIRONMENT=(str, "local"),
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    CORS_ALLOWED_ORIGINS=(list, []),
    RESERVATION_MINUTES=(int, 15),
    DATABASE_URL=(str, ""),
    POSTGRES_HOST=(str, ""),
    POSTGRES_PORT=(int, 5432),
    POSTGRES_DB=(str, ""),
    POSTGRES_USER=(str, ""),
    POSTGRES_PASSWORD=(str, ""),
    POSTGRES_SSLMODE=(str, "disable"),
    MERCADOPAGO_PUBLIC_KEY=(str, ""),
    MERCADOPAGO_ACCESS_TOKEN=(str, ""),
    MERCADOPAGO_WEBHOOK_SECRET=(str, ""),
    MERCADOPAGO_NOTIFICATION_URL=(str, ""),
    MERCADOPAGO_STATEMENT_DESCRIPTOR=(str, ""),
)

env_file = Path(env("ENV_FILE", default=str(ROOT_DIR / ".env")))
if env_file.exists():
    environ.Env.read_env(env_file)

SECRET_KEY = env("SECRET_KEY", default="dev-only-change-me")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "apps.core",
    "apps.rifa",
    "apps.compras",
    "apps.gateway",
    "apps.notifications",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Belem"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
RESERVATION_MINUTES = env("RESERVATION_MINUTES")

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

CORS_ALLOWED_ORIGINS = env(
    "CORS_ALLOWED_ORIGINS",
    default=["http://localhost:3000", "http://127.0.0.1:3000"],
)

MERCADOPAGO_PUBLIC_KEY = env("MERCADOPAGO_PUBLIC_KEY")
MERCADOPAGO_ACCESS_TOKEN = env("MERCADOPAGO_ACCESS_TOKEN")
MERCADOPAGO_WEBHOOK_SECRET = env("MERCADOPAGO_WEBHOOK_SECRET")
MERCADOPAGO_NOTIFICATION_URL = env("MERCADOPAGO_NOTIFICATION_URL")
MERCADOPAGO_STATEMENT_DESCRIPTOR = env("MERCADOPAGO_STATEMENT_DESCRIPTOR")


def get_database_url(default: str | None = None) -> str | None:
    database_url = env("DATABASE_URL", default="")
    if database_url:
        return database_url

    postgres_host = env("POSTGRES_HOST", default="")
    postgres_db = env("POSTGRES_DB", default="")
    postgres_user = env("POSTGRES_USER", default="")
    postgres_password = env("POSTGRES_PASSWORD", default="")

    if postgres_host and postgres_db and postgres_user and postgres_password:
        postgres_port = env("POSTGRES_PORT", default=5432)
        postgres_sslmode = env("POSTGRES_SSLMODE", default="disable")
        return (
            f"postgres://{postgres_user}:{postgres_password}"
            f"@{postgres_host}:{postgres_port}/{postgres_db}?sslmode={postgres_sslmode}"
        )

    return default
