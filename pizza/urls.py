from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pizza.views import PizzaViewSet, ExtraViewSet, OrderViewSet

router = DefaultRouter()
router.register(r"pizzas", PizzaViewSet)
router.register(r"extras", ExtraViewSet)
router.register(r"orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
