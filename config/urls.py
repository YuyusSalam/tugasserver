from django.contrib import admin
from django.urls import include, path
from pengaduan.views import beranda

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("pengaduan.urls")),
    path("", beranda, name="beranda"),
]
