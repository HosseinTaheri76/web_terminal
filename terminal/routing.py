from django.urls import path

from .consumers import TerminalConsumer

websocket_urlpatterns = [
    path('ws/terminal/', TerminalConsumer.as_asgi()),
]