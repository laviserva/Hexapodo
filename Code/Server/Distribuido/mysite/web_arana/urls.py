from django.urls import path
from . import views
urlpatterns= [
    path("", views.index, name="index"),
    path("<str:room_name>/",views.inicio,name="inicio"),
    path('logout/',views.singout,name='logout'),
    path('inicio1/',views.incio1,name='inicio1'),
    path('message/',views.enviar_comando, name='enviar_comando'),
]