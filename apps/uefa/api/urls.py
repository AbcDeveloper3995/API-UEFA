from django.urls import path
from apps.uefa.api.views import *

urlpatterns = [
    path('jugador/', jugadorApiView.as_view(), name='jugadorApi'),
    path('equipo/', equipoApiView.as_view(), name='equipoApi'),
    path('liga/', ligaApiView.as_view(), name='ligaApi'),
]