from django.urls import path
from apps.usuario.api.views import Login

urlpatterns = [
    path('', Login.as_view(), name='login'),
]