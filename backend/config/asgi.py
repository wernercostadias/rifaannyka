from django.core.asgi import get_asgi_application
from config.settings_loader import configure_django_settings


configure_django_settings()

application = get_asgi_application()
