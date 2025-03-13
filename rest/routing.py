from django.urls import re_path
from rest import consumers

websocket_urlpatterns = [
    re_path(r"ws/notify/", consumers.NotificationConsumer.as_asgi()),
]