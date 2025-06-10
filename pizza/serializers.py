from typing import List

from rest_framework import serializers

from pizza.models import Pizza, Extra, Order


class ExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extra
        fields = ["id", "name", "price"]
        read_only_fields = ("id",)


class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = [
            "id",
            "name",
            "base_price",
            "image_url",
            "created_at",
        ]
        read_only_fields = ("id", "created_at")


class PizzaDetailSerializer(serializers.ModelSerializer):
    available_extras = serializers.SerializerMethodField()

    class Meta:
        model = Pizza
        fields = [
            "id",
            "name",
            "base_price",
            "image_url",
            "is_available",
            "available_extras",
            "created_at",
        ]
        read_only_fields = ("id", "created_at")

    def get_available_extras(self, _) -> List[Extra]:
        extras = Extra.objects.filter(is_available=True)
        return ExtraSerializer(extras, many=True).data


class OrderCreateSerializer(serializers.ModelSerializer):
    extras = serializers.PrimaryKeyRelatedField(
        queryset=Extra.objects.all(), many=True, required=False
    )
    calculated_total = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "pizza",
            "extras",
            "quantity",
            "customer_name",
            "delivery_address",
            "calculated_total",
        ]

    def get_calculated_total(self, obj) -> float:
        if obj.pk:
            return obj.calculate_total_price()
        return None

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")

        return value

    def validate_pizza(self, value):
        if not value.is_available:
            raise serializers.ValidationError("This pizza is currently unavailable")
        return value

    def validate_extras(self, value):
        unavailable_extras = [extra for extra in value if not extra.is_available]
        if unavailable_extras:
            names = [extra.name for extra in unavailable_extras]
            raise serializers.ValidationError(
                f"These extras are unavailable: {', '.join(names)}"
            )
        return value


class OrderSerializer(serializers.ModelSerializer):
    pizza = PizzaSerializer(read_only=True)
    extras = ExtraSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "pizza",
            "extras",
            "quantity",
            "total_price",
            "status",
            "customer_name",
            "delivery_address",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "created_at", "updated_at")
