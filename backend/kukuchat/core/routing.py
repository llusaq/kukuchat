from django.urls import path

from channels.routing import URLRouter

from core.consumers import chat


chatapp = URLRouter([
    path('ws/chat/', chat.ChatConsumer),
])
