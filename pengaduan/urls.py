from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import PengaduanViewSet

router = DefaultRouter()
router.register("pengaduan", PengaduanViewSet, basename="pengaduan")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls")),
]
