"""
ASGI config for real_time_analystics_Dashboard project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""




import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'real_time_analystics_Dashboard.settings')

# Initialize Django ASGI application early to ensure settings are loaded
django_asgi_app = get_asgi_application()

# Import routing after Django is set up
import analytics.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            analytics.routing.websocket_urlpatterns
        )
    ),
})
