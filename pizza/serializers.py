from typing import List

from rest_framework import serializers

from pizza.models import Pizza, Extra, Order, Ingredient


class ExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extra
        fields = ["id", "name", "price"]
        read_only_fields = ("id",)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name"]


class PizzaSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Pizza
        fields = [
            "id",
            "name",
            "base_price",
            "image_url",
            "ingredients",
            "created_at",
        ]
        read_only_fields = ("id", "created_at")


class CalculateOrderAmountSerializer(serializers.Serializer):
    extras = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text="List of extra item IDs to include.",
    )
    quantity = serializers.IntegerField(
        default=1, min_value=1, help_text="Quantity of the pizza."
    )

    pizza_id = serializers.IntegerField(read_only=True)
    pizza_name = serializers.CharField(read_only=True)
    base_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )


class PizzaDetailSerializer(serializers.ModelSerializer):
    available_extras = serializers.SerializerMethodField()
    ingredients = IngredientSerializer(many=True, read_only=True)

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
            "ingredients"
        ]
        read_only_fields = ("id", "created_at",)

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
            "id",
            "pizza",
            "extras",
            "quantity",
            "customer_name",
            "delivery_address",
            "calculated_total",
        ]
        read_only_fields = ("id", "created_at")

    def get_calculated_total(self, obj) -> float:
        if obj.pk:
            return obj.calculate_total_price()
        return None

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value

    def validate_pizza(self, value):
        if not value.is_available or value.quantity_in_stock <= 0:
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

    def validate(self, attrs):
        pizza = attrs.get("pizza")
        extras = attrs.get("extras", [])
        quantity = attrs.get("quantity", 1)

        # Ensure enough pizza in stock
        if pizza and pizza.quantity_in_stock < quantity:
            raise serializers.ValidationError(
                f"Only {pizza.quantity_in_stock} pizzas left in stock."
            )

        # Ensure enough of each extra in stock
        low_stock_extras = [
            extra for extra in extras if extra.quantity_in_stock < quantity
        ]
        if low_stock_extras:
            names = [extra.name for extra in low_stock_extras]
            raise serializers.ValidationError(
                f"Insufficient stock for extras: {', '.join(names)}"
            )

        return attrs


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
