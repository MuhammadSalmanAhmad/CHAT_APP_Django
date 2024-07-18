
"""
async def application(scope, receive, send):
    assert scope['type'] == 'http'

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            (b'content-type', b'text/plain'),
        ]
    })

    await send({
        'type': 'http.response.body',
        'body': b'Hello, World!',
    })
  

"""

import os
import django
from django.urls import path, re_path
from chat.consumers import ChatConsumer
from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ChatProject.settings")
django.setup()

django_asgi_app = get_asgi_application()



application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": 
        URLRouter(
            [  re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),]
        )
    
})


