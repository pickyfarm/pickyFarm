import os
import dotenv
from django.core.wsgi import get_wsgi_application

dotenv.read_dotenv(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.debug")

application = get_wsgi_application()