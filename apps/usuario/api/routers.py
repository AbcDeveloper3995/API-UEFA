from rest_framework.routers import DefaultRouter

from apps.usuario.api.views import *

router = DefaultRouter()
router.register(r'', usuarioViewSet, basename='usuarioViewSet'),

urlpatterns = router.urls