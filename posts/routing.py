from django.urls import path
from posts.consumers import ChatConsumer


websockets_urls = [
    path('ws/chat/', ChatConsumer.as_asgi())
]