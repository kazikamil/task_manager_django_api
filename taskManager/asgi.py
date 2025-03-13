import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskManager.settings')

import django
django.setup()  # 🔥 Cette ligne est essentielle !

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from rest.middlewares import JWTAuthMiddleware
from rest.routing import websocket_urlpatterns

print("✅ asgi.py chargé par Daphne")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":
        JWTAuthMiddleware(
            URLRouter(websocket_urlpatterns)
        )
})
