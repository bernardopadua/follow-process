from django.urls import re_path

from channels.routing import URLRouter, ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from followprocess.process.consumers import ProcessConsumer

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r'^process/websock/$', ProcessConsumer),
        ])
    ),
})