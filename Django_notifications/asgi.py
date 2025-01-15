"""
ASGI config for Django_notifications project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
# asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from notification_app.consumers import NotificationConsumer  # Update with your app name
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_notifications.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/notifications/', NotificationConsumer.as_asgi()),  # Update the path as needed
        ])
    ),
})











"""
import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import notification_app.routing


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django_notifications.settings")


application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(
            notification_app.routing.websocket_urlpatterns
        )
    ),
})


"""



