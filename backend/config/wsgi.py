from django.core.wsgi import get_wsgi_application
from config.settings_loader import configure_django_settings


configure_django_settings()

application = get_wsgi_application()
