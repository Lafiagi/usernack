from django.contrib import admin
from django.urls import path, include
from decouple import config

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

VERSION = config("VERSION", default="v1", cast=str)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"api//usersnack/{VERSION}/pizzas/", include("pizza.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url="/usersnack/api/schema/"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
