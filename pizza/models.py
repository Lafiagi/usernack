from django.db import models
from django.db import transaction

from generics.BaseModel import BaseModel
from pizza.choices import DeliveryStatus


class Ingredient(BaseModel):
    name = models.CharField(max_length=100)


class Pizza(BaseModel):
    name = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Extra(BaseModel):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(BaseModel):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    extras = models.ManyToManyField(Extra, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, default=0.0
    )
    status = models.CharField(max_length=20, choices=DeliveryStatus, default="pending")
    customer_name = models.CharField(max_length=100)
    delivery_address = models.TextField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} - {self.customer_name}"

    def calculate_total_price(self):
        """Calculate total price including pizza base price and extras"""
        total = self.pizza.base_price * self.quantity
        for extra in self.extras.all():
            total += extra.price * self.quantity
        return total

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # Lock the pizza row
            pizza = Pizza.objects.select_for_update().get(pk=self.pizza.pk)
            pizza.quantity_in_stock -= self.quantity
            if pizza.quantity_in_stock <= 0:
                pizza.is_available = False
            pizza.save(update_fields=["quantity_in_stock", "is_available"])

            if not self.total_price:
                super().save(*args, **kwargs)
                self.total_price = self.calculate_total_price()
                super().save(update_fields=["total_price"])
            else:
                super().save(*args, **kwargs)

            for extra in self.extras.all():
                extra.quantity_in_stock = extra.quantity_in_stock - self.quantity
                extra.save(update_fields=["quantity_in_stock"])
                extra.refresh_from_db()

                if extra.quantity_in_stock <= 0:
                    extra.is_available = False
                    extra.save(update_fields=["is_available"])
