from rest_framework.routers import DefaultRouter

from apps.uefa.api.views import *

router = DefaultRouter()
router.register(r'liga', ligaViewSet, basename='ligaViewSet'),
router.register(r'equipo', equipoViewSet, basename='equipoViewSet'),
router.register(r'jugador', jugadorViewSet, basename='jugadorViewSet')

urlpatterns = router.urls