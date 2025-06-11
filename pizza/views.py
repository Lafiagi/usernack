from django.db.models import Q
from rest_framework import viewsets, status

from django_filters import rest_framework
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from pizza.models import Pizza, Extra, Order
from pizza.serializers import (
    CalculateOrderAmountSerializer,
    PizzaSerializer,
    PizzaDetailSerializer,
    ExtraSerializer,
    OrderCreateSerializer,
    OrderSerializer,
)


class PizzaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Pizza.objects.filter(is_available=True).prefetch_related("ingredients")
    filter_backends = [rest_framework.DjangoFilterBackend]
    filterset_fields = ("name",)

    def get_serializer_class(self):
        return PizzaDetailSerializer if self.action == "retrieve" else PizzaSerializer

    def get_queryset(self):
        queryset = self.queryset
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(Q(name__icontains=search))
        return queryset

    @extend_schema(
        request=CalculateOrderAmountSerializer,
        responses={200: CalculateOrderAmountSerializer},
    )
    @action(detail=True, methods=["post"])
    def calculate_price(self, request, pk=None):
        pizza = self.get_object()
        extras_ids = request.data.get("extras", [])
        quantity = request.data.get("quantity", 1)

        try:
            quantity = int(quantity)
            if quantity < 1:
                return Response(
                    {"error": "Quantity must be at least 1"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid quantity"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        total_price = pizza.base_price * quantity

        if extras_ids:
            extras = Extra.objects.filter(
                id__in=set(extras_ids), is_available=True
            ).only("price")
            extras_price = sum(extra.price for extra in extras) * quantity
            total_price += extras_price

        return Response(
            {
                "pizza_id": pizza.id,
                "pizza_name": pizza.name,
                "base_price": pizza.base_price,
                "quantity": quantity,
                "extras_ids": extras_ids,
                "total_price": total_price,
            }
        )


class ExtraViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing available extras
    """

    queryset = Extra.objects.filter(is_available=True)
    serializer_class = ExtraSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for creating and managing orders
    """

    queryset = Order.objects.select_related("pizza").prefetch_related("extras")

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        # Recalculate total price after saving with extras
        order.total_price = order.calculate_total_price()
        order.save(update_fields=["total_price"])
