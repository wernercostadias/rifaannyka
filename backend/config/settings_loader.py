import os


SETTINGS_BY_ENVIRONMENT = {
    "local": "config.settings.local",
    "production": "config.settings.production",
}


def get_settings_module() -> str:
    explicit_module = os.environ.get("DJANGO_SETTINGS_MODULE")
    if explicit_module:
        return explicit_module

    environment = os.environ.get("ENVIRONMENT", "local").strip().lower()
    return SETTINGS_BY_ENVIRONMENT.get(environment, SETTINGS_BY_ENVIRONMENT["local"])


def configure_django_settings() -> str:
    settings_module = get_settings_module()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    return settings_module
