from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls", namespace="main")),
]

handler404 = "main.views.custom_handler404"
handler500 = "main.views.custom_handler500"
