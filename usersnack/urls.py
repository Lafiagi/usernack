from django.urls import re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from decouple import config


VERSION = config("VERSION", default="v1", cast=str)
schema_view = get_schema_view(
    openapi.Info(
        title="UserSnack API",
        default_version="v1",
        description="API powering the new usersnack app",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@UserSnack.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    url="https://api.ile-wa.com/usersnack",
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    re_path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        "redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    re_path(f"api/{VERSION}/", include("pizza.urls")),
]
