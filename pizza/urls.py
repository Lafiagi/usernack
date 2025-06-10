from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pizza.views import PizzaViewSet, ExtraViewSet, OrderViewSet

router = DefaultRouter()
router.register(r"pizza", PizzaViewSet)
router.register(r"extra", ExtraViewSet)
router.register(r"order", OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
