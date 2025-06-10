from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from pizza.models import Order


@receiver(post_save, sender=Order)
def update_stock_on_order_creation(sender, instance, created, **kwargs):
    if created:
        pizza = instance.pizza
        pizza.quantity_in_stock = F("quantity_in_stock") - instance.quantity
        # we are using using F() expression for atomic update to prevent race conditions
        pizza.save(update_fields=["quantity_in_stock"])
        pizza.refresh_from_db()

        if pizza.quantity_in_stock <= 0:
            pizza.is_available = False
            pizza.save(update_fields=["is_available"])

        for extra in instance.extras.all():
            # Deduct the quantity of the order for each extra
            extra.quantity_in_stock = F("quantity_in_stock") - instance.quantity
            extra.save(update_fields=["quantity_in_stock"])
            extra.refresh_from_db()

            if extra.quantity_in_stock <= 0:
                extra.is_available = False
                extra.save(update_fields=["is_available"])
