from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter

from core.routing import chatapp


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        chatapp,
    ),
})
