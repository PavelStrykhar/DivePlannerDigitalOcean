"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
application = get_asgi_application()
#from channels.routing import ProtocolTypeRouter
#from django.core.asgi import get_asgi_application

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

#application = ProtocolTypeRouter({
#    "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
    # WebSocket chat handler
#    "websocket": AuthMiddlewareStack(
#        URLRouter([
            #url(r"^chat/admin/$", AdminChatConsumer.as_asgi()),
            #url(r"^chat/$", PublicChatConsumer.as_asgi()),
#        ])
#    ),
#})