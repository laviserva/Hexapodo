from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ConsumidorVotacion.as_asgi()),
    re_path(r"ws/img/(?P<room_name>\w+)/$",consumers.ConsumidorIMG.as_asgi())
]